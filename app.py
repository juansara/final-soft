from flask import Flask, request, jsonify
from flask.testing import FlaskClient
from flask_cors import CORS
from datetime import date
import unittest

class Operacion:
    def __init__(self, destino, fecha, valor):
        self.numero_destino = destino
        self.fecha = fecha
        self.valor = valor

class Cuenta:
    def __init__(self, numero, nombre ,saldo, contactos):
        self.numero = numero
        self.saldo = saldo
        self.nombre = nombre
        self.contactos = contactos
        self.historial = {}
    
    def historial_rev(self):
        print(f"El saldo de {self.nombre} es de {self.saldo}")
        for key in self.historial:
            print(f"Para {key}: ", end="\n")
            for transa in self.historial[key]:
                print(transa)
                print("\n")

    def pagar(self, destino_numero, valor):
        if(valor > self.saldo):
            print("No tienes saldo suficiente")
        else:
            if destino_numero in self.contactos:
                opera = Operacion(destino_numero, date.today, valor)
                self.historial[destino_numero] = opera
            else:
                print("Tu contacto no existe")
                
    def get_contactos(self):
        return self.contactos

BaseDatos = []
BaseDatos.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
BaseDatos.append(Cuenta("123", "Luisa", 400, ["456"]))
BaseDatos.append(Cuenta("456", "Andrea", 300, ["21345"]))

app = Flask(__name__)
app.debug = True
CORS(app, origins=["https://127.0.0.1:8000"], max_age=10)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response


def recuperar_nombre(contactos, base_datos):
    arr = []
    for contacto in contactos:
        for cuenta in base_datos:
            if cuenta.numero == contacto:
                arr.append(f"{contacto} : {cuenta.nombre}")
                
    return arr

def aumentar_saldo(destino, valor, base_datos):
    res = 0
    for cuenta in base_datos:
        if destino == cuenta.numero:
            cuenta.saldo += valor
            res = cuenta
    return cuenta

@app.route("/billetera/contactos", methods=["GET"])
def get_contactos():
    numerito = request.args.get("minumero")
    
    for cuenta in BaseDatos:
        if cuenta.numero == numerito:
            cuenta_contactos = cuenta.get_contactos()
            gaa = recuperar_nombre(cuenta_contactos, BaseDatos)
            return jsonify({
                "Contactos":gaa,
            })

@app.route("/billetera/pagar", methods=["GET"])
def pagar_usuario():
    numerito = request.args.get("minumero")
    destino = request.args.get("numerodestino")
    valor = request.args.get("valor")
    
    for cuenta in BaseDatos:
        if cuenta.numero == numerito:
            if destino in cuenta.contactos:
                cuen = aumentar_saldo(destino, valor)
                return jsonify({
                    "result":cuen
                })
            else:
                return jsonify({
                    "result":"No existe contacto"
                })
    
@app.route("/billetera/historial", methods=["GET"])
def historial_usuario():
    numerito = request.args.get("minumero")
    BaseDatos = []
    BaseDatos.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
    BaseDatos.append(Cuenta("123", "Luisa", 400, ["456"]))
    BaseDatos.append(Cuenta("456", "Andrea", 300, ["21345"]))
    
    


if __name__ == "__main__":
    app.run(port=8000, debug=False)