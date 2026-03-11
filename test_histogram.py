import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import secrets
from kilim_cipher import KILIM_Cipher

def plot_single_channel_hist(ax, channel_data):
    hist = cv2.calcHist([channel_data], [0], None, [256], [0, 256]).flatten()
    ax.bar(range(256), hist, width=1, color='#1f77b4', edgecolor='#1f77b4')
    ax.set_xlim([0, 256])
    ax.tick_params(axis='both', which='major', labelsize=8)

def create_academic_histogram_figure():
    white_img_path = "white.png"
    if not os.path.exists(white_img_path):
        white_rgb = np.ones((256, 256, 3), dtype=np.uint8) * 255
        cv2.imwrite(white_img_path, white_rgb)

    files = [white_img_path, "lena.png", "1024.png"]
    key = secrets.token_bytes(32)
    cipher = KILIM_Cipher(key)

    fig, axes = plt.subplots(3, 6, figsize=(18, 8))
    col_titles = ["Original (R)", "Original (G)", "Original (B)", 
                  "Encrypted (R)", "Encrypted (G)", "Encrypted (B)"]

    for row, path in enumerate(files):
        if not os.path.exists(path):
            continue
            
        img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
        orig_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        enc_img = cipher.encrypt(orig_img)

        channels = [
            orig_img[:,:,0], orig_img[:,:,1], orig_img[:,:,2],
            enc_img[:,:,0],  enc_img[:,:,1],  enc_img[:,:,2]
        ]

        for col in range(6):
            ax = axes[row, col]
            plot_single_channel_hist(ax, channels[col])
            
            if row == 0:
                ax.set_title(col_titles[col], fontsize=11, fontweight='bold', pad=10)

    fig.text(0.25, 0.02, '(a) Original Image Histograms', ha='center', fontsize=14, fontweight='bold')
    fig.text(0.75, 0.02, '(b) Encrypted Image Histograms', ha='center', fontsize=14, fontweight='bold')

    plt.subplots_adjust(left=0.05, right=0.98, bottom=0.1, top=0.92, wspace=0.3, hspace=0.4)
    save_path = "Figure_7_Block_Histograms.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    create_academic_histogram_figure()