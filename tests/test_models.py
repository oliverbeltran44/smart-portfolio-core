# tests/test_models.py
import pytest
from src.modelos import Posicion, Instrumento
from tests.conftest import instrumento_test

@pytest.mark.parametrize(
    "precio_entrada, precio_actual, _cantidad, esperado",
    [
        (100, 150, 10, 500),
        (200, 180, 5, -100),
        (50, 50, 7, 0),
    ],
)
def test_calculo_pnl(
    precio_entrada,
    precio_actual,
    _cantidad,
    esperado,
    instrumento_test,
):
    posicion = Posicion(
        instrumento=instrumento_test,
        _cantidad=_cantidad,
        precio_entrada=precio_entrada,
    )

    pnl = posicion.calcular_ganancia_no_realizada(
        precio_actual=precio_actual
    )

    assert pnl == esperado

def test_posicion_cantidad_negativa_lanza_error(instrumento_test):
    with pytest.raises(ValueError):
        Posicion(instrumento=instrumento_test, _cantidad=-5, precio_entrada=100)

def test_posicion_cantidad_no_numerica_lanza_error(instrumento_test):
    with pytest.raises(TypeError):
        Posicion(instrumento=instrumento_test, _cantidad="cinco", precio_entrada=100)

def test_posicion_precio_entrada_no_numerico(instrumento_test):
    with pytest.raises(TypeError):
        Posicion(instrumento=instrumento_test, _cantidad=5, precio_entrada="cien")

def test_posicion_instrumento_invalido():
    with pytest.raises(TypeError):
        Posicion(instrumento="TSLA", _cantidad=5, precio_entrada=100) 

def test_calculo_pnl_precio_actual_invalido(instrumento_test):
    posicion = Posicion(instrumento=instrumento_test, _cantidad=5, precio_entrada=100)
    with pytest.raises(TypeError):
        posicion.calcular_ganancia_no_realizada(precio_actual="cien")

def test_calcular_valor_actual_precio_invalido(instrumento_test):
    posicion = Posicion(instrumento=instrumento_test, _cantidad=5, precio_entrada=100)
    with pytest.raises(TypeError):
        posicion.calcular_valor_actual(precio_mercado="cien")