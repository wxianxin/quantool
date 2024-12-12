import numpy as np


def get_log_return(prices):
    """
    Calculate log returns from prices
    """
    return np.log(prices[1:] / prices[:-1])


def get_simple_return(prices):
    """
    Calculate simple returns from prices
    """
    return prices[1:] / prices[:-1] - 1


def get_annualized_volatility(returns, period):
    """
    Calculate annualized volatility from returns
    """
    return np.std(returns) * np.sqrt(period)


def get_annualized_sharpe_ratio(returns, period):
    """
    Calculate annualized Sharpe ratio from returns
    """
    return np.mean(returns) / np.std(returns) * np.sqrt(period)


def get_annualized_sortino_ratio(returns, period):
    """
    Calculate annualized Sortino ratio from returns
    """
    if returns[returns < 0].size <= 1:
        return np.nan

    return np.mean(returns) / np.std(returns[returns < 0]) * np.sqrt(period)


def get_annualized_downside_deviation(returns, period):
    """
    Calculate annualized downside deviation from returns
    """
    return np.std(returns[returns < 0]) * np.sqrt(period)


def get_annualized_information_ratio(returns, benchmark_returns, period):
    """
    Calculate annualized information ratio from returns and benchmark returns
    """
    return (
        np.mean(returns - benchmark_returns)
        / np.std(returns - benchmark_returns)
        * np.sqrt(period)
    )


def get_annualized_tracking_error(returns, benchmark_returns, period):
    """
    Calculate annualized tracking error from returns and benchmark returns
    """
    return np.std(returns - benchmark_returns) * np.sqrt(period)


def get_hit_ratio(returns):
    """
    Calculate hit ratio from returns
    """
    return len(returns[returns > 0]) / len(returns)


def get_all_ratios(prices, benchmark_prices, period):
    """
    Calculate all ratios from prices and benchmark prices
    """
    returns = get_log_return(prices)
    benchmark_returns = get_log_return(benchmark_prices)

    return {
        "annualized_log_return": np.mean(returns) * period,
        "annualized_volatility": get_annualized_volatility(returns, period),
        "annualized_sharpe_ratio": get_annualized_sharpe_ratio(returns, period),
        "annualized_sortino_ratio": get_annualized_sortino_ratio(returns, period),
        "annualized_downside_deviation": get_annualized_downside_deviation(
            returns, period
        ),
        "annualized_information_ratio": get_annualized_information_ratio(
            returns, benchmark_returns, period
        ),
        "annualized_tracking_error": get_annualized_tracking_error(
            returns, benchmark_returns, period
        ),
        "hit_ratio": get_hit_ratio(returns),
    }


def print_all_ratios(prices, benchmark_prices, period):
    """
    Print all ratios from prices and benchmark prices
    """
    ratios = get_all_ratios(prices, benchmark_prices, period)
    print("#" * 41)
    for key, value in ratios.items():
        # pretty print with indentation
        print(f"{key:<30}: {value:.4f}")
    print("#" * 41)

    return None


if __name__ == "__main__":
    pass
    # test code here

    prices = np.array([100, 101, 102, 103, 104, 105, 104, 107, 108, 107])
    benchmark_prices = np.array(
        [100, 100.5, 101, 101.5, 102, 102.5, 103, 103.5, 104, 104.5]
    )
    print_all_ratios(prices, benchmark_prices, 365)
