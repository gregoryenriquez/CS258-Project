import requests

url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1"

headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}

response = requests.delete(url, headers=headers, auth=('admin', 'admin'))

print(response.text)
