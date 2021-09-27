from flask import send_file, request, Flask


app = Flask(__name__)


@app.route("/data")
def data():
    module = request.args.get("module")

    if module:
        return f"MODULE-URL: {module}"
    else:
        return f"ERROR: Invalid Module URL"

"""
def get_image():
    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(filename, mimetype='image/gif')
"""