import os
from flask import send_file, request, Flask
from modules.pw_microsoft_learn import ms_learn


required_folders = {
    "export": "\\export"
}

app = Flask(__name__)
working_dir = str(os.path.dirname(os.path.abspath(__file__))) + required_folders["export"]

@app.route("/data")
def data():
    module = request.args.get("module")

    if module:
        save_location = ms_learn(module, working_dir)
        return send_file(save_location, mimetype="image/png")
    else:
        return f"ERROR: Invalid Module URL"
