# src/smart_portfolio/visualizacion.py
from yfinance_data import YahooFinanceClient
from modelos import Instrumento
import matplotlib.pyplot as plt

def graficar_tendencia(instrumento):
    hist = instrumento._history.copy()
    hist["t"] = range(len(hist))

    modelo = instrumento._modelo
    hist["trend"] = modelo.predict(hist["t"].values.reshape(-1, 1))

    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist["Close"], label="Precio real")
    plt.plot(hist.index, hist["trend"], label="Tendencia (Regresión)", linestyle="--")
    plt.title(f"Precio vs Tendencia — {instrumento.ticker}")
    plt.legend()
    plt.show()


