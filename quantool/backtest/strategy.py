import abc
import typing
import logging
from collections import deque
import numpy as np

import event

# Setting up the logger
logger = logging.getLogger(__name__)


class Strategy(abc.ABC):
    """
    Abstract class representing a trading strategy.
    All strategy implementations should inherit from this class and implement its methods.
    """

    @abc.abstractmethod
    def generate_signal(
        self, event: event.MarketEvent
    ) -> typing.Optional[event.SignalEvent]:
        """
        Processes a MarketEvent to generate a SignalEvent if a trading signal is triggered.
        Returns None if no signal is generated.
        """
        pass


class MovingAverageCrossoverStrategy(Strategy):
    """
    Simple moving average crossover strategy.
    Generates a BUY signal when the short moving average crosses above the long moving average,
    and a SELL signal when the short moving average crosses below the long moving average.
    """

    def __init__(self, short_window: int = 40, long_window: int = 100):
        self.short_window = short_window
        self.long_window = long_window
        self.short_deque = deque((), maxlen=short_window)
        self.long_deque = deque((), maxlen=long_window)
        self.short_sum = 0
        self.long_sum = 0
        self.current_short_sma = 0
        self.current_long_sma = 0
        self.prev_short_sma = 0
        self.prev_long_sma = 0
        self.data = np.array(())
        logger.info(
            f"Initialized MovingAverageCrossoverStrategy with short_window={short_window} and long_window={long_window}"
        )

    def update_averages(self, new_value):
        """
        Compute short and long moving averages.
        """

        if len(self.short_deque) == self.short_window:
            self.short_sum -= self.short_deque[0]
        self.short_deque.append(new_value)
        self.short_sum += new_value

        if len(self.short_deque) < self.short_window:
            self.prev_short_sma = np.nan
            self.current_short_sma = np.nan
        else:
            self.prev_short_sma = self.current_short_sma
            self.current_short_sma = self.short_sum / self.short_window

        if len(self.long_deque) == self.long_window:
            self.long_sum -= self.long_deque[0]
        self.long_deque.append(new_value)
        self.long_sum += new_value

        if len(self.long_deque) < self.long_window:
            self.prev_long_sma = np.nan
            self.current_long_sma = np.nan
        else:
            self.prev_long_sma = self.current_long_sma
            self.current_long_sma = self.long_sum / self.long_window

        return None

    def generate_signal(
        self, x: event.MarketEvent
    ) -> typing.Optional[event.SignalEvent]:
        """
        Process a MarketEvent to generate a SignalEvent if a trading signal is triggered.
        """
        if x is None:
            return None
        self.data = np.concatenate(
            (self.data, np.array((x.timestamp, x.price))), axis=0
        )
        if len(self.data) < self.long_window:
            return None

        self.update_averages(x.price)

        if self.current_short_sma > self.current_long_sma and self.prev_short_sma <= self.prev_long_sma:
            print("BUY")
            logger.info(f"Generated BUY signal on {x.timestamp}")
            return event.SignalEvent(x.timestamp, x.symbol, "BUY")
        elif self.current_short_sma < self.current_long_sma and self.prev_short_sma >= self.prev_long_sma:
            print("SELL")
            logger.info(f"Generated SELL signal on {x.timestamp}")
            return event.SignalEvent(x.timestamp, x.symbol, "SELL")

        return None


if __name__ == "__main__":
    import datafeed

    feed = datafeed.CSVDataFeed("/home/coupe/Downloads/TSLA.csv")
    sma = MovingAverageCrossoverStrategy(short_window=40, long_window=100)
    for x in feed.get_data():
        sma.generate_signal(x)
