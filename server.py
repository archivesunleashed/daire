import os
from flask import Flask, jsonify, send_from_directory
from backend.preprocess import preprocess, gen_random
app = Flask(__name__, static_folder='ui/build')

# API
@app.route('/gen', methods=["GET"])
def generateImages():
    print('Gen', gen_random())
    return jsonify(isReady=True)


# Serve React App
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


# Trigger Server
if __name__ == '__main__':
    # Pre-processing
    preprocess()
    # Development Mode
    app.run(debug=True)
    # Production Mode
    # app.run(host='0.0.0.0', port=8080)
