# Perturbed Inverse QFT Circuit Analysis

A toolkit for constructing, simulating, and visualizing parameterized quantum circuits built around the Inverse Quantum Fourier Transform (IQFT). The project explores how continuous phase perturbations applied after an IQFT create structured interference patterns across the computational basis, and provides interactive tools for analyzing the resulting probability landscapes.

## Overview

The core circuit operates on 4 qubits and follows this pipeline:

1. **Input Encoding** — A classical integer $x \in \{0, \dots, 15\}$ is encoded into a computational basis state $|x\rangle$.
2. **Inverse QFT** — The IQFT maps the basis state into a phase-encoded superposition.
3. **Phase Perturbation** — Independent parameterized phase gates $P(\theta_k)$ are applied to each qubit, coupling arbitrary angles to the fractional periods dictated by the IQFT.
4. **Final Decoding IQFT** — A second IQFT decodes the perturbed state, producing complex interference patterns governed by both the input and the phase parameters.

The mathematical derivation is documented in [`circuit_math.tex`](circuit_math.tex) (compiled PDF: [`circuit_math.pdf`](circuit_math.pdf)).

## Project Structure

| File | Description |
|---|---|
| `perturbed_qft.py` | Core circuit construction and 3D surface plot generation. Defines `create_circuit()` and computes marginal qubit probabilities across all 16×16 input/theta configurations. |
| `perturbed_qft_gui.py` | Interactive bar-chart GUI with sliders for continuous theta control, input state selection, and toggles for enabling/disabling IQFT stages. Includes circuit diagram export. |
| `heatmap_qft_gui.py` | Interactive heatmap GUI displaying marginal $P(\|1\rangle)$ for all 4 qubits across all 16 input states simultaneously, with continuous theta sliders. |
| `circuit_math.tex` | LaTeX derivation of the full mathematical model: input encoding, IQFT factorization, phase perturbation coupling, global statevector expansion, and marginal probability equations. |
| `circuit_math.pdf` | Compiled PDF of the derivation. |

## Requirements

- Python 3.8+
- [Qiskit](https://qiskit.org/) (`qiskit`, `qiskit-aer`)
- NumPy
- Matplotlib
- A LaTeX distribution (e.g., MiKTeX or TeX Live) to compile `circuit_math.tex`

Install Python dependencies:

```bash
pip install qiskit numpy matplotlib
```

## Usage

### 3D Surface Plots

Generate static 3D surface plots showing the marginal probability of measuring $|1\rangle$ for each qubit across all 16 input states and 16 binary theta configurations:

```bash
python perturbed_qft.py
```

This produces a 2×2 grid of surface plots (one per qubit) with the input state on one axis, the theta configuration on the other, and the marginal probability on the Z-axis.

### Interactive Bar Chart GUI

Launch the slider-based GUI for real-time exploration of output probability distributions:

```bash
python perturbed_qft_gui.py
```

**Controls:**
- **Theta 0–3 sliders** — Continuously adjust each qubit's phase perturbation from $-\pi$ to $\pi$.
- **Input State slider** — Select the classical input integer (0–15).
- **Checkboxes** — Toggle the initial IQFT and the final decoding IQFT independently.
- **Show Circuit button** — Print the circuit diagram and LaTeX-formatted statevector to the console.

### Interactive Heatmap GUI

Launch the heatmap view for a compact overview of all qubit marginals across all inputs:

```bash
python heatmap_qft_gui.py
```

**Controls:**
- **Theta 0–3 sliders** — Continuously adjust phase perturbations. The heatmap updates in real time, showing how the interference pattern shifts across all 16 input states simultaneously.

### Compile the Math Derivation

```bash
pdflatex circuit_math.tex
```

## Mathematical Background

The final statevector after both IQFT stages and phase perturbation is:

$$|\psi_{\text{final}}\rangle = \frac{1}{2^n} \sum_{z=0}^{2^n-1} \sum_{y=0}^{2^n-1} \exp\!\left(-2\pi i \frac{y(x+z)}{2^n} + i \sum_{k=0}^{n-1} \theta_k y_k\right) |z\rangle$$

The marginal probability of measuring qubit $j$ in the $|1\rangle$ state is obtained by tracing out the remaining qubits:

$$P(q_j = 1) = \frac{1}{2^{2n}} \sum_{z=0}^{2^n-1} z_j \left|\sum_{y=0}^{2^n-1} \exp\!\left(-2\pi i \frac{y(x+z)}{2^n} + i \sum_{k=0}^{n-1} \theta_k y_k\right)\right|^2$$

See [`circuit_math.pdf`](circuit_math.pdf) for the complete step-by-step derivation.
