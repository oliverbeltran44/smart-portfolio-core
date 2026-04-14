# src/smart_portfolio/cli.py
from yfinance_data import YahooFinanceClient
from modelos import Instrumento
from modelos import Posicion
from json_storage import guardar_portafolio
from visualizacion import graficar_tendencia

def main():
    print("SMART PORTFOLIO ORACLE ---\n")

    ticker = input("Ingrese Ticker: ").upper()

    data_client = YahooFinanceClient()
    instrumento = Instrumento(ticker, data_client)

    print("\nObteniendo datos ... OK")
    precio_actual = data_client.obtener_precio_actual(ticker)

    print("Entrenando modelo ... OK")
    pred_7 = instrumento.predecir_precio(7)

    print(f"\n{ticker}")
    print(f"Precio actual: ${precio_actual:.2f}")
    print(f"Predicción 7 días: ${pred_7:.2f}")

    # ✔ PRIMERO se pregunta
    ver_grafica = input("\n¿Ver gráfica de tendencia? (s/n): ").strip().lower()

    # ✔ LUEGO se evalúa
    if ver_grafica == "s":
        graficar_tendencia(instrumento)

    comprar = input("\n¿Comprar? (s/n): ").strip().lower()

    if comprar == "s":
        cantidad = int(input("Cantidad: "))
        posicion = Posicion(ticker, cantidad, precio_compra=precio_actual)

        alerta = posicion.alerta_riesgo(precio_actual)
        data = {
            "ticker": ticker,
            "precio_actual": precio_actual,
            "prediccion_7_dias": pred_7,
            "cantidad": cantidad,
            "alerta_riesgo": alerta,
        }

        guardar_portafolio(data)
        print("\nGuardado en portafolio.json")
    else:
        print("\nOperación cancelada.")


if __name__ == "__main__":
    main()
