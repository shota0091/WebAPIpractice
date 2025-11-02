from flask import Flask, jsonify, request,Response
import psutil, socket, datetime
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

@app.route("/helo",methods=["GET"])
def get_hello():
    try:
        return jsonify({"results": "OK"}), 200
    except Exception  as e:
        return error(e)

@app.route("/passParameter/<name>", methods=["GET"])
def get_passParameter(name):
    try:
        data = {
            "message": "パラメータを受け取りました",
            "received_name": name
        }
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        return Response(json_data, status=200, content_type="application/json; charset=utf-8")
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
        json_data = json.dumps(reqJsonItemList, ensure_ascii=False, indent=2)

        return Response(json_data, status=200, content_type="application/json; charset=utf-8")
    except Exception  as e:
        return error(e)

def error(e, status=500):
    return jsonify({
        "results": "NG",
        "error": str(e)
    }), status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
