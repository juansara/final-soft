from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date

class Operacion:
    def __init__(self, destino, valor ,fecha = date.today().isoformat(), tipo = None):
        self.numero_destino = destino
        self.fecha = fecha
        self.valor = valor
        self.tipo = tipo

class Cuenta:
    def __init__(self, numero, nombre ,saldo, contactos):
        self.numero = numero
        self.saldo = saldo
        self.nombre = nombre
        self.contactos = contactos
        self.historial = {}
    
    def historial_rev(self):
        historial = {"Enviado" : [], "Recibido": []}
        for key in self.historial:
            for operacion in self.historial[key]:
                if operacion.tipo == 'Enviado':
                    historial['Enviado'].append(f'Pago realizado de {operacion.valor} a {recuperar_by_numero(operacion.numero_destino)}')
                elif operacion.tipo == 'Recibido':
                    historial['Recibido'].append(f'Pago recibido de {operacion.valor} de {recuperar_by_numero(operacion.numero_destino)}')
                    
        return jsonify({
            f'Saldo de {self.nombre}' : self.saldo,
            "Operaciones" : historial
        })

    def pagar(self, destino_numero, valor):
        if(valor > self.saldo):
            return 'Saldo insuficiente'
        else:
            if str(destino_numero) in self.contactos:
                opera = Operacion(destino_numero, valor, tipo='Enviado')
                self.saldo -= valor
                if destino_numero not in list(self.historial.keys()):
                    self.historial[destino_numero] = [opera]
                else:
                    self.historial[destino_numero].append(opera)
                return f"Realizado en {opera.fecha}"
            else:
                return "No tienes el contacto guardado"
                
    def get_contactos(self):
        return self.contactos
    
    def actualizar_historial(self, destino ,operacion):
        if destino not in list(self.historial.keys()):
            self.historial[destino] = [operacion]
        else:
            self.historial[destino].append(operacion)

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

def actualizar_destino(destino, valor, numero_enviado):
    for cuenta in BaseDatos:
        if cuenta.numero == destino:
            cuenta.saldo += valor
            opera = Operacion(numero_enviado, valor, tipo='Recibido')
            cuenta.actualizar_historial(numero_enviado, opera)
    return "Exito"

def recuperar_by_numero(destino):
    for cuenta in BaseDatos:
        if cuenta.numero == destino:
            return str(cuenta.nombre)
        
def existe_usuario(BaseDatos, minumero):
    for usuario in BaseDatos:
        if usuario.numero == minumero:
            return True
        else:
            return False

@app.route("/billetera/contactos", methods=["GET"])
def get_contactos():
    numerito = request.args.get("minumero")
    
    for cuenta in BaseDatos:
        if cuenta.numero == numerito:
            cuenta_contactos = cuenta.get_contactos()
            gaa = recuperar_nombre(cuenta_contactos, BaseDatos)
            return jsonify({
                "Contactos":gaa,
                "Response":200
            })


@app.route("/billetera/pagar", methods=["GET"])
def pagar_usuario():
    numerito = request.args.get("minumero")
    destino = request.args.get("numerodestino")
    valor = int(request.args.get("valor"))
    
    for cuenta in BaseDatos:
        if cuenta.numero == numerito:
            ga = cuenta.pagar(destino, valor)
            #print(ga)
            if ga == f"Realizado en {date.today().isoformat()}":
                #print(ga)
                actualizar_destino(destino, valor, numerito)
                return jsonify({
                    "result": ga
                })
            else:
                return jsonify({
                    "result":"No se realizo la transaccion",
                    "motivo":ga
                })

@app.route("/billetera/historial", methods=["GET"])
def historial_usuario():
    numerito = request.args.get("minumero")
    existe_usuario_res = existe_usuario(BaseDatos, numerito)
    
    if existe_usuario_res:
        for cuenta in BaseDatos:
            if cuenta.numero == numerito:
                return cuenta.historial_rev()
    else:
        return jsonify({
            "result" : "No existe el historial del usuario solicitado"
        })
            
BaseDatos = []
BaseDatos.append(Cuenta("21345", "Arnaldo", 500, ["123", "456"]))
BaseDatos.append(Cuenta("123", "Luisa", 400, ["456"]))
BaseDatos.append(Cuenta("456", "Andrea", 300, ["21345"]))

if __name__ == "__main__":
    app.run(port=8000)