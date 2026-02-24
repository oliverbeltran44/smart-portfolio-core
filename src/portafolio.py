from dataclasses import dataclass, field
from typing import List, Dict
from src.modelos import Posicion, Instrumento, PosicionNoExisteError

@dataclass
class Portafolio:
    posiciones: List[Posicion] = field(default_factory=list)
 
    def agregar_posicion(self, posicion: Posicion) -> None:
        if not isinstance(posicion, Posicion):
            raise TypeError("Solo se pueden agregar objetos de tipo Posicion")
        self.posiciones.append(posicion)
 
    def valor_total(self, precios_mercado: Dict[str, float]) -> float:
        if not isinstance(precios_mercado, dict):
            raise TypeError("precios_mercado debe ser un diccionario {ticker: precio}")
 
        total = 0.0
        for pos in self.posiciones:
            ticker = pos.instrumento.ticker
            try:
                precio = precios_mercado[ticker]
            except KeyError as e:
                raise KeyError(f"Falta precio de mercado para el ticker '{ticker}'") from e
 
            total += pos.calcular_valor_actual(precio)
 
        return total
 
    def posiciones_por_ticker(self) -> Dict[str, List[Posicion]]:
        agrupadas = {}
        for pos in self.posiciones:
            clave = pos.instrumento.ticker
            agrupadas.setdefault(clave, []).append(pos)
        return agrupadas
 
    def remover_posicion(self, ticker: str):
        for pos in self.posiciones:
            if pos.instrumento.ticker == ticker:
                self.posiciones.remove(pos)
                return
        raise PosicionNoExisteError(f"No existe posición con ticker {ticker}")