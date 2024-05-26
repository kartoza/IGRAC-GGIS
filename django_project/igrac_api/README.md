# IGRAC API

Igrac API is used to fetch data using API with xml format.
Technically it is using istSOS with version 1.0.0

GetCapabilities
```
http://localhost/istsos?service=SOS&request=GetCapabilities&api-key=<api-key>
```


DescribeSensor
```
https://localhost/istsos?service=SOS&version=1.0.0&request=DescribeSensor&procedure=<procedure-id>&outputFormat=text/xml;subtype="sensorML/1.0.1"&api-key=<api-key>
```