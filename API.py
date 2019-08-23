from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor':'DS18B20', 'variable':'Temperatura ambiente', 'unidades': 'Centigrados Fahrenheit'}

mediciones = [
    {'fecha': '2019-08-22 13:22:43', **tipo_medicion, 'valor': 11},
    {'fecha': '2019-08-22 18:24:00', **tipo_medicion, 'valor': 52},
    {'fecha': '2019-08-22 20:35:15', **tipo_medicion, 'valor': 78},
    {'fecha': '2019-08-22 20:42:55', **tipo_medicion, 'valor': 24},
    {'fecha': '2019-08-23 00:15:10', **tipo_medicion, 'valor': 25},
    {'fecha': '2019-08-23 03:30:36', **tipo_medicion, 'valor': 12},
    {'fecha': '2019-08-24 09:41:28', **tipo_medicion, 'valor': 77}
]

@app.route('/mediciones', methods=['POST'])
def postOne():
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    return jsonify(mediciones)
    
@app.route('/mediciones/<porcentaje>', methods=['GET'])
def getMayores(porcentaje):
    cantidad = len(mediciones) * float(porcentaje)
    lista = sorted(mediciones, key = lambda medicion: medicion['valor'])
    lista = lista[len(lista)-int(cantidad)-1:]

    return jsonify(lista)

@app.route('/')
def get():
    return jsonify(tipo_medicion)

@app.route('/mediciones', methods = ['GET'])
def getAll():
    return jsonify(mediciones)

"""@app.route('/mediciones/media', methods = ['GET'])
def getMedia():
    media = 0
    for medicion in mediciones:
        media += medicion['valor']
    return jsonify(media/int(len(mediciones))) """

@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteOne(fecha):
    x = False
    for medicion in mediciones:
        if (fecha in medicion['fecha']):
            x = True
            mediciones.remove(medicion)
    return 'Eliminado' if x else 'No Encontrado'

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha):
    body = request.json
    x = False
    for medicion in mediciones:
        if(fecha in medicion['fecha']):
            x = True
            medicion['valor'] = body['valor']
    return 'Modificado' if x else 'No Encontrado'

app.run(port = 5000, debug = True)