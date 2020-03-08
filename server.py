from flask_cors import CORS
import os
from flask import Flask, jsonify, send_from_directory, abort, request
from backend.generator import loadMetadata, loadHNSW, gen_random
app = Flask(__name__, static_folder='ui/build')

# Local Web Dev Allow CORS
CORS(app)

# API
@app.route('/gen/', defaults={'path': None})
@app.route('/gen', defaults={'path': None})
@app.route('/gen/<path:path>', methods=["GET"])
def generateImages(path):
    print(f'[generateImages]', path)
    pageNumber = request.args.get('pageNumber', default=1, type=int)
    srcImage, res = gen_random(path, pageNumber)
    if res is False:
        return abort(404)
    else:
        return jsonify(sample=res, srcImage=srcImage)


# Serve React App
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serveReact(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/img', defaults={'path': ''})
@app.route('/img/<path:path>')
def serveImages(path):
    print(path)
    if path != "" and os.path.exists('img' + '/' + path):
        return send_from_directory('img', path)
    else:
        return abort(404)


# Trigger Server
if __name__ == '__main__':
    # Preparation
    loadHNSW()
    loadMetadata()
    # Production Mode
    app.run(
        host='0.0.0.0',
        port=5432,
        # debug=True  # Development Mode
    )
