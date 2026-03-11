import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_scrambling_toy_example():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.axis('off')

    grid_size = 3
    cell_size = 1.0
    
    original_seq = [11, 12, 13, 21, 22, 23, 31, 32, 33]
    scrambled_seq = [31, 13, 22, 12, 33, 21, 23, 11, 32] 
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']
    color_map = {val: colors[i] for i, val in enumerate(original_seq)}

    start_x1, start_y1 = 0, 0
    for i in range(grid_size):
        for j in range(grid_size):
            idx = i * grid_size + j
            val = original_seq[idx]
            rect = patches.Rectangle((start_x1 + j*cell_size, start_y1 + (grid_size-1-i)*cell_size), 
                                     cell_size, cell_size, linewidth=1.5, edgecolor='black', facecolor=color_map[val], alpha=0.8)
            ax.add_patch(rect)
            ax.text(start_x1 + j*cell_size + cell_size/2, start_y1 + (grid_size-1-i)*cell_size + cell_size/2, 
                    str(val), color='white', weight='bold', fontsize=14, ha='center', va='center')

    start_x2 = 6

    ax.annotate("Global\nScrambling", xy=(5.6, 1.5), xytext=(4.3, 1.5),
                arrowprops=dict(facecolor='black', shrink=0.05, width=3, headwidth=10),
                fontsize=13, fontweight='bold', ha='center', va='center')

    for i in range(grid_size):
        for j in range(grid_size):
            idx = i * grid_size + j
            val = scrambled_seq[idx]
            rect = patches.Rectangle((start_x2 + j*cell_size, start_y1 + (grid_size-1-i)*cell_size), 
                                     cell_size, cell_size, linewidth=1.5, edgecolor='black', facecolor=color_map[val], alpha=0.8)
            ax.add_patch(rect)
            ax.text(start_x2 + j*cell_size + cell_size/2, start_y1 + (grid_size-1-i)*cell_size + cell_size/2, 
                    str(val), color='white', weight='bold', fontsize=14, ha='center', va='center')

    ax.text(1.5, -0.5, "Before Scrambling", fontsize=14, fontweight='bold', ha='center')
    ax.text(7.5, -0.5, "After Scrambling", fontsize=14, fontweight='bold', ha='center')

    plt.xlim(-0.5, 9.5)
    plt.ylim(-1, 3.5)
    
    save_path = "Figure_2_Scrambling_Global.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def draw_diffusion_toy_example():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')

    seq_length = 8
    rounds = 5  
    
    cell_w = 1.0
    cell_h = 0.6
    y_spacing = 1.4 

    labels = [f"$S_{{{i}}}$" for i in range(1, seq_length+1)]
    
    for r in range(rounds):
        y_pos = (rounds - 1 - r) * y_spacing
        
        row_title = "Initial State (Scrambled Array)" if r == 0 else f"Step {r} Diffusion"
        ax.text(seq_length/2, y_pos - 0.25, row_title, fontsize=12, ha='center', va='top')

        for c in range(seq_length):
            x_pos = c * cell_w
            face_color = 'white'
            text_color = 'black'
            cell_text = labels[c]

            if r > 0:
                if c < r:
                    face_color = '#d3d3d3' 
                    cell_text = f"$C_{{{c+1}}}$"
                elif c == r:
                    face_color = '#696969' 
                    text_color = 'white'
                    cell_text = f"$C_{{{c+1}}}$"

            rect = patches.Rectangle((x_pos, y_pos), cell_w, cell_h, 
                                     linewidth=1.5, edgecolor='black', facecolor=face_color)
            ax.add_patch(rect)
            ax.text(x_pos + cell_w/2, y_pos + cell_h/2, cell_text, 
                    color=text_color, fontsize=12, fontweight='bold', ha='center', va='center')

        if r > 0:
            formula = f"$C_{{{r+1}}} = (S_{{{r+1}}} + C_{{{r}}} + {r+1}) \\ \\mathrm{{mod}} \\ 256$"
            ax.text(seq_length + 0.5, y_pos + cell_h/2, formula, fontsize=12, va='center')

    plt.xlim(-0.5, seq_length + 5)
    plt.ylim(-1.0, rounds * y_spacing)
    
    save_path = "Figure_9_Architecture.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_scrambling_toy_example()
    draw_diffusion_toy_example()