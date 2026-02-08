from dataclasses import dataclass, field
from typing import List, Dict
from modelos import Posicion, Instrumento

@dataclass
class Portafolio:
    # posiciones: lista con todas las posiciones que componen el portafolio
    # (cada Posicion representa una inversión/tenencia concreta)
    posiciones: List[Posicion] = field(default_factory=list)

    def agregar_posicion(self, posicion: Posicion) -> None:
        # posicion: objeto Posicion a agregar al portafolio
        if not isinstance(posicion, Posicion):
            raise TypeError("Solo se pueden agregar objetos de tipo Posicion")

        # Agrega la posición al final de la lista
        self.posiciones.append(posicion)

    def valor_total(self, precios_mercado: Dict[str, float]) -> float:
        # precios_mercado: mapa {Ticker: precio_actual} usado para valorar cada posición
        if not isinstance(precios_mercado, dict):
            raise TypeError("precios_mercado debe ser un diccionario {Ticker: precio}")

        # total: acumulador del valor de mercado del portafolio completo
        total: float = 0.0

        for pos in self.posiciones:
            # ticker: identificador del instrumento asociado a la posición (ej: 'AAPL')
            Ticker: str = pos.instrumento.ticker

            # precio: precio de mercado para el ticker de esta posición
            # (si falta, no se puede valorar la posición)
            try:
                precio: float = precios_mercado[Ticker]
            except KeyError as e:
                raise KeyError(f"Falta precio de mercado para el ticker '{Ticker}'") from e

            # Se suma el valor actual de la posición usando el precio encontrado
            total += pos.calcular_valor_actual(precio)

        return total

    def posiciones_por_ticker(self) -> Dict[str, List[Posicion]]:
        # agrupadas: mapa {ticker: [posiciones...]} para analizar exposición por instrumento
        agrupadas: Dict[str, List[Posicion]] = {}

        for pos in self.posiciones:
            # clave: ticker del instrumento de la posición actual
            clave: str = pos.instrumento.ticker

            # Se agrega la posición al grupo correspondiente
            agrupadas.setdefault(clave, []).append(pos)

        # Se devuelve como dict normal (más cómodo para serializar/mostrar)
        return agrupadas
    
    ## Oliver
