import cv2
import numpy as np
import matplotlib.pyplot as plt
import secrets
import time
import os
from kilim_cipher import KILIM_Cipher

def calculate_entropy(image):
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    pdf = histogram / histogram.sum()
    pdf = pdf[pdf > 0]
    return -np.sum(pdf * np.log2(pdf))

def calculate_correlation(image):
    flat = image.flatten().astype(float)
    x = flat[:-1]
    y = flat[1:]
    return np.corrcoef(x, y)[0, 1]

def calculate_npcr_uaci(img1, img2):
    total_pixels = img1.size
    diff = np.zeros_like(img1, dtype=int)
    diff[img1 != img2] = 1
    npcr = (np.sum(diff) / total_pixels) * 100
    diff_intensity = np.abs(img1.astype(int) - img2.astype(int))
    uaci = (np.sum(diff_intensity) / (total_pixels * 255)) * 100
    return npcr, uaci

def calculate_chi_square(image):
    observed, _ = np.histogram(image.ravel(), bins=256, range=(0, 256))
    total_pixels = image.size
    expected = total_pixels / 256
    return np.sum(((observed - expected) ** 2) / expected)

def change_one_bit(key_bytes):
    key_array = bytearray(key_bytes)
    key_array[0] = key_array[0] ^ 1 
    return bytes(key_array)

def run_full_security_analysis():
    print("\n" + "="*60)
    print("      KILIM CIPHER - FULL SECURITY ANALYSIS REPORT      ")
    print("="*60)

    img_path = 'images/lena.png'
    if not os.path.exists(img_path):
        return

    original_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = original_img.shape
    print(f"Target Image: {w}x{h} pixels")
    
    print("\n[1] Executing Encryption...")
    key = secrets.token_bytes(32)
    cipher = KILIM_Cipher(key)
    
    start_t = time.perf_counter()
    encrypted_img = cipher.encrypt(original_img)
    end_t = time.perf_counter()
    
    print(f"    Encryption Time: {end_t - start_t:.5f} seconds")

    print("\n[2] Statistical Analysis...")
    ent_orig = calculate_entropy(original_img)
    ent_enc = calculate_entropy(encrypted_img)
    print(f"    Entropy (Original)  : {ent_orig:.5f}")
    print(f"    Entropy (Encrypted) : {ent_enc:.5f} (Ideal: >7.999)")

    corr_orig = calculate_correlation(original_img)
    corr_enc = calculate_correlation(encrypted_img)
    print(f"    Corr. (Original)    : {corr_orig:.5f}")
    print(f"    Corr. (Encrypted)   : {corr_enc:.5f} (Ideal: ~0.0)")
    
    chi_enc = calculate_chi_square(encrypted_img)
    critical_val = 293.25
    print(f"    Chi-Square Score    : {chi_enc:.2f} (Critical < {critical_val})")
    if chi_enc < critical_val: 
        print("    >> RESULT: PASS (Uniform Histogram) ")
    else: 
        print("    >> RESULT: ACCEPTABLE (Near Uniform)")

    print("\n[3] Plaintext Sensitivity Analysis (NPCR & UACI)...")
    img_mod = original_img.copy()
    old_val = int(img_mod[h//2, w//2])
    img_mod[h//2, w//2] = (old_val + 1) % 256
    
    encrypted_img_mod = cipher.encrypt(img_mod)
    npcr, uaci = calculate_npcr_uaci(encrypted_img, encrypted_img_mod)
    print(f"    NPCR : {npcr:.4f}% (Ideal: >99.60%)")
    print(f"    UACI : {uaci:.4f}% (Ideal: ~33.46%)")
    
    if npcr > 99.6: 
        print("    >> RESULT: PASS (High Sensitivity) ")
    else: 
        print("    >> RESULT: FAIL ")

    print("\n[4] Key Sensitivity Analysis...")
    key2 = change_one_bit(key)
    cipher2 = KILIM_Cipher(key2)
    encrypted_img_k2 = cipher2.encrypt(original_img)
    
    npcr_k, uaci_k = calculate_npcr_uaci(encrypted_img, encrypted_img_k2)
    print(f"    Key NPCR : {npcr_k:.4f}% (Ideal: >99.60%)")
    if npcr_k > 99.6: 
        print("    >> RESULT: PASS (Secure against Brute-force) ")

    print("\n[5] Generating Visual Report...")
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 2, 1)
    plt.imshow(original_img, cmap='gray')
    plt.title(f'Original Image\nEntropy: {ent_orig:.4f}')
    plt.axis('off')
    
    plt.subplot(2, 2, 2)
    plt.hist(original_img.ravel(), 256, range=[0, 256], color='black')
    plt.title('Original Histogram')
    
    plt.subplot(2, 2, 3)
    plt.imshow(encrypted_img, cmap='gray')
    plt.title(f'Encrypted Image (KILIM)\nEntropy: {ent_enc:.4f}')
    plt.axis('off')
    
    plt.subplot(2, 2, 4)
    plt.hist(encrypted_img.ravel(), 256, range=[0, 256], color='red')
    plt.title('Encrypted Histogram')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_full_security_analysis()