"""
update_config.py

This script updates the GeoServer security config file by appending a new filter to the filter chain.

"""
import xml.etree.ElementTree as ET
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def append_filterchain_config(xml_file, new_filter_config, append_before=None):
    """Append geoserver filterchain to the security configuration

    Args:
        xml_file (path): Path to the security config file e.g. GEOSERVER_DATA_DIR/security/config.xml
        new_filter_config (path): XML string for the new filter configuration
        append_before (string): Name of the filter of the relative filter to append before. If None, the new filter is appended to the bottom of the filter chain

    Raises:
        ValueError: Raises an error when the path of the security config file is not valid
    """
    logging.info(f"Updating configuration for {xml_file}")

    if not os.path.exists(xml_file):
        logging.error(f"File {xml_file} does not exist")
        return
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Locate the filters container
    filterchain_container = root.find('filterChain')
    if filterchain_container is None:
        filterchain_container = root.find('filterchain')
        if filterchain_container is None:
            logging.error("No <filterChain> element found in the XML")
            return

    # Create XML from the new configuration
    new_filter_config_xml = ET.fromstring(new_filter_config)

    filters = filterchain_container.findall('filters')
    if append_before is not None:
        for index, filter in enumerate(filters):
            if new_filter_config_xml.get('name') == filter.get('name'):
                # Already exists
                break
            if filter.get('name') == append_before:
                filterchain_container.insert(index, new_filter_config_xml)
                break
    else:
        filterchain_container.append(new_filter_config_xml)

    # Write back to the file
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    logging.info(f"Configuration for {xml_file} applied.")


append_before = "gwc"
new_filter_config = '''
    <filters name="gwc service wmts" class="org.geoserver.security.ServiceLoginFilterChain" interceptorName="interceptor" exceptionTranslationName="exception" path="/gwc/service/**" disabled="true" allowSessionCreation="false" ssl="false" matchHTTPMethod="true" httpMethods="GET">
        <filter>anonymous</filter>
    </filters>
'''

append_filterchain_config(
    f"{os.environ.get('GEOSERVER_DATA_DIR')}/security/config.xml", new_filter_config, append_before)
