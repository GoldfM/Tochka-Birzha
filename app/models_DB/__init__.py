from .users import User_db as User
from .balances import Balance_db as Balance
from .deposit import Deposit_db as Deposit
from .instruments import Instrument_db as Instrument
from .limit_orders import LimitOrder_db as LimitOrder
from .market_orders import MarketOrder_db as MarketOrder
from .order import OrderReq_db as OrderReq
from .orderbook import OrderBook_db as OrderBook
from .withdraw import Withdraw_db as Withdraw
from .transactions import Transaction_db as Transaction

# Все модели должны быть перечислены в __all__
__all__ = [
    'User',
    'Balance',
    'Deposit',
    'Instrument',
    'LimitOrder',
    'MarketOrder',
    'OrderReq',
    'OrderBook',
    'Withdraw',
    'Transaction'
]