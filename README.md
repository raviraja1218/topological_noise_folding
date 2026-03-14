# Topological Noise Folding (TNF)

Official research implementation of **Topological Noise Folding**, a neuro-symbolic quantum circuit optimization framework designed to reduce sampling overhead in quantum error mitigation.

This repository contains the full codebase used in the paper:

**Topological Noise Folding for Scalable Quantum Error Mitigation**

---

## Overview

Quantum error mitigation techniques suffer from an exponential sampling cost that grows with the number of noise channels in a circuit.

Topological Noise Folding (TNF) addresses this problem by combining:

* ZX-calculus based diagrammatic circuit representation
* Graph Neural Networks (GNNs)
* Reinforcement Learning optimization
* Neuro-symbolic constraints enforcing Pauli flow

The framework discovers **noise-suppressing topological rewrites** that reduce non-Clifford gate counts while preserving circuit extractability.

---

## Key Results

| Metric                        | Result            |
| ----------------------------- | ----------------- |
| Benchmark circuits            | 81                |
| Improvement vs TKET           | 98.8% of circuits |
| Average T-count reduction     | 19.7%             |
| Maximum reduction             | 40.3%             |
| Hardware fidelity improvement | +2.39%            |

Hardware validation was performed on the **IBM Fez 156-qubit superconducting processor**.

---

## Repository Structure

```
topological_noise_folding/

src/
   core/                 # core GNN + RL implementation
   validation/           # hardware and benchmark evaluation
   figures/              # scripts to generate paper figures

scripts/
   reproduce_all.sh
   run_benchmarks.sh
   generate_figures.sh

results/
   benchmarks/
   ablation/
   hardware/
   hardware_real/

figures/
   benchmark_comparison.pdf
   ablation_figure.pdf
   hardware_results.pdf

data/
   raw/
   processed/

checkpoints/
   trained models

logs/
   training logs
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/raviraja1218/topological_noise_folding.git
cd topological_noise_folding
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Reproducing Results

Run the full experimental pipeline:

```bash
bash scripts/reproduce_all.sh
```

Run only benchmark experiments:

```bash
bash scripts/run_benchmarks.sh
```

Generate figures used in the paper:

```bash
bash scripts/generate_figures.sh
```

---

## Hardware Validation

Hardware experiments were executed using IBM Quantum backends.

Example run:

```bash
python src/validation/hardware_validation/hardware_runner.py
```

Outputs are stored in:

```
results/hardware_real/
```

---

## Dataset

Experiments use the **op-T-mize dataset** together with additional synthetic non-Clifford circuits.

Dataset reference:

```
results/benchmarks/full_benchmark_results.csv
```

---

## Citation

If you use this code, please cite:

```
Topological Noise Folding for Scalable Quantum Error Mitigation
Ravi Raja et al.
```

---

## License

MIT License

---

## Author

Ravi Raja
Quantum Computing Research
