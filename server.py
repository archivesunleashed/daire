import os
from flask import Flask, jsonify, send_from_directory, abort
from backend.generator import loadHNSW, gen_random
app = Flask(__name__, static_folder='ui/build')

# Local Web Dev Allow CORS
from flask_cors import CORS
CORS(app)

# API
@app.route('/gen', methods=["GET"])
def generateImages():
    res = gen_random()
    # res = [{"distance":"0.0","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/9246f653502adc1f92e9581bb98eaafc.gif"},{"distance":"88.43506","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/691f7f5dd682ffa4569bb34585cbc9fd.jpg"},{"distance":"96.4041","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/3097c9b8913219e1afb94914f949639b.jpg"},{"distance":"97.8673","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/d7986a9d2350510356b16dfe8e65e2f2.jpg"},{"distance":"108.29394","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/2772617e2cec42a035a8e3b6cfdb4f1d.gif"},{"distance":"111.51843","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/8999f07d25fd359dfcd2a2e8febbda99.gif"},{"distance":"111.59082","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/c636bbdaa794ff1336763a2fbbff5708.gif"},{"distance":"112.23317","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/d47b6273b3a8fea966b43f26ac1c6480.jpg"},{"distance":"114.96908","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/43f30a8f97574ed030cf971f90045cae.gif"},{"distance":"115.18208","imgPath":"http://tuna.cs.uwaterloo.ca:5432/img/fe9019550742e4f88d4c237d1fa8c7db.gif"}]
    return jsonify(sample=res)


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
    # Development Mode
    # app.run(debug=True)
    # Production Mode
    app.run(host='0.0.0.0', port=5432)
