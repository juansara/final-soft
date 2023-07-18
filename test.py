import unittest
from flask import Flask, request, jsonify

from app import get_contactos, pagar_usuario, historial_usuario

class Testing(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        
    #CASO DE ACIERTO: VERIFICA SI TU LISTA DE CONTACTOS ES LA INDICADA
    def test_get_contactos(self):
        with self.app.test_request_context("billetera/contactos?minumero=21345", method='GET'):
            response = get_contactos()
            
            respuesta_esperada = {
                "Contactos":["123 : Luisa", "456 : Andrea"],
                "Response": 200
            }
            
            self.assertEqual(response.get_json(), respuesta_esperada)
            
    #CASO DE FALLO: VERIFICA SI TU SALDO ES SUFICIENTE
    def test_saldo_insuficiente_pagar(self):
        with self.app.test_request_context("billetera/pagar?minumero=21345&numerodestino=123&valor=700", method='GET'):
            response = pagar_usuario()
            
            respuesta_esperada = {
                "result":"No se realizo la transaccion",
                "motivo":"Saldo insuficiente"
            }
            
            self.assertEqual(response.get_json(), respuesta_esperada)
            
    #CASO DE FALLO: VERIFICA SI EL CONTACTO, AL QUE LE VAS A PAGAR, EXISTE      
    def test_no_contacto_pagar(self):
        with self.app.test_request_context("billetera/pagar?minumero=21345&numerodestino=777&valor=200", method='GET'):
            response = pagar_usuario()
            
            respuesta_esperada = {
                "motivo":'No tienes el contacto guardado'
            }
            
            self.assertEqual(response.get_json()["motivo"], respuesta_esperada['motivo'])
            
    #CASO DE FALLO: VERIFICA SI EL HISTORIAL DEL NUMERO BRINDADO EXISTE
    def test_no_existe_historial_para_el_numero(self):
        with self.app.test_request_context('billetera/historial?minumero=888', method='GET'):
            response = historial_usuario()
            
            respuesta_esperada = {
                "result" : "No existe el historial del usuario solicitado"
            }
            
            self.assertEqual(response.get_json(), respuesta_esperada)
            
if __name__ == '__main__':
    unittest.main()