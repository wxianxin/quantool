import logging
import queue
from typing import Type

import datafeed
import event
import strategy
import portfolio
import execution

# Setting up the logger
logger = logging.getLogger(__name__)


class Engine:
    """
    The main backtest engine that drives the event loop and coordinates between the different modules.
    """

    def __init__(
        self,
        data_feed_class: Type[datafeed.DataFeed],
        strategy_class: Type[strategy.Strategy],
        portfolio_class: Type[portfolio.Portfolio],
        execution_handler_class: Type[execution.ExecutionHandler],
        args: dict = {
            "datafeed": {},
            "strategy": {},
            "portfolio": {"initial_cash": 100000.0},
        },
    ):
        self.events = queue.Queue()
        # TODO Use priority queue with timestamp in Event class to avoid priority issue

        # Initialize the various components
        self.data_feed = data_feed_class(**args["datafeed"])
        self.strategy = strategy_class(**args["strategy"])
        self.portfolio = portfolio_class(**args["portfolio"])
        self.execution_handler = execution_handler_class()

        logger.info("Engine initialized.")

    def _run_event_loop(self):
        """
        The main event loop that processes events.
        """
        self.events.put(next(self.data_feed.get_data()))
        while True:
            if not self.events.empty():
                x = self.events.get()

                if isinstance(x, event.MarketEvent):
                    # Handle market data and potentially generate signals
                    signal_event = self.strategy.generate_signal(x)
                    if signal_event:
                        print(signal_event)
                        self.events.put(signal_event)
                    # Queue the next MarketEvent for processing
                    next_market_event = next(self.data_feed.get_data(), None)
                    if next_market_event:
                        self.events.put(next_market_event)
                elif isinstance(x, event.SignalEvent):
                    # Determine order details and generate orders
                    order_event = self.portfolio.generate_order(x, fixed_order_size=100)
                    if order_event:
                        self.events.put(order_event)
                elif isinstance(x, event.OrderEvent):
                    # Simulate order execution and potentially generate fills
                    fill_event = self.execution_handler.execute_order(x, x.order_price)
                    if fill_event:
                        self.events.put(fill_event)
                elif isinstance(x, event.FillEvent):
                    # Update portfolio with fill details
                    self.portfolio.handle_fill(x)
            else:
                # No more events, exit the loop
                break

        logger.info("Backtest completed.")

    def run(self):
        """
        Starts the backtest.
        """
        logger.info("Starting backtest...")

        # Run the main event loop
        self._run_event_loop()


if __name__ == "__main__":
    engine = Engine(
        data_feed_class=datafeed.CSVDataFeed,
        strategy_class=strategy.MovingAverageCrossoverStrategy,
        portfolio_class=portfolio.Portfolio,
        execution_handler_class=execution.SimulatedExecutionHandler,
        args={
            "datafeed": {"csv_file": "/home/coupe/Downloads/AMD.csv"},
            "strategy": {},
            "portfolio": {"initial_cash": 100000.0},
        },
    )

    engine.run()
    print(engine.portfolio)
    print(engine.portfolio.positions)
    print(engine.portfolio.calculate_performance())
