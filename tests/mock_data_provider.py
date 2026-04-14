class MockMarketDataProvider:

    def obtener_precio_actual(self, ticker: str) -> float:
        return 100.0

    def obtener_historia(self, ticker: str, dias: int):
        import pandas as pd

        return pd.DataFrame({
            "Close": [100, 101, 102]
        })

mock = MockMarketDataProvider()

print(mock.obtener_precio_actual("AAPL"))
print(mock.obtener_historia("AAPL", 3))
##listo