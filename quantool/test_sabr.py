import matplotlib.pyplot as plt
import quantool
my_d = quantool.prepare_option("MSFT", 0.01)
sabr_param_list = quantool.sabr.get_sabr_params(my_d)
print(sabr_param_list)
tau_axis = list(set([C.tau for C in my_d["call"]]))
K_axis = list(set([C.K for C in my_d["call"]]))
spot_price = my_d["call"][0].S
sabr_vol_list, sabr_vol_df = quantool.sabr.get_sabr_vol_surface(sabr_param_list, spot_price, tau_axis, K_axis)

quantool.sabr.plot_volatility_surface(K_axis, tau_axis, sabr_vol_df)
plt.show()

