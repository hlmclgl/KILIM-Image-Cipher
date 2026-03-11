import cv2
import numpy as np
import random
import os
from kilim_cipher import KILIM_Cipher

def calculate_npcr_uaci(img1, img2):
    arr1 = img1.flatten().astype(int)
    arr2 = img2.flatten().astype(int)
    
    diff = arr1 != arr2
    npcr = (np.sum(diff) / len(arr1)) * 100
    
    abs_diff = np.abs(arr1 - arr2)
    uaci = (np.sum(abs_diff) / (len(arr1) * 255)) * 100
    
    return npcr, uaci

def run_simulation():
    image_files = ["images/white.png", "images/lena.png", "images/aerial.png"] 
    results_db = {}

    print(f"{'='*65}")
    print(f"KILIM ALGORITHM - DIFFERENTIAL CRYPTANALYSIS SIMULATION")
    print(f"{'='*65}\n")

    for img_path in image_files:
        print(f"Processing {os.path.basename(img_path)}...")
        
        if not os.path.exists(img_path):
            continue
            
        img = cv2.imread(img_path) 
        metrics_list = []
        
        for trial in range(100):
            key = os.urandom(32) 
            cipher_engine = KILIM_Cipher(key)
            
            c1 = cipher_engine.encrypt(img)
            
            img_mod = img.copy()
            h, w = img.shape[:2]
            rx, ry = random.randint(0, h-1), random.randint(0, w-1)
            
            if len(img.shape) == 3:
                rc = random.randint(0, 2) 
                original_val = int(img_mod[rx, ry, rc])
                img_mod[rx, ry, rc] = (original_val + 1) % 256
            else:
                original_val = int(img_mod[rx, ry])
                img_mod[rx, ry] = (original_val + 1) % 256
            
            c2 = cipher_engine.encrypt(img_mod)
            
            npcr, uaci = calculate_npcr_uaci(c1, c2)
            metrics_list.append((trial+1, npcr, uaci))
            
            if (trial+1) % 20 == 0:
                print(f"  Completed {trial+1}/100 trials...")

        selected_trials = random.sample(metrics_list, 5)
        selected_trials.sort(key=lambda x: x[0]) 
        
        results_db[os.path.basename(img_path)] = selected_trials
        print(f"  Finished {os.path.basename(img_path)}.\n")

    print(f"{'='*70}")
    print(f"{'TEST IMAGE':<15} | {'TRIAL':<8} | {'NPCR (%)':<15} | {'UACI (%)':<15}")
    print(f"{'-'*70}")
    
    for img_name, trials in results_db.items():
        base_name = img_name.split('.')[0].capitalize()
        for t_id, npcr, uaci in trials:
            print(f"{base_name:<15} | {t_id:<8} | {npcr:.4f}%          | {uaci:.4f}%")
        print(f"{'-'*70}")

if __name__ == "__main__":
    run_simulation()