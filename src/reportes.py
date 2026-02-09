from __future__ import annotations
import json  
from dataclasses import asdict  
from typing import Any, Dict, List  
from src.modelos import Posicion
from src.portafolio import Portafolio

class ReportadorFinanciero:
    # 1) SRP (Single Responsibility): esta clase NO guarda datos
    # 2) Solo recibe un Portafolio y genera salidas (consola/archivos)

    def imprimir_resumen(self, portafolio: Portafolio) -> None:
        # 1) Validación: aseguramos que el argumento sea del tipo correcto
        if not isinstance(portafolio, Portafolio):
            raise TypeError("portafolio debe ser una instancia de Portafolio")

        # 2) Encabezado del reporte en consola
        print("===================================")
        print("  RESUMEN DEL PORTAFOLIO")
        print("===================================")

        # 3) Caso base: si no hay posiciones, no intentamos imprimir detalles
        if not portafolio.posiciones:
            print("No hay posiciones registradas.")
            return

        # 4) Recorremos cada posición y mostramos información clave
        for i, pos in enumerate(portafolio.posiciones, start=1):
            inst = pos.instrumento  # 4.1) Atajo al instrumento asociado a la posición
            print(f"{i}. {inst.ticker} | {inst.tipo} | {inst.sector}")
            print(f"   Cantidad: {pos.cantidad}")
            print(f"   Precio entrada: {pos.precio_entrada}")
            print("-----------------------------------")

    def exportar_json(self, portafolio: Portafolio, ruta: str) -> None:
        # 1) Convertimos el portafolio a una estructura serializable (dict/list)
        data = self._portafolio_a_dict(portafolio)

        # 2) Guardamos esa estructura en un archivo JSON
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def exportar_csv(self, portafolio: Portafolio, ruta: str) -> None:
        # 1) Import local: solo se usa aquí (evita cargar módulos innecesarios al importar la clase)
        import csv

        # 2) Creamos el archivo CSV y definimos sus columnas
        with open(ruta, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["ticker", "tipo", "sector", "cantidad", "precio_entrada"],
            )
            writer.writeheader()  # 2.1) Escribimos la fila de encabezados

            # 3) Por cada posición generamos una fila con los datos principales
            for pos in portafolio.posiciones:
                inst = pos.instrumento
                writer.writerow(
                    {
                        "ticker": inst.ticker,
                        "tipo": inst.tipo,
                        "sector": inst.sector,
                        "cantidad": pos.cantidad,
                        "precio_entrada": pos.precio_entrada,
                    }
                )

    def _portafolio_a_dict(self, portafolio: Portafolio) -> Dict[str, Any]:
        # 1) Armamos una lista de posiciones en formato "serializable" (dict)
        posiciones: List[Dict[str, Any]] = []

        # 2) Recorremos cada posición del portafolio
        for pos in portafolio.posiciones:
            inst = pos.instrumento

            # 3) Convertimos el instrumento:
            #    - Si es dataclass, usamos asdict(inst)
            #    - Si no, construimos el dict manualmente (más robusto)
            instrumento_dict = (
                asdict(inst)
                if hasattr(inst, "__dataclass_fields__")
                else {"ticker": inst.ticker, "tipo": inst.tipo, "sector": inst.sector}
            )

            # 4) Agregamos la posición como un diccionario
            posiciones.append(
                {
                    "instrumento": instrumento_dict,
                    "cantidad": pos.cantidad,
                    "precio_entrada": pos.precio_entrada,
                }
            )

        # 5) Devolvemos la estructura final del portafolio
