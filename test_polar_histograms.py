import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import secrets
from kilim_cipher import KILIM_Cipher

def plot_polar_histogram(ax, img, title, color):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256]).flatten()
    angles = np.linspace(0, 2 * np.pi, len(hist))
    ax.bar(angles, hist, width=(2*np.pi/256), color=color, alpha=0.8)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.set_xticklabels([]) 

def create_horizontal_polar_figure():
    white_img_path = "images/white.png"
    if not os.path.exists(white_img_path):
        os.makedirs("images", exist_ok=True)
        cv2.imwrite(white_img_path, np.ones((256, 256, 3), dtype=np.uint8) * 255)

    files = [
        ("White", white_img_path),
        ("Lena", "images/lena.png"),
        ("Aerial", "images/aerial.png")
    ]
    
    key = secrets.token_bytes(32)
    cipher = KILIM_Cipher(key)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw={'projection': 'polar'})

    for col, (name, path) in enumerate(files):
        if not os.path.exists(path):
            continue

        img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
        orig_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        enc_img = cipher.encrypt(orig_img)

        plot_polar_histogram(axes[0, col], orig_img[:,:,0], f"Original: {name}", '#1f77b4')
        plot_polar_histogram(axes[1, col], enc_img[:,:,0], f"Encrypted: {name}", '#d62728')

    fig.text(0.5, 0.96, 'Original Polar Histograms', ha='center', fontsize=16, fontweight='bold')
    fig.text(0.5, 0.48, 'Encrypted Polar Histograms', ha='center', fontsize=16, fontweight='bold')

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.90, wspace=0.3, hspace=0.4)
    save_path = "Figure_8_Horizontal_Polar.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    create_horizontal_polar_figure()