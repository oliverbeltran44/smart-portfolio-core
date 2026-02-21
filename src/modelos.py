from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True) ## Es un decorador inmutable, no se pueden modificar los atributos después de la creación. ##
class Instrumento:

    """Representa un activo financiero, inmutable."""

    ticker: str # Nombre o Sigla del Activo Financiero #
    tipo: str     # Tipo de Activo Financiero #
    sector: str        # Sector economico al que pertenece el Activo Financiero #
    nombre: str


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

        """
        if not isinstance(self.instrumento, Instrumento): # Regla de negocio: El instrumento debe ser del tipo correcto # 
            raise TypeError("instrumento debe ser de tipo Instrumento")
        # Usa el setter de cantidad para validar el valor inicial
        self.cantidad = self._cantidad
        if not isinstance(self.precio_entrada, (int, float)): # Regla de negocio: El precio de entrada debe ser numérico #
            raise TypeError("precio_entrada debe ser numérico")

    @property # Decorador para definir un método como propiedad, permitiendo acceder a él como si fuera un atributo. #
    def cantidad(self) -> float:
        """Cantidad de unidades.
        """
        return self._cantidad # Devuelve el valor almacenado en el atributo _cantidad. #

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
        return self._cantidad * precio_mercado

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        if not isinstance(precio_actual, (int, float)):
            raise TypeError("precio_actual debe ser numérico")

        return (precio_actual - self.precio_entrada) * self._cantidad