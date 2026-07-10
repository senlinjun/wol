import requests,json
from subprocess import Popen

with open("config.json","r") as f:
    data = json.load(f)

try:
    res = requests.get(f"http://{data['server']}/api/gettargetsystem/{data['instance_id']}").json()
    if res["state"] == 0:
        target = res["order"]
        if target != data["order"]:
            print(f"reboot to {target}")
            Popen(f"grub-reboot {target}")
            Popen("reboot")
except Exception as e:
    pass