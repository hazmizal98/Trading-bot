import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        bot.on_bar_update(reqId, time, open_, high, low,
                          close, volume, wap, count)


class Bot:
    ib = None

    def __init__(self):
        self.ib = IBapi()
        self.ib.connect("127.0.0.1", 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        symbol = input("Enter the symbol you want to trade: ")
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])

        order = Order()
        order.orderType = "MKT"
        order.action = "BUY"
        quantity = 1
        order.totalQuantity = quantity

        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.primaryExchange = "ISLAND"
        contract.currency = "USD"

        self.ib.placeOrder(1, contract, order)

    def run_loop(self):
        self.ib.run()

    def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
        print(reqId)


bot = Bot()
