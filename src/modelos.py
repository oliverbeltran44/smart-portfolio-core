from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True) ## Es un decorador inmutable, no se pueden modificar los atributos después de la creación. ##
class Activo_financiero:

    """Representa un activo financiero, inmutable."""

    Nombre_activo: str # Nombre o Sigla del Activo Financiero #
    Categoria: str     # Tipo de Activo Financiero #
    sector: str        # Sector economico al que pertenece el Activo Financiero #

    # No hay métodos adicionales. Por ser "frozen", no se pueden
    # modificar los atributos después de la creación. Python arrojará
    # dataclasses.FrozenInstanceError si intenta reasignar un campo.


@dataclass  # Es una clase de datos mutable, se pueden modificar los atributos después de la creación. #
class Posicion:
    """Representa una posición del activo financiero."""
    
    Activo: Activo_financiero # Instancia de Activo_financiero asociada a la posición #
    _cantidad: float  # atributo interno (prefijo _) para controlarlo vía property
    Precio_entrada: float     # Precio al que se adquirió el activo #

    def __post_init__(self) -> None:
        """Validación de atributos inicial.

        Se asegura de que el activo sea del tipo correcto

        """
        if not isinstance(self.Activo, Activo_financiero): # Regla de negocio: El activo debe ser del tipo correcto # 
            raise TypeError("Activo debe ser de tipo Activo_financiero")
        # Usa el setter de cantidad para validar el valor inicial
        self.cantidad = self._cantidad
        if not isinstance(self.Precio_entrada, (int, float)): # Regla de negocio: El precio de entrada debe ser numérico #
            raise TypeError("Precio_entrada debe ser numérico")

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

    def Valor_activo_actual(self, Precio_mercado: float) -> float: # Precio_mercado es un parámetro que representa el precio actual del activo financiero. #
        """Calcula el valor actual del activo financiero.
        """
        if not isinstance(Precio_mercado, (int, float)): # Regla de negocio: El precio de mercado debe ser numérico #
            raise TypeError("precio_mercado debe ser numérico")
        return self.cantidad * Precio_mercado
