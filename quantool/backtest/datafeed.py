import numpy as np
import abc
from typing import Union, Iterator

import event


class DataFeed(abc.ABC):
    """Abstract class
    * Provides the latest market data.
    * Can handle multiple data sources: CSV, databases, live data feeds, etc.
    """

    @abc.abstractmethod
    def get_data(self) -> Iterator[Union[None, event.MarketEvent]]:
        pass


class CSVDataFeed(DataFeed):
    """
    Data feed that loads market data from a CSV file.
    Assumes the CSV has columns: 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'
    """

    def __init__(self, csv_file: str):
        self.epoch_timestamp = np.datetime64("1970-01-01T00:00:00")
        self.data = self._load_data(csv_file)
        self.current_index = 0
        self.symbol = csv_file.split("/")[-1][:-4]

    def _load_data(self, csv_file: str) -> np.array:
        """
        Loads the CSV data into a pandas DataFrame.
        """
        converter = {0: lambda x: np.datetime64(x) - self.epoch_timestamp}
        arr = np.loadtxt(
            csv_file, delimiter=",", converters=converter, skiprows=1, dtype=float
        )
        arr = arr[arr[:, 0].argsort()]  # Ensure data is sorted by date
        return arr

    def get_data(self):
        """
        Yields the next data point as a MarketEvent.
        If no more data is available, it returns None.
        """
        while self.current_index < len(self.data):
            row = self.data[self.current_index]
            self.current_index += 1
            yield event.MarketEvent(row[0], self.symbol, row[5])
        yield None


if __name__ == "__main__":
    feed = CSVDataFeed("/home/coupe/Downloads/AMD.csv")
    for x in feed.get_data():
        print(x)
