from models import User, Instrument, OrderBook, Transaction, Level
from typing import Dict, List


instruments_history: List[Instrument] = [
    Instrument(name="BTC", ticker="Bytcoin"),
    Instrument(name="ETH", ticker="Etherium"),
]


transactions_history: Dict[str, List[Transaction]] = {
    "BTC": [
        Transaction(ticker="BTC", amount=20, price=20000, timestamp="2025-05-30"),
        Transaction(ticker="BTC", amount=30, price=30000, timestamp="2025-05-30"),
    ],
    "ETH": [
        Transaction(ticker="ETH", amount=10, price=1000, timestamp="2025-05-30"),
    ],
}

orderbooks_history: Dict[str, OrderBook] = {
    "ETH":
        OrderBook(
        buy_levels=[Level(price=500, qty=5)],
        sell_levels=[Level(price=600, qty=5), Level(price=400, qty=3)],
    ),
    "BTC":
        OrderBook(
        buy_levels=[Level(price=30000, qty=1), Level(price=35000, qty=10)],
        sell_levels=[Level(price=67000, qty=5)],
    ),
}


balances_history: Dict[str, Dict[str, int]] = {}
users_history: Dict[int, User] = {}

def generate_user_id() -> str:
    if users_history:
        return str(max([int(k) for k in users_history.keys()]) + 1)
    else:
        return "1"