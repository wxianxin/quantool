import matplotlib.pyplot as plt
import numpy as np


def plot_grid(vec_of_dict):
    # grid plots

    if len(vec_of_dict) > 15:
        raise Exception("Can only plot 15 or less plots in the grid!")

    fig, axes = plt.subplots(3, 5, figsize=(16, 9))
    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Loop over each subplot
    for i, d in enumerate(vec_of_dict):
        for k, v in d.items():
            axes[i].plot(v, label=k)
        axes[i].legend()
        axes[i].set_title(f"Graph {i+1}")
        # axes[i].axvline(x=idx, color='g', linestyle='--', label='Middle')

    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    # Display the figure
    plt.show()


def plot_dict_of_vec(data, title="Loss over Epochs", xlabel="Epoch", ylabel="Loss"):
    # Plot each loss series
    for label, loss_values in data.items():
        plt.plot(loss_values, label=label)

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()

    # Display the plot
    plt.show()


def plot_performance(
    x,
    y,
    position=None,
    benchmark=None,
    title="Performance Metrics",
    xlabel="time",
    ylabel="return",
):
    color = "palegreen"
    # downsample the data for better visualization
    if len(x) / 10_000 > 10:
        step = len(x) // 10_000
        x = x[::step]
        y = y[::step]
        if position is not None:
            position = position[::step]
        if benchmark is not None:
            benchmark = benchmark[::step]

    # calculate the nav, drawdown, volatility and sharpe ratio
    nav = 1 + y[-1]
    drawdown = y - np.maximum.accumulate(y)
    vol = np.std(y)
    sharpe = np.mean(y) / vol

    # Create the figure and the grid layout
    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(2, 2, wspace=0.1, width_ratios=(4, 1), height_ratios=(4, 1))

    # Main plot (top left)
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(x, y, "b", label="Return")
    if benchmark is not None:
        ax.plot(x, benchmark, "r", label="Benchmark")
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Drawdown plot
    ax_drawdown = ax.twinx()  # Create twin axis sharing the same x-axis
    ax_drawdown.fill_between(
        x,
        0,
        drawdown,
        where=(drawdown <= 0),
        color=color,
        alpha=0.5,
        label="Drawdown",
    )

    # Set the same y-limits for both ax and ax_drawdown
    y_min, y_max = ax.get_ylim()  # Get limits from the main plot
    ax_drawdown.set_ylim(-y_max, 0)  # Set the drawdown y-axis limits to mirror main

    # Bottom plot (bottom left)
    if position is None:
        position = np.zeros_like(x)
    ax_1_0 = fig.add_subplot(gs[1, 0], sharex=ax)
    ax_1_0.plot(x, position, color)
    ax_1_0.set_ylabel("position")

    # Right Top part (top right)
    ax_0_1 = fig.add_subplot(gs[0, 1], sharey=ax)
    ax_0_1.set_facecolor(color)
    # hide axis
    ax_0_1.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    # hide plot border
    for spine in ax_0_1.spines.values():
        spine.set_visible(False)

    cell_text = [
        ["NAV:", "{:.2%}".format(nav)],
        ["Max DD:", "{:.2%}".format(min(drawdown))],
        ["Volatility:", "{:.2%}".format(vol)],
        ["Sharpe:", "{:.2%}".format(sharpe)],
    ]
    table = ax_0_1.table(
        cellText=cell_text,
        cellLoc="left",
        colWidths=[0.6, 0.4],
        loc="center",
        edges="open",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 3)  # Scale to fit the layout

    # Right Bottom part (bottom right)
    ax_1_1 = fig.add_subplot(gs[1, 1])
    ax_1_1.axis("off")
    text = "AK-RS-test"
    ax_1_1.text(
        0.5,
        0.5,
        text,
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color="white",
        bbox=dict(facecolor=color, edgecolor="none", boxstyle="round,pad=1"),
    )

    plt.show()
