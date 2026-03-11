import cv2
import numpy as np
import matplotlib.pyplot as plt
import secrets
import os
from kilim_cipher import KILIM_Cipher

def add_rgb_salt_and_pepper_noise(image, density):
    noisy_image = image.copy()
    h, w, c = noisy_image.shape
    num_pixels = h * w
    total_noisy_pixels = int(num_pixels * density)
    indices = np.random.choice(num_pixels, total_noisy_pixels, replace=False)
    coords = np.unravel_index(indices, (h, w))
    num_salt = total_noisy_pixels // 2
    salt_coords = (coords[0][:num_salt], coords[1][:num_salt])
    pepper_coords = (coords[0][num_salt:], coords[1][num_salt:])
    noisy_image[salt_coords] = [255, 255, 255]
    noisy_image[pepper_coords] = [0, 0, 0]
    return noisy_image

def calculate_psnr(img1, img2):
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0: return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(mse))

def create_clean_robustness_figure():
    lena_path = "images/lena.png"
    if not os.path.exists(lena_path):
        return

    img_bgr = cv2.imread(lena_path, cv2.IMREAD_COLOR)
    orig_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    key = secrets.token_bytes(32)
    cipher = KILIM_Cipher(key)
    
    perfect_enc_img = cipher.encrypt(orig_img)
    noise_levels = [0.05, 0.10, 0.20, 0.40] 
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    for i, density in enumerate(noise_levels):
        noisy_enc_img = add_rgb_salt_and_pepper_noise(perfect_enc_img, density)
        dec_noisy_img = cipher.decrypt(noisy_enc_img)
        
        psnr_val = calculate_psnr(orig_img, dec_noisy_img)
        print(f"Noise {int(density*100)}% | PSNR: {psnr_val:.2f} dB")

        ax = axes[i]
        ax.imshow(dec_noisy_img)
        ax.axis('off')

    plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0.02)
    save_path = "Figure_10_Robustness_Clean.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

if __name__ == "__main__":
    create_clean_robustness_figure()