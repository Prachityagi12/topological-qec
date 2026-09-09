# Topological Quantum Error Correction

## Overview

This repository contains the study and implementation of **topological quantum error-correcting codes**, with a focus on understanding their stabilizer structure, error detection, decoding, and logical error behavior.

The repository currently covers:

* **Toric Code**
* **Surface Code**
* **Color Code**

The work progresses from the study and simulation of the Toric Code toward Surface Code and Color Code implementations.

---

## Codes Covered

### Toric Code

**Status:** Implemented and simulated

The Toric Code implementation includes:

* Stabilizer construction
* Pauli error models
* Syndrome extraction
* Minimum-Weight Perfect Matching (MWPM) decoding
* Logical error detection
* Exhaustive error testing
* Monte Carlo simulation

The implemented code corresponds to a `[[50,2,5]]` quantum error-correcting code.

For details, see [`Toric_Code/README.md`](Toric_Code/README.md).

### Surface Code

**Status:** Implementation and simulation in progress

The Surface Code is currently being implemented and simulated, following the study of its stabilizer structure, boundaries, logical operators, and decoding procedure.

For details, see [`Surface_Code/README.md`](Surface_Code/README.md).

### Color Code

**Status:** Planned / In progress

The Color Code section will focus on the construction and study of topological color codes, including their stabilizers, logical operators, error correction, and decoding.

For details, see [`Color_Code/README.md`](Color_Code/README.md).

---

## Repository Structure

```text
topological-qec/
│
├── Toric_Code/
│   ├── notes/
│   │   └── Toric_Code_Notes.pdf
│   ├── code/
│   │   └── Toric_Code_L52.py
│   ├── plots/
│   │   ├── Toric_Code_Plot1.png
│   │   └── Toric_Code_Plot2.png
│   ├── README.md
│   └── requirements.txt
│
├── Surface_Code/
│   ├── notes/
│   ├── code/
│   └── README.md
│
└── Color_Code/
    ├── notes/
    ├── code/
    └── README.md
```

---

## Implemented Work

The Toric Code implementation currently includes:

1. Construction of the toric lattice
2. Stabilizer matrix construction
3. Pauli noise model
4. Syndrome extraction
5. MWPM decoding
6. Logical error detection
7. Exhaustive testing of single- and two-qubit errors
8. Targeted testing of three-qubit errors
9. Monte Carlo simulation
10. Analysis of logical error and decoder failure rates

The implementation was validated for a code with parameters `[[50,2,5]]`.

---

## Future Work

The repository will be extended with:

* Completion of Surface Code simulation
* Color Code implementation and simulation
* Comparison of decoding performance across different topological codes
* Analysis of logical error rates and code-distance scaling
* Further exploration of fault-tolerant quantum error correction
