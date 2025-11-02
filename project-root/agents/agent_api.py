from flask import Flask, jsonify, request,Response
import psutil, socket
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

@app.route("/helo",methods=["GET"])
def get_hello():
    try:
        data = {"results": "OK"}
        return complete(data)
    except Exception  as e:
        return error(e)

@app.route("/passParameter/<name>", methods=["GET"])
def get_passParameter(name):
    try:
        data = {
            "message": "パラメータを受け取りました",
            "received_name": name
        }
        return complete(data)
    except Exception  as e:
        return error(e)

@app.route("/queryTest",methods=["GET"])
def get_queryTest():
    try:
        name = request.args.get("name")
        age = request.args.get("age")
        data =[{"name":name,"age":age}]
        return complete(data)
    except Exception  as e:
        return error(e)


@app.route("/status", methods=["POST"])
def get_status():
    try:
        # JSON Bodyからリストを取得
        data = request.get_json(silent=True) or {}
        targetList = data.get("targetList", []) 
        reqJsonItemList = []
        for target in targetList:
            target_lower = target.lower()
            running = any((p.name() or "").lower() == target_lower for p in psutil.process_iter(["name"]))
            reqJsonItem = {
                "message":"Processチェックを実行",
                "hostname": socket.gethostname(),
                "process": target,
                "running": running
            }
            reqJsonItemList.append(reqJsonItem)
        return complete(reqJsonItemList)
    except Exception  as e:
        return error(e)

def complete(data, status=200):
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_data, status, content_type="application/json; charset=utf-8")

def error(e, status=500):
    data = { "results": "NG","error": str(e)}
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_data, status, content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
