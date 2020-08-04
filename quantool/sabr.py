"""
SABR model 
"""

__author__ = "Steven Wang"
__email__ = "github.com/wxianixn"

import math
import numpy as np
import pandas as pd
from scipy import optimize
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


################################################################################
# sabr
def sabr_vol(
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
    spot_price: float,
    K: float,
    tau: float,
):
    """
    Args:
        alpha (float):
        beta (float):
        rho (float):
        nu (float):
        spot_price (float):
    """
    mid = (spot_price * K) ** 0.5
    # epsilon ???
    epsilon = tau
    zeta = alpha / (nu * (1 - beta)) * (spot_price ** (1 - beta) - K ** (1 - beta))
    gamma_1 = beta / mid
    gamma_2 = beta * (beta - 1) / mid ** 2
    D = math.log(((1 - 2 * rho * zeta + zeta ** 2) ** 0.5 + zeta - rho) / (1 - rho))
    if D == 0:
        print(
            "!!! D is 0; it could be that the spot price is too close to strike"
            " price!!!"
        )
        print(spot_price ** (1 - beta) - K ** (1 - beta))
        print(zeta)
        D = 0.000001
    A = alpha * math.log(spot_price / K) / D
    B = (
        (2 * gamma_2 - gamma_1 ** 2 + mid ** (-2))
        / 24
        * (nu * mid ** beta / alpha) ** 2
        + rho * gamma_1 / 4 * nu * mid ** beta / alpha
        + (2 - 3 * rho ** 2) / 24
    )

    sigma = A * (1 + B * epsilon)

    if mid < 0.001:
        print("mid: ", mid)

    return sigma


def get_sabr_params(option_chain_dict):
    """
    TODO: improve initial Guess
    """
    def sabr_obj_func(params, call_option_chain_list):
        alpha, beta, rho, nu = params
        summ = 0
        actual_sum_of_sigma = 0
        for C in call_option_chain_list:
            actual_sum_of_sigma += C.sigma  # TODO: move this out of object func for efficiency
            spot_price = C.S
            tau = C.tau
            K = C.K

            e = (sabr_vol(alpha, beta, rho, nu, spot_price, K, tau) - C.sigma) ** 2
            # if math.isnan(e):
            # why 100 not 0? After compare the 0 and 100, 100 'feels' better
            #   e = 100
            summ += e

        print(f"sum = {summ}; Relative residual: {summ / actual_sum_of_sigma}")
        return summ

    initial_guess = [0.0001, 0.5, 0, 0.0001]
    bnds = (0.0001, None), (0, 1), (-0.9999, 0.9999), (0.0001, 0.9999)
    sabr_params = optimize.minimize(
        sabr_obj_func,
        x0=initial_guess,
        args=(option_chain_dict["call"]),
        bounds=bnds,
        method="SLSQP",
        options={"eps": 0.001},
    )

    return sabr_params.x


#################################################################################
# Get sabr volatility
def get_sabr_vol_surface(params, spot_price, tt, kk):
    """Get surface vol of given tau and K"""
    alpha, beta, rho, nu = params
    sabr_vol_list = []
    for tau in tt:
        for K in kk:
            sabr_vol_list.append(sabr_vol(alpha, beta, rho, nu, spot_price, K, tau))

    sabr_vol_df = pd.DataFrame(np.array(sabr_vol_list).reshape(len(tt), len(kk)))

    return sabr_vol_list, sabr_vol_df


#################################################################################
# Get sabr volatility 1
def get_sabr_vol_surface_from_df(params: list, call_option_chain_list: list):
    """Get a list of vol of original data"""
    alpha, beta, rho, nu = params
    sabr_vol_list = []
    for C in call_option_chain_list:
        sabr_vol_list.append(sabr_vol(alpha, beta, rho, nu, C.S, C.K, C.tau))

    return sabr_vol_list


################################################################################
# Plot volatility surface
def plot_volatility_surface(tau_axis, K_axis, z):
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    tau_axis, K_axis = np.meshgrid(tau_axis, K_axis)
    surf = ax.plot_surface(tau_axis, K_axis, z, cmap=cm.seismic, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


################################################################################
# Plot comparison of volatility surface
def volatility_surface_comparison(kk, tt, z_1, z_2):
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    tt, kk = np.meshgrid(tt, kk)
    surf = ax.plot_surface(kk, tt, z_1, cmap=cm.seismic, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # TODO
    # blahblah

    plt.show()


if __name__ == "__main__":
    """Testing"""
    S = 100
    K = 100
    tau = 0.5
    r = 0.05
    price = 10
    iv = BS_IV(1, S, K, tau, r, price)
    print(f"iv: {iv}, price: {10}, Price based on IV: {BS_call(S, K, tau, r, iv)}")
