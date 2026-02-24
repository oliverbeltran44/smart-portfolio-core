import pytest
from src.portafolio import Portafolio, PosicionNoExisteError
from src.modelos import Posicion

def test_agregar_posicion_tipo_invalido(portafolio_vacio):
    with pytest.raises(TypeError):
        portafolio_vacio.agregar_posicion("no es una posición")

def test_agregar_posicion(portafolio_vacio, instrumento_test):
    pos = Posicion(instrumento=instrumento_test, _cantidad=5, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
 
    assert len(portafolio_vacio.posiciones) == 1
    assert portafolio_vacio.posiciones[0].instrumento.ticker == "TSLA"

def test_remover_posicion_existente(portafolio_vacio, instrumento_test):
    pos = Posicion(instrumento=instrumento_test, _cantidad=1, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
 
    portafolio_vacio.remover_posicion("TSLA")
 
    assert len(portafolio_vacio.posiciones) == 0

def test_remover_posicion_inexistente(portafolio_vacio):
    with pytest.raises(PosicionNoExisteError):
        portafolio_vacio.remover_posicion("AAPL")

def test_valor_total(portafolio_vacio, instrumento_test):
    pos = Posicion(instrumento=instrumento_test, _cantidad=2, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
 
    precios = {"TSLA": 150}
    total = portafolio_vacio.valor_total(precios)
 
    assert total == pytest.approx(300)

def test_valor_total_falta_precio(portafolio_vacio, instrumento_test):
    pos = Posicion(instrumento=instrumento_test, _cantidad=1, precio_entrada=100)
    portafolio_vacio.agregar_posicion(pos)
 
    with pytest.raises(KeyError):
        portafolio_vacio.valor_total({})

def test_posiciones_por_ticker(portafolio_vacio, instrumento_test):
    pos1 = Posicion(instrumento=instrumento_test, _cantidad=1, precio_entrada=100)
    pos2 = Posicion(instrumento=instrumento_test, _cantidad=2, precio_entrada=120)
 
    portafolio_vacio.agregar_posicion(pos1)
    portafolio_vacio.agregar_posicion(pos2)
 
    agrupadas = portafolio_vacio.posiciones_por_ticker()
 
    assert "TSLA" in agrupadas
    assert len(agrupadas["TSLA"]) == 2