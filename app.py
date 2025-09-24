from wol_lib import WOL_SEND
import flask,json

app = flask.Flask(__name__)

html = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WOL</title>
    <script>
        window.onload = function () {
            document.getElementsByClassName("btn")[0].onclick = function () {
                fetch("/wol/" + document.getElementsByClassName("input")[0].value).then(res => res.text()).then(data => {
                    alert(data);
                });
            }
        }
    </script>
</head>

<body>
    <input placeholder="password" class="input">
    <button class="btn">Click me</button>
</body>

</html>
'''

with open("password.json","r") as f:
    data = json.load(f)

@app.route("/")
def index():
    return html

@app.route("/wol/<password>")
def wol(password):
    if password == data["password"]:
        ws = WOL_SEND("255.255.255.255",data["mac"])
        ws.send_wol_package()
        return "OK"
    return "ERROR"