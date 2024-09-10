import matplotlib.pyplot as plt

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
        axes[i].set_title(f'Graph {i+1}')
        # axes[i].axvline(x=idx, color='g', linestyle='--', label='Middle')
        
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()
    
    # Display the figure
    plt.show()
