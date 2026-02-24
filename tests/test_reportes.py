import pytest
from src.reportes import ReportadorFinanciero

class PosicionNoExisteError(Exception):
    pass

def test_imprimir_resumen_tipo_invalido():
    rep = ReportadorFinanciero()
    with pytest.raises(TypeError):
        rep.imprimir_resumen("no es un portafolio")

 
def test_imprimir_resumen_portafolio_vacio(portafolio_vacio, capsys):
    rep = ReportadorFinanciero()
    rep.imprimir_resumen(portafolio_vacio)
    salida = capsys.readouterr().out
    assert "No hay posiciones registradas." in salida

from src.modelos import Posicion
 
def test_imprimir_resumen_con_posiciones(portafolio_vacio, instrumento_test, capsys):
    rep = ReportadorFinanciero()
    pos = Posicion(instrumento=instrumento_test, cantidad=3, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
    rep.imprimir_resumen(portafolio_vacio)
    salida = capsys.readouterr().out
    assert "TSLA" in salida
    assert "Cantidad: 3" in salida

import json
import os
 
def test_exportar_json(tmp_path, portafolio_vacio, instrumento_test):
    rep = ReportadorFinanciero()
    pos = Posicion(instrumento=instrumento_test, cantidad=2, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
    ruta = tmp_path / "reporte.json"
    rep.exportar_json(portafolio_vacio, ruta)
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["posiciones"][0]["instrumento"]["ticker"] == "TSLA"

import csv
 
def test_exportar_csv(tmp_path, portafolio_vacio, instrumento_test):
    rep = ReportadorFinanciero()
    pos = Posicion(instrumento=instrumento_test, cantidad=1, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
    ruta = tmp_path / "reporte.csv"
    rep.exportar_csv(portafolio_vacio, ruta)
    with open(ruta, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)
    assert filas[0]["ticker"] == "TSLA"
    assert filas[0]["cantidad"] == "1"