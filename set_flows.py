import requests
import time

headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}

url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1"
response = requests.put(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow1.xml').read())
print(response.text)

time.sleep(2)

url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/2"
response = requests.put(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow2.xml').read())
print(response.text)

time.sleep(2)

url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/3"
response = requests.put(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow3.xml').read())
print(response.text)
