from __future__ import annotations

import json  # Para exportar a JSON
from dataclasses import asdict  # Para convertir dataclasses a diccionarios
from typing import Any, Dict, List  # Para tipado
from .portafolio import Portafolio  # Import relativo desde src/ (misma carpeta)


class ReportadorFinanciero:
    # ==========================================================
    #  ReportadorFinanciero
    #  - SRP: Esta clase NO guarda datos.
    #  - Solo recibe un Portafolio y genera salidas:
    #       1) imprimir en consola
    #       2) exportar a JSON
    #       3) exportar a CSV
    # ==========================================================

    def imprimir_resumen(self, portafolio: Portafolio) -> None:
        # 1) Validación: asegurar que el objeto recibido sea un Portafolio
        if not isinstance(portafolio, Portafolio):
            raise TypeError("portafolio debe ser una instancia de Portafolio")

        # 2) Encabezado del reporte
        print("===================================")
        print("📊  RESUMEN DEL PORTAFOLIO")
        print("===================================")

        # 3) Caso base: si no hay posiciones, no imprimimos detalles
        if not portafolio.posiciones:
            print("No hay posiciones registradas.")
            return

        # 4) Recorremos las posiciones e imprimimos los datos principales
        for i, pos in enumerate(portafolio.posiciones, start=1):
            inst = pos.instrumento  # Acceso rápido al instrumento asociado a la posición

            # 4.1) Mostrar Instrumento (ticker, tipo, sector)
            print(f"{i}. {inst.ticker} | {inst.tipo} | {inst.sector}")

            # 4.2) Mostrar datos de la posición
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
        # 1) Import local: solo se usa aquí (buena práctica para no cargarlo siempre)
        import csv

        # 2) Abrimos el archivo CSV y escribimos encabezados y filas
        with open(ruta, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["ticker", "tipo", "sector", "cantidad", "precio_entrada"],
            )

            # 2.1) Escribimos el encabezado del CSV
            writer.writeheader()

            # 2.2) Escribimos una fila por cada posición
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
        # 1) Creamos una lista donde guardaremos cada posición como diccionario
        posiciones: List[Dict[str, Any]] = []

        # 2) Recorremos cada posición del portafolio
        for pos in portafolio.posiciones:
            inst = pos.instrumento

            # 3) Convertimos Instrumento a dict:
            #    - Si es dataclass, usamos asdict(inst)
            #    - Si no, lo construimos manualmente
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

        # 5) Devolvemos la estructura final del portafolio (lista de posiciones)
        return {"posiciones": posiciones}