# KILIM Image Cipher

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/1178376518.svg)](https://doi.org/10.5281/zenodo.18946529)

Official Python implementation of **"KILIM: A Novel Lightweight and Lossless Spatiotemporal Image Encryption Algorithm for Resource-Constrained IoT Environments"**.

## 📌 Overview
The transmission of sensitive visual data over resource-constrained Internet of Things (IoT) networks demands encryption schemes that balance rigorous security with high computational efficiency. Existing algorithms often rely on continuous floating-point chaotic maps, which are prone to dynamical degradation, or complex DNA encoding sequences that impose heavy processing burdens. 

**KILIM** addresses these limitations by operating strictly within the Galois Field $GF(2^8)$ utilizing integer-based Modulo 256 arithmetic. 

### ✨ Key Features
* **Lightweight & Hardware-Friendly:** Pure integer-based linear time complexity $O(N)$, eliminating floating-point quantization errors.
* **Extreme Key Sensitivity:** HMAC-SHA256 driven deterministic random bit generator.
* **Maximized Avalanche Effect:** Bidirectional sequential diffusion guarantees exceptional differential resistance (NPCR > 99.85%, UACI ~ 33.52%).
* **100% Lossless Recovery:** Guarantees a Mean Squared Error (MSE) of exactly 0.0 in noise-free channels.
* **Highly Robust:** Maintains semantic intelligibility even under 40% salt-and-pepper noise and 50% data occlusion attacks.

## 📂 Repository Structure
This repository is designed for reproducibility. It contains the core encryption engine and all simulation scripts used to generate the tables and figures in the manuscript.

* `kilim_cipher.py`: The core object-oriented implementation of the KILIM algorithm.
* `test_unified_metrics.py`: Generates the main performance table (Encryption Time, Entropy, NPCR, UACI) and the 3x3 visual encryption grid.
* `test_histograms.py`: Generates 1D block histograms for RGB channels.
* `test_polar_histograms.py`: Generates polar histogram plots.
* `test_correlation.py`: Analyzes adjacent pixel correlation (Horizontal, Vertical, Diagonal) and plots scatter diagrams.
* `test_differential.py`: Simulates 100 rounds of plaintext attacks to prove NPCR and UACI stability.
* `test_clipping_attack.py`: Evaluates robustness against data occlusion (cropping) attacks.
* `test_noise_attack_clean.py`: Evaluates robustness against Salt & Pepper noise attacks.
* `draw_architecture_schematics.py`: Generates the toy examples for the Scrambling and Diffusion processes.
* `/images`: Directory containing the standard test images (`white.png`, `lena.png`, `aerial.png`).

## 💾 NIST SP 800-22 Dataset (750 MB)
Due to GitHub's file size limitations, the **750 MB ciphertext dataset** generated for the NIST Statistical Test Suite is securely archived on Zenodo. 
👉 **[Download the Dataset from Zenodo](https://doi.org/10.5281/zenodo.18946529)**

## 🚀 Installation & Usage

1. Clone the repository:
```bash
git clone [https://github.com/hlmclgl/KILIM-Image-Cipher.git](https://github.com/hlmclgl/KILIM-Image-Cipher.git)
cd KILIM-Image-Cipher
```

2. Install the required dependencies:
```bash
pip install numpy opencv-python matplotlib scipy
```

3. Run any of the test scripts. For example, to generate the main performance metrics and visual grid:
```bash
python test_unified_metrics.py
```

## 📝 Citation
If you find this code useful in your research, please consider citing our paper:
```bibtex
@article{kilim2026,
  title={KILIM: A Novel Lightweight and Lossless Spatiotemporal Image Encryption Algorithm for Resource-Constrained IoT Environments},
  author={[Author Names]},
  journal={[Journal Name]},
  year={2026}
}
```
