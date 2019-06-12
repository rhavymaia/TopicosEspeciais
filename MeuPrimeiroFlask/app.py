from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/olamundo")
def ola_mundo(nome):
    return ("Olá %s! Estou aprendendo Flask"%(nome), 200)

@app.route("/noticias/<categoria>")
def getNoticias(categoria):
    pass

@app.route("/usuario/<int:id>", methods=['GET'])
def getUsuario(id):
    usuarios = [{1: "João"}, {2: "Maria"}, {3: "José"}]
    for usuario in usuarios:
        if (id in usuario.keys()):
            print(usuario[id])
            return (usuario[id], 200)

@app.route("/json/usuario/<int:id>", methods=['GET'])
def getUsuarioJson(id):
    usuarios = [{1: "João"}, {2: "Maria"}, {3: "José"}, {4: "Antônio"}]
    for usuario in usuarios:
        if (id in usuario.keys()):
            return jsonify({id:usuario[id]})
    return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
