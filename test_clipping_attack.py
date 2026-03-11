import cv2
import numpy as np
import matplotlib.pyplot as plt
import secrets
import math
import os
from kilim_cipher import KILIM_Cipher

def add_clipping_attack(image, percentage):
    clipped_img = image.copy()
    h, w, c = clipped_img.shape
    total_area = h * w
    crop_area = total_area * percentage
    crop_side = int(math.sqrt(crop_area)) 
    start_y = (h - crop_side) // 2
    start_x = (w - crop_side) // 2
    clipped_img[start_y:start_y+crop_side, start_x:start_x+crop_side] = [0, 0, 0]
    return clipped_img

def calculate_psnr(img1, img2):
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0: return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(mse))

def create_labeled_2x4_clipping_figure():
    lena_path = "images/lena.png"
    if not os.path.exists(lena_path):
        return

    img_bgr = cv2.imread(lena_path, cv2.IMREAD_COLOR)
    orig_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    key = secrets.token_bytes(32)
    cipher = KILIM_Cipher(key)
    
    perfect_enc_img = cipher.encrypt(orig_img)
    clip_levels = [0.10, 0.20, 0.30, 0.50]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    for i, percentage in enumerate(clip_levels):
        clipped_enc_img = add_clipping_attack(perfect_enc_img, percentage)
        dec_clipped_img = cipher.decrypt(clipped_enc_img)
        
        psnr_val = calculate_psnr(orig_img, dec_clipped_img)
        print(f"Clipped {int(percentage*100)}% | PSNR: {psnr_val:.2f} dB")

        ax_top = axes[0, i]
        ax_top.imshow(clipped_enc_img)
        ax_top.axis('off')

        label_text = f"({chr(97+i)}) Clipped {int(percentage*100)}%"
        ax_top.text(0.5, -0.02, label_text, fontsize=14, ha='center', va='top', transform=ax_top.transAxes)

        ax_bottom = axes[1, i]
        ax_bottom.imshow(dec_clipped_img)
        ax_bottom.axis('off')

    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, wspace=0.02, hspace=0.08)
    save_path = "Figure_11_Clipping_Attack.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()

if __name__ == "__main__":
    create_labeled_2x4_clipping_figure()