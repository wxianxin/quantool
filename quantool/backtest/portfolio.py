from typing import Dict
import logging

import event

# Setting up the logger
logger = logging.getLogger(__name__)


class Portfolio:
    """
    Tracks and manages current and historical positions.
    Calculates performance metrics and risk.
    Generates orders and decides the actual order size based on risk management rules.
    """

    def __init__(self, initial_cash: float = 100000.0):
        self.positions: Dict[str, int] = {}  # Tracks quantity for each symbol
        self.cash = initial_cash
        self.initial_cash = initial_cash    # TODO remove
        self.total_market_value = initial_cash
        self.filled_orders = []

    def _update_market_value(self):
        """
        Updates the total market value of the portfolio.
        """
        # TODO use market price
        # In a real-world scenario, this would involve multiplying the quantity of each position by its current price.
        # Here, for simplicity, we'll assume a dummy price 100.
        total_positions_value = sum(
            [qty * 100 for symbol, qty in self.positions.items()]
        )  # Dummy price = 100
        self.total_market_value = self.cash + total_positions_value

    def handle_fill(self, x: event.FillEvent):
        """
        Updates portfolio positions based on a FillEvent.
        """
        if x.direction == "BUY":
            self.positions[x.symbol] = self.positions.get(x.symbol, 0) + x.quantity
            self.cash -= x.fill_cost
        elif x.direction == "SELL":
            self.positions[x.symbol] = self.positions.get(x.symbol, 0) - x.quantity
            self.cash += x.fill_cost

        self._update_market_value()
        self.filled_orders.append(x)
        logger.info(
            f"Handled {x.direction} order for {x.symbol}: {x.quantity} @ {x.fill_cost / x.quantity:.2f}"
        )

    def generate_order(
        self, signal_event: event.SignalEvent, fixed_order_size: int
    ) -> event.OrderEvent:
        """
        Generates an OrderEvent based on a SignalEvent.
        """
        if signal_event.direction == "BUY":
            order = event.OrderEvent(
                signal_event.timestamp,
                signal_event.symbol,
                fixed_order_size,
                "BUY",
                signal_event.signal_price,
            )
        elif signal_event.direction == "SELL":
            order = event.OrderEvent(
                signal_event.timestamp,
                signal_event.symbol,
                fixed_order_size,
                "SELL",
                signal_event.signal_price,
            )
        logger.info(
            f"Generated {order.direction} order for {order.symbol}: {order.quantity}"
        )
        return order

    def calculate_performance(self) -> Dict[str, float]:
        """
        Calculates key performance metrics.
        For this example, we'll only calculate total returns.
        """
        total_return = (self.total_market_value - self.initial_cash) / self.initial_cash
        return {"Total Return": total_return}

    def __str__(self) -> str:
        return f"Portfolio(cash={self.cash:.2f}, total_market_value={self.total_market_value:.2f})"


if __name__ == "__main__":
    p = Portfolio()
