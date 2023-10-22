"""
TODO!!!
To integrate this with the other modules:

    Data Collection: Modify the Portfolio module to store historical values, trades, and other metrics of interest.
    Execution: After running the backtest, create an instance of BacktestVisualizer and call the desired visualization methods.
---
Separation of Concerns: The visualization module should focus only on presenting data. It should not modify or compute data but rather receive prepared data from other modules.
Integration Points: Identify the data from other modules that you'd like to visualize. Common visualizations include:

    Equity curve
    Drawdowns
    Returns over time
    Position sizes and exposures
    Order and fill events on price charts
"""

import matplotlib.pyplot as plt


class BacktestVisualizer:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def plot_equity_curve(self):
        """
        Plots the equity curve based on the portfolio's historical values.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(
            self.portfolio.historical_values["timestamp"],
            self.portfolio.historical_values["value"],
            label="Equity Curve",
        )
        plt.title("Equity Curve")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_drawdowns(self):
        """
        Plots drawdowns over time.
        """
        # Assuming the portfolio module calculates drawdowns and stores them in a list or DataFrame
        drawdowns = self.portfolio.calculate_drawdowns()

        plt.figure(figsize=(10, 6))
        plt.plot(drawdowns["timestamp"], drawdowns["drawdown"], label="Drawdown")
        plt.title("Drawdowns")
        plt.xlabel("Date")
        plt.ylabel("Drawdown (%)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# More visualization methods can be added as needed.
