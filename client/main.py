import requests,json
import subprocess

with open("config.json","r") as f:
    data = json.load(f)

flag = False
attempt_times = 0
while not network_reachable and attempt_times < data["attempt"]:
    try:
        res = requests.get(f"http://{data['server']}/api/gettargetsystem/{data['instance_id']}")
        attempt_times += 1
        flag = True
    except:
        time.sleep(data["attempt_second"])
        pass

if flag:
    if res_data["state"] == 0:
        target = res_data["order"]
        if target != data["order"]:
            print(f"reboot to {target}")
            subprocess.run(f"sudo grub-reboot {target}",shell=True)
            subprocess.run("sudo reboot",shell=True)
else:
    print("Cannot connect to wol server")

# systemctl enable systemd-networkd-wait-online.service