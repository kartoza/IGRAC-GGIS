import requests
import pypandoc
import re

def define_env(env):
    @env.macro
    def include_remote_doc(url, image_base_url=None):
        """
        Includes a remote .md or .rst document.
        - Converts .rst to Markdown.
        - Leaves .md as-is.
        - Optionally rewrites relative image paths.
        """
        response = requests.get(url)
        if response.status_code != 200:
            return f"*Failed to fetch {url}*"

        content = response.text

        # Convert .rst to Markdown if necessary
        if url.endswith((".rst", ".rst.txt")):
            try:
                pypandoc.download_pandoc()
                content = pypandoc.convert_text(content, to='markdown', format='rst')
            except Exception as e:
                return f"*Conversion failed: {e}*"

        # If an image base URL is provided, rewrite relative image paths
        if image_base_url:
            content = re.sub(
                # Match Markdown image syntax with relative paths
                r'!\[([^\]]*)\]\(\s*(?:\.\/)?(?:img|images(?:/manual)?(?:/en)?)\/([^)]+?)\s*\)',
                lambda match: f'![{match.group(1)}]({image_base_url}/{match.group(2)})',
                content
            )

        return content
