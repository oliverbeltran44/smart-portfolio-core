from dataclasses import dataclass, field
<<<<<<< HEAD
from typing import List, Dict
from modelos import Posicion, Instrumento

@dataclass
class Portafolio:
    # posiciones: lista con todas las posiciones que componen el portafolio
    # (cada Posicion representa una inversión/tenencia concreta)
    posiciones: List[Posicion] = field(default_factory=list)
=======
from typing import List
from modelos import Posicion, Instrumento
>>>>>>> 175bd40da8d7c13b7171b91d9bb60854261e2b02

@dataclass(frozen=True) ## Es un decorador inmutable, no se pueden modificar los atributos después de la creación. ##
class Instrumento:

    """Representa un activo financiero, inmutable."""

    Ticker: str # Nombre o Sigla del Activo Financiero #
    Tipo: str     # Tipo de Activo Financiero #
    sector: str        # Sector economico al que pertenece el Activo Financiero #

    # No hay métodos adicionales. Por ser "frozen", no se pueden
    # modificar los atributos después de la creación. Python arrojará
    # dataclasses.FrozenInstanceError si intenta reasignar un campo.


@dataclass  # Es una clase de datos mutable, se pueden modificar los atributos después de la creación. #
class Posicion:
    """Representa una posición del activo financiero."""
    
    instrumento: Instrumento # Instancia de Instrumento asociada a la posición #
    _cantidad: float  # atributo interno (prefijo _) para controlarlo vía property
    precio_entrada: float     # Precio al que se adquirió el activo #

    def __post_init__(self) -> None:
        """Validación de atributos inicial.

        Se asegura de que el instrumento sea del tipo correcto

<<<<<<< HEAD
    def posiciones_por_ticker(self) -> Dict[str, List[Posicion]]:
        # agrupadas: mapa {ticker: [posiciones...]} para analizar exposición por instrumento
        agrupadas: Dict[str, List[Posicion]] = {}
=======
        """
        if not isinstance(self.instrumento, Instrumento): # Regla de negocio: El instrumento debe ser del tipo correcto # 
            raise TypeError("instrumento debe ser de tipo Instrumento")
        # Usa el setter de cantidad para validar el valor inicial
        self.cantidad = self._cantidad
        if not isinstance(self.precio_entrada, (int, float)): # Regla de negocio: El precio de entrada debe ser numérico #
            raise TypeError("precio_entrada debe ser numérico")
>>>>>>> 175bd40da8d7c13b7171b91d9bb60854261e2b02

    @property # Decorador para definir un método como propiedad, permitiendo acceder a él como si fuera un atributo. #
    def cantidad(self) -> float:
        """Cantidad de unidades.
        """
        return self._cantidad # Devuelve el valor almacenado en el atributo _cantidad. #

<<<<<<< HEAD
            # Se agrega la posición al grupo correspondiente
            agrupadas.setdefault(clave, []).append(pos)

        # Se devuelve como dict normal (más cómodo para serializar/mostrar)
        return agrupadas
=======
    @cantidad.setter # Decorador para definir el método como setter de la propiedad cantidad. #
    def cantidad(self, value: float) -> None:
        if not isinstance(value, (int, float)): # Regla de negocio: La cantidad debe ser un número #
            raise TypeError("cantidad debe ser numérica")
        if value < 0: # Regla de negocio: La cantidad no puede ser negativa #
            raise ValueError("cantidad no puede ser negativa")
        self._cantidad = float(value)

    def calcular_valor_actual(self, precio_mercado: float) -> float: # Precio_mercado es un parámetro que representa el precio actual del activo financiero. #
        """Calcula el valor actual del activo financiero.
        """
        if not isinstance(precio_mercado, (int, float)): # Regla de negocio: El precio de mercado debe ser numérico #
            raise TypeError("precio_mercado debe ser numérico")
        return self.cantidad * precio_mercado
>>>>>>> 175bd40da8d7c13b7171b91d9bb60854261e2b02
