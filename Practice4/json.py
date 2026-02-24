import json

with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("DN | Description | Speed | MTU")
print("---------------------------------------")

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes["dn"]
    description = attributes["descr"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    
    print(dn, "|", description, "|", speed, "|", mtu)