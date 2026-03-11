import cv2
import numpy as np
import matplotlib.pyplot as plt
import secrets
import random
import os
from kilim_cipher import KILIM_Cipher

def get_adjacent_pixels(img_channel, direction, num_samples=3000):
    h, w = img_channel.shape
    x_vals, y_vals = [], []
    max_h, max_w = h - 2, w - 2
    for _ in range(num_samples):
        r = random.randint(0, max_h)
        c = random.randint(0, max_w)
        x_vals.append(img_channel[r, c])
        if direction == 'horizontal': y_vals.append(img_channel[r, c + 1])
        elif direction == 'vertical': y_vals.append(img_channel[r + 1, c])
        elif direction == 'diagonal': y_vals.append(img_channel[r + 1, c + 1])
    return x_vals, y_vals

def create_color_correlation_figure():
    white_img_path = "images/white.png"
    if not os.path.exists(white_img_path):
        os.makedirs("images", exist_ok=True)
        cv2.imwrite(white_img_path, np.ones((256, 256, 3), dtype=np.uint8) * 255)

    files = [white_img_path, "images/lena.png", "images/aerial.png"]
    key = secrets.token_bytes(32)
    cipher = KILIM_Cipher(key)

    fig, axes = plt.subplots(3, 6, figsize=(16, 9))
    
    directions = ['horizontal', 'vertical', 'diagonal']
    dir_colors = ['#1f77b4', '#2ca02c', '#d62728']
    col_titles = ["Orig (H)", "Orig (V)", "Orig (D)", "Enc (H)", "Enc (V)", "Enc (D)"]

    for row, path in enumerate(files):
        if not os.path.exists(path):
            continue
            
        img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
        orig_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        enc_img = cipher.encrypt(orig_img)

        orig_ch = orig_img[:,:,0]
        enc_ch = enc_img[:,:,0]

        for col in range(6):
            ax = axes[row, col]
            idx = col % 3
            direction = directions[idx]
            color = dir_colors[idx]
            
            x, y = get_adjacent_pixels(orig_ch if col < 3 else enc_ch, direction)
            
            ax.scatter(x, y, s=0.8, c=color, alpha=0.4)
            ax.set_xlim([0, 255]); ax.set_ylim([0, 255])
            ax.set_xticks([0, 255]); ax.set_yticks([0, 255])
            ax.tick_params(labelsize=8)
            
            if row == 0:
                ax.set_title(col_titles[col], fontsize=12, fontweight='bold', color=color)
            if col == 0:
                label_name = os.path.basename(path).split('.')[0].capitalize()
                ax.set_ylabel(label_name, fontsize=12, fontweight='bold')

    plt.subplots_adjust(left=0.05, right=0.98, bottom=0.1, top=0.9, wspace=0.3, hspace=0.3)
    
    fig.text(0.28, 0.02, '(a) Original (H, V, D Directions)', ha='center', fontsize=14, fontweight='bold')
    fig.text(0.72, 0.02, '(b) Encrypted (H, V, D Directions)', ha='center', fontsize=14, fontweight='bold')

    save_path = "Figure_9_Color_Correlation.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    create_color_correlation_figure()