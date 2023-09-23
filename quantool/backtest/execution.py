import abc
import logging
from typing import Optional

import event

# Setting up the logger
logger = logging.getLogger(__name__)


class ExecutionHandler(abc.ABC):
    """
    Abstract class representing an execution handler.
    * Sends orders to the market and receives fill confirmations.
    * Can simulate slippage, transaction costs, and other execution-related factors.
    * In a live trading system, this component would interface with a brokerage.
    """

    @abc.abstractmethod
    def execute_order(self, order_event: event.OrderEvent) -> Optional[event.FillEvent]:
        """
        Executes an OrderEvent and returns a corresponding FillEvent.
        If the order cannot be executed, returns None.
        """
        pass


class SimulatedExecutionHandler(ExecutionHandler):
    """
    Simulates the execution of orders.
    Assumes that all orders are filled at the next available price.
    """

    def execute_order(
        self, order_event: event.OrderEvent, fill_price: float
    ) -> Optional[event.FillEvent]:
        """
        Simulates order execution by creating a corresponding FillEvent.
        """
        fill_cost = (
            order_event.quantity * fill_price
        )  # Using a dummy price of 100 for simplicity
        fill_event = event.FillEvent(
            order_event.timestamp,
            order_event.symbol,
            order_event.quantity,
            order_event.direction,
            fill_cost,
        )
        logger.info(
            f"Executed {order_event.direction} order for {order_event.symbol}: {order_event.quantity} @ {fill_cost / order_event.quantity:.2f}"
        )
        return fill_event
