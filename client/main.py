import requests,json,time
import subprocess

with open("config.json","r") as f:
    data = json.load(f)

flag = False
attempt_times = 0
while not flag and attempt_times < data["attempt"]:
    try:
        attempt_times += 1
        res = requests.get(f"http://{data['server']}/api/gettargetsystem/{data['instance_id']}")
        res_data = res.json()
        flag = True
    except:
        print(f"Network is unreachable, retry in {data['attempt_second']}s({attempt_times})")
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
            print("already in this target system")
    else:
        print("no target")
else:
    print("Cannot connect to wol server")

# systemctl enable systemd-networkd-wait-online.service