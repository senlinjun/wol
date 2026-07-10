import requests,json
import subprocess

with open("config.json","r") as f:
    data = json.load(f)

try:
    res = requests.get(f"http://{data['server']}/api/gettargetsystem/{data['instance_id']}").json()
    if res["state"] == 0:
        target = res["order"]
        if target != data["order"]:
            print(f"reboot to {target}")
            subprocess.run(f"sudo grub-reboot {target}",shell=True)
            subprocess.run("sudo reboot",shell=True)
except Exception as e:
    print(f"ERROR: {e}")