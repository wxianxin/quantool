import numpy as np
from typing import Union


class Event:
    """
    Base class for all events.
    """

    pass


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding timestamp, symbol, and price.
    """

    def __init__(self, timestamp: np.datetime64, symbol: str, price: Union[float, int]):
        self.timestamp = timestamp
        self.symbol = symbol
        self.price = price

    def __str__(self) -> str:
        return f"MarketEvent({self.timestamp}, {self.symbol}, {self.price:.2f})"


class SignalEvent(Event):
    """
    Signals from a strategy with a timestamp, symbol, and direction.
    """

    def __init__(self, timestamp: np.datetime64, symbol: str, direction: str):
        self.timestamp = timestamp
        self.symbol = symbol
        assert direction in ["BUY", "SELL"], "Invalid direction"
        self.direction = direction

    def __str__(self) -> str:
        return f"SignalEvent({self.timestamp}, {self.symbol}, {self.direction})"


class OrderEvent(Event):
    """
    Represents a set of instructions to execute a trade.
    Contains a timestamp, symbol, quantity, and direction.
    """

    def __init__(
        self, timestamp: np.datetime64, symbol: str, quantity: int, direction: str
    ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.quantity = quantity
        assert direction in ["BUY", "SELL"], "Invalid direction"
        self.direction = direction

    def __str__(self) -> str:
        return f"OrderEvent({self.timestamp}, {self.symbol}, {self.quantity}, {self.direction})"


class FillEvent(Event):
    """
    Represents the filling of an order in the market.
    Contains a timestamp, symbol, quantity, direction, and the fill cost.
    """

    def __init__(
        self,
        timestamp: np.datetime64,
        symbol: str,
        quantity: int,
        direction: str,
        fill_cost: Union[float, int],
    ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.quantity = quantity
        assert direction in ["BUY", "SELL"], "Invalid direction"
        self.direction = direction
        self.fill_cost = fill_cost

    def __str__(self) -> str:
        return f"FillEvent({self.timestamp}, {self.symbol}, {self.quantity}, {self.direction}, {self.fill_cost:.2f})"
