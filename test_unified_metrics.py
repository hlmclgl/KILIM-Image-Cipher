import cv2
import numpy as np
import matplotlib.pyplot as plt
import secrets
import time
import os
from kilim_cipher import KILIM_Cipher

def calculate_entropy(image):
    histogram, _ = np.histogram(image.flatten(), bins=256, range=[0, 256])
    pdf = histogram / histogram.sum()
    pdf = pdf[pdf > 0]
    return -np.sum(pdf * np.log2(pdf))

def calculate_npcr_uaci(img1, img2):
    total_elements = img1.size 
    diff = np.zeros_like(img1, dtype=int)
    diff[img1 != img2] = 1
    
    npcr = (np.sum(diff) / total_elements) * 100
    diff_intensity = np.abs(img1.astype(int) - img2.astype(int))
    uaci = (np.sum(diff_intensity) / (total_elements * 255)) * 100
    
    return npcr, uaci

def run_unified_color_tests():
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

    print("\n" + "="*118)
    print(" " * 32 + "KILIM ALGORITHM: PERFORMANCE AND SECURITY METRICS")
    print("="*118)
    print(f"{'Test Image':<15} | {'Size':<12} | {'Enc Time(s)':<14} | {'Dec Time(s)':<12} | {'Entropy':<9} | {'NPCR (%)':<9} | {'UACI (%)':<9} | {'MSE'}")
    print("-" * 118)

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    title_font = {'fontsize': 14, 'fontweight': 'bold'}

    for i, (name, path) in enumerate(files):
        if not os.path.exists(path):
            continue
            
        img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        size_str = f"{h}x{w}x{c}"

        start_time = time.time()
        enc_img = cipher.encrypt(img)
        enc_time = time.time() - start_time
        
        start_time = time.time()
        dec_img = cipher.decrypt(enc_img)
        dec_time = time.time() - start_time
        
        mse_val = np.mean((img - dec_img) ** 2)
        entropy_val = calculate_entropy(enc_img)
        
        mod_img = img.copy()
        current_val = int(mod_img[h//2, w//2, 0])
        mod_img[h//2, w//2, 0] = (current_val + 1) % 256
        
        enc_img_mod = cipher.encrypt(mod_img)
        npcr, uaci = calculate_npcr_uaci(enc_img, enc_img_mod)

        print(f"{name:<15} | {size_str:<12} | {enc_time:<14.4f} | {dec_time:<12.4f} | {entropy_val:<9.5f} | {npcr:<9.4f} | {uaci:<9.4f} | {mse_val:.1f}")

        ax_orig = axes[i, 0]
        ax_orig.imshow(img)
        if i == 0: ax_orig.set_title("Original Image", fontdict=title_font)
        ax_orig.set_ylabel(name, fontsize=12, fontweight='bold')
        ax_orig.set_xticks([]); ax_orig.set_yticks([])

        ax_enc = axes[i, 1]
        ax_enc.imshow(enc_img)
        if i == 0: ax_enc.set_title("Encrypted Image", fontdict=title_font)
        ax_enc.axis('off')

        ax_dec = axes[i, 2]
        ax_dec.imshow(dec_img)
        if i == 0: ax_dec.set_title("Decrypted Image", fontdict=title_font)
        ax_dec.axis('off')

    print("=" * 118)
    
    plt.tight_layout()
    save_path = "Figure_5_RGB_Final_Proof.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    run_unified_color_tests()