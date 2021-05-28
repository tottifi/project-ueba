import os
from flask import Flask
from flask import jsonify
from locFinder import handleNewIp
app = Flask(__name__)


@app.route('/<id>/<ip>', methods=['GET'])
def test_ip(id, ip):
    try:
        location, known = handleNewIp(id, ip)
        return jsonify(city=location[0], country=location[1], known=known)
    except Exception as e:
        print(e)
        return 500


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), debug=False)
