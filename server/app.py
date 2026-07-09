from wol_lib import sendWolPackage
import flask,json,jwt
from datetime import datetime,timedelta

app = flask.Flask(__name__)
SECRET_KEY = "6550acc44f93f611270b414711fb6c06004603d60cb47f2b3910992c74396cce"
tokens = []
target = {}
okState = 0
errorState = 1
wrongToken = 2

with open("config.json","r") as f:
    data = json.load(f)

def checkToken():
    for token in tokens:
        payload = jwt.decode(token,SECRET_KEY,algorithms="HS256")
        if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
            tokens.remove(token)
    token = flask.request.headers.get("Authorization").replace("Bearer ","")
    if token not in tokens:
        print("token not in list")
        return False

def saveConfig():
    with open("config.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=1)

@app.route("/")
def index():
    return flask.render_template("index.html")

# 登录
@app.route("/api/auth",methods=["POST"])
def auth():
    username = flask.request.json.get("username")
    password_sha256 = flask.request.json.get("password")
    if password_sha256 == data["password"]:
        token = jwt.encode({"exp":datetime.utcnow()+timedelta(hours=2)},SECRET_KEY,algorithm="HS256")
        tokens.append(token)
        return {"state":okState,"token":token}
    else:
        return {"state":errorState}

# 获取实例列表
@app.route("/api/getinstances",methods=["GET"])
def getInstance():
    if not checkToken():
        return {"state":wrongToken}
    instances = {}
    for key in data["instances"]:
        instances[key] = data["instances"][key]["name"]
    return {"state":okState,"instances":instances}

# 新建实例
@app.route("/api/createinstance",methods=["POST"])
def createInstance():
    if not checkToken():
        return {"state":wrongToken}
    name = flask.request.json.get("name")
    mac = flask.request.json.get("mac")
    ip = flask.request.json.get("ip")
    id = -1
    for key in data["instances"]:
        id = max(int(key),id)
    id += 1
    data["instances"][str(id)] = {"name":name,"mac":mac,"ip":ip,"systems":[]}
    saveConfig()
    return {"state":okState}

# 删除实例
@app.route("/api/deleteinstance/<instance_id>",methods=["POST"])
def deleteInstance(instance_id:str):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    data["instances"].pop(instance_id)
    saveConfig()
    return {"state":okState}

# 获取某实例所安装的系统列表
@app.route("/api/getsystems/<instance_id>",methods=["GET"])
def getSystems(instance_id:str):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    return {"state":okState,"systems":list(data["instances"][instance_id]["systems"].keys())}

# 设置实例目标系统
@app.route("/api/setsystem/<instance_id>",methods=["POST"])
def setSystem(instance_id:str):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    os = flask.request.json.get("os")
    if os not in data["instances"][instance_id]["systems"]:
        return {"state":errorState}
    target[instance_id] = data["instances"][instance_id]["systems"][os]
    return {"state":okState}

# 唤醒实例
@app.route("/api/launch/<instance_id>",methods=["POST"])
def launchInstance(instance_id:str):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    ip = data["instances"][instance_id]["ip"]
    sendWolPackage(data["instances"][instance_id]["mac"],ip if ip is not None else "255.255.255.255")
    return {"state":okState}

# 获取实例状态
@app.route("/api/getinstancestate/<instance_id>",methods=["GET"])
def getInstanceState(instance_id:str):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    return {"state":0,"os":target[instance_id]}

# 关闭实例
@app.route("/api/shutdown/<instance_id>",methods=["POST"])
def shutdownInstance(instance_id:str):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    return {"state":1}

# 创建系统
@app.route("/api/createsystem/<instance_id>",methods=["POST"])
def createSystem(instance_id):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    system_name = flask.request.json.get("system_name")
    order = flask.request.json.get("order")
    if system_name in data["instances"][instance_id]["systems"]:
        return {"state":errorState}
    data["instances"][instance_id]["systems"]["system_name"] = order
    saveConfig()
    return {"state":okState}

# 删除系统
@app.route("/api/deletesystem/<instance_id>",methods=["POST"])
def deleteSystem(instance_id):
    if not checkToken():
        return {"state":wrongToken}
    if instance_id not in data["instances"]:
        return {"state":errorState}
    system_name = flask.request.json.get("system_name")
    if system_name not in data["instances"][instance_id]["systems"]:
        return {"state":errorState}
    data["instances"][instance_id]["systems"].remove(system_name)
    saveConfig()
    return {"state":okState}

# 获取目标系统
@app.route("/api/gettargetsystem/<instance_id>",methods=["GET"])
def getTargetSystem(instance_id):
    if instance_id not in data["instances"]:
        return {"state":errorState}
    target.pop(instance_id)
    return {"state":okState,"order":target[instance_id]}
    