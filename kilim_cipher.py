import numpy as np
import hashlib
import random
import hmac

class KILIM_Cipher:
    def __init__(self, key_bytes, iv_bytes=b'KILIM_IV_2026'):
        self.key_bytes = key_bytes
        self.iv_bytes = iv_bytes
        self.S_BOX = list(range(256))
        self.INV_S_BOX = list(range(256))
        self.seed_int = 0
        self._generate_sboxes()

    def _generate_sboxes(self):
        hmac_digest = hmac.new(self.key_bytes, self.iv_bytes, hashlib.sha256).digest()
        self.seed_int = int.from_bytes(hmac_digest[:8], byteorder='big')
        
        random.seed(self.seed_int)
        random.shuffle(self.S_BOX)
        
        for i, val in enumerate(self.S_BOX):
            self.INV_S_BOX[val] = i

    def encrypt(self, image):
        h, w = image.shape[0], image.shape[1]
        channels = image.shape[2] if len(image.shape) == 3 else 1
        
        flat_img = image.flatten().astype(int)
        N = len(flat_img)
        
        perm_indices = np.arange(N)
        np.random.seed(self.seed_int % (2**32 - 1)) 
        np.random.shuffle(perm_indices)
        scrambled_img = flat_img[perm_indices]
        
        c_fwd = np.zeros(N, dtype=int)
        current_c = self.S_BOX[0]
        
        for i in range(N):
            val = (scrambled_img[i] + current_c + i) % 256
            current_c = self.S_BOX[val]
            c_fwd[i] = current_c
            
        c_rev = c_fwd[::-1]
        c_bwd = np.zeros(N, dtype=np.uint8)
        current_c = self.S_BOX[-1]
        
        for i in range(N):
            val = (c_rev[i] + current_c + i) % 256
            current_c = self.S_BOX[val]
            c_bwd[i] = current_c
            
        final_cipher = c_bwd[::-1]
        return final_cipher.reshape((h, w, channels) if channels == 3 else (h, w))

    def decrypt(self, cipher_image):
        h, w = cipher_image.shape[0], cipher_image.shape[1]
        channels = cipher_image.shape[2] if len(cipher_image.shape) == 3 else 1
        
        flat_cipher = cipher_image.flatten().astype(int)
        N = len(flat_cipher)
        
        c_bwd = flat_cipher[::-1]
        c_rev = np.zeros(N, dtype=int)
        current_c = self.S_BOX[-1]
        
        for i in range(N):
            val = self.INV_S_BOX[c_bwd[i]]
            c_rev[i] = (val - current_c - i) % 256
            current_c = c_bwd[i]
            
        c_fwd = c_rev[::-1]
        scrambled_img = np.zeros(N, dtype=int)
        current_c = self.S_BOX[0]
        
        for i in range(N):
            val = self.INV_S_BOX[c_fwd[i]]
            scrambled_img[i] = (val - current_c - i) % 256
            current_c = c_fwd[i]
            
        perm_indices = np.arange(N)
        np.random.seed(self.seed_int % (2**32 - 1))
        np.random.shuffle(perm_indices)
        
        plain_img_flat = np.zeros(N, dtype=np.uint8)
        plain_img_flat[perm_indices] = scrambled_img
        
        return plain_img_flat.reshape((h, w, channels) if channels == 3 else (h, w))