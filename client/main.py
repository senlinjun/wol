import requests,json
from subprocess import Popen

with open("config.json","r") as f:
    data = json.load(f)
target = requests.get(f"{data['server']}/api/gettargetssystem/{data['instance_id']}")
if target != data["instance_id"]:
    Popen(f"grub-reboot {target}")
    Popen(f"reboot")
