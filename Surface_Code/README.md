\# Surface Code



\## Overview



This project focuses on the implementation and simulation of a \*\*rotated distance-3 Surface Code\*\* for quantum error correction.



The implementation studies the complete QEC workflow, starting from the construction of the surface-code geometry and stabilizers, followed by logical operators, encoding, syndrome extraction, error detection, and decoding.



The current implementation uses a rotated distance-3 Surface Code with parameters:



`\[\[9,1,3]]`



The project is being developed incrementally toward a complete \*\*boundary-aware MWPM decoder and Monte Carlo simulation\*\*.



\---



\## Surface Code vs Toric Code



The Surface Code is closely related to the Toric Code, but differs in its boundary conditions.



\### Toric Code



\* Uses periodic boundary conditions.

\* The lattice effectively wraps around in both directions.

\* There are no physical boundaries.

\* Error strings form closed or non-contractible loops.



\### Surface Code



\* Uses physical boundaries.

\* The lattice does not wrap around.

\* Two types of boundaries are present: \*\*rough\*\* and \*\*smooth\*\*.

\* Error strings can terminate at the appropriate boundary.



This project uses a \*\*rotated distance-3 Surface Code\*\* with 9 data qubits and 1 logical qubit.



\---



\## Code Parameters



The rotated distance-3 Surface Code contains:



\* 9 physical data qubits

\* 4 X-type stabilizers

\* 4 Z-type stabilizers

\* 1 logical qubit



The code parameters are:



`\[\[9,1,3]]`



The code distance is determined from the minimum weight of non-trivial logical operators:



$$

d = \\min(d\_X,d\_Z)

$$



For this implementation:



$$

d\_X = 3,\\qquad d\_Z = 3

$$



Therefore:



$$

d=3

$$



The code encodes one logical qubit into nine physical qubits and can correct an arbitrary single-qubit error.



\---



\## Geometry and Boundaries



The implementation uses a rotated distance-3 surface-code geometry with data qubits labeled:



`D1, D2, ..., D9`



The physical boundaries are divided into rough and smooth boundaries.



\### Rough Boundaries



The left and right boundaries are the rough boundaries.



\* Left rough boundary → `X4 = \[D4, D7]`

\* Right rough boundary → `X2 = \[D3, D6]`



These correspond to weight-2 X-type boundary stabilizers.



\### Smooth Boundaries



The top and bottom boundaries are the smooth boundaries.



\* Top smooth boundary → `Z1 = \[D1, D2]`

\* Bottom smooth boundary → `Z4 = \[D8, D9]`



These correspond to weight-2 Z-type boundary stabilizers.



The boundaries will later be incorporated into the decoding graph for boundary-aware MWPM decoding.



\---



\## Stabilizer Formalism



The surface code is described using X-type and Z-type stabilizers.



The implementation constructs:



\* `H\_X` — X-type stabilizer matrix

\* `H\_Z` — Z-type stabilizer matrix



The stabilizer matrices satisfy the CSS commutation condition:



$$

H\_XH\_Z^T = 0 \\pmod 2

$$



The number of logical qubits is calculated using:



$$

k=n-\\operatorname{rank}(H\_X)-\\operatorname{rank}(H\_Z)

$$



For the constructed code:



$$

n=9,\\qquad k=1

$$



which is consistent with the `\[\[9,1,3]]` code.



\---



\## Logical Operators



The logical operators used in this implementation are:



$$

X\_L=X\_1X\_2X\_3

$$



and



$$

Z\_L=Z\_3Z\_6Z\_9

$$



The logical operators commute with all stabilizer generators and anticommute with each other.



Equivalent logical representatives can be obtained by multiplying a logical operator by stabilizers.



For example, another minimum-weight representative of the logical Z operator is:



$$

Z\_1Z\_4Z\_7

$$



\---



\## Encoding



An encoding circuit was constructed for the logical state \\(|0\_L\\rangle\\).



The encoding procedure prepares four independent physical qubits in the \\(|+\\rangle\\) state and uses CNOT gates to generate the encoded surface-code state.



The independent qubits used in the implementation are:



\* D1

\* D3

\* D4

\* D5



The resulting state is verified against the stabilizer generators and the logical Z operator.



\---



\## Encoding Verification



The encoded state was verified using a statevector simulation.



The prepared state satisfies:



$$

S\_i|0\_L\\rangle=|0\_L\\rangle

$$



for all stabilizer generators.



The logical Z eigenvalue was also verified:



$$

Z\_L|0\_L\\rangle=|0\_L\\rangle

$$



Therefore, the circuit successfully prepares the encoded logical \\(|0\_L\\rangle\\) state.



\---



\## Error Model



The implementation studies physical Pauli errors applied to the encoded state.



The initial error models include:



\* Single-qubit X errors

\* Single-qubit Z errors

\* Single-qubit Y errors

\* Multiple-qubit errors

\* Random Pauli errors



The syndrome-extraction implementation currently focuses on verifying the effect of single-qubit X and Z errors.



\---



\## Syndrome Extraction



Syndrome extraction is performed using ancilla qubits without directly measuring the encoded logical information.



The syndrome-extraction circuit contains:



\* 9 data qubits

\* 4 X-stabilizer ancillas

\* 4 Z-stabilizer ancillas



giving a total of:



$$

9+4+4=17

$$



qubits.



The qubit assignment is:



| Qubits | Indices | Purpose               |

| ------ | ------: | --------------------- |

| D1–D9  |     0–8 | Data qubits           |

| X1–X4  |    9–12 | X-stabilizer ancillas |

| Z1–Z4  |   13–16 | Z-stabilizer ancillas |



\---



\## Error-Free Syndrome Verification



The encoded \\(|0\_L\\rangle\\) state was prepared and all eight stabilizers were measured using ancilla qubits.



For the error-free state:



$$

S\_X=\[0,0,0,0]

$$



$$

S\_Z=\[0,0,0,0]

$$



Therefore, the complete syndrome is:



$$

S=\[0,0,0,0,0,0,0,0]

$$



This confirms that the encoded state satisfies all eight stabilizer checks.



\---



\## Single-Qubit X-Error Syndrome



A single-qubit X error was introduced independently on each of the nine data qubits.



Since an X error anticommutes with Z-type stabilizers, the Z-stabilizer measurements are used to detect X errors.



The syndrome-extraction circuit was tested for X errors on:



`D1–D9`



and produced the expected stabilizer-flip patterns.



For example, an X error on D5 produces flips in the corresponding Z-type stabilizers.



The results confirm that the syndrome-extraction circuit detects single-qubit X errors.



\---



\## Single-Qubit Z-Error Syndrome



Single-qubit Z errors were similarly introduced on each of the nine data qubits.



Since a Z error anticommutes with X-type stabilizers, the X-stabilizer measurements are used to detect Z errors.



For example:



$$

Z(D3)\\rightarrow X\_2

$$



because D3 is part of:



$$

X\_2=X\_{D3}X\_{D6}

$$



The syndrome-extraction circuit was tested for Z errors on all nine data qubits and produced the expected stabilizer-flip patterns.



\---



\## Qiskit Pauli-String Convention



The physical data qubits are labeled D1–D9 and correspond to Qiskit qubits:



`q0–q8`



Qiskit Pauli strings use reverse qubit ordering:



$$

q\_8,q\_7,\\ldots,q\_1,q\_0

$$



Therefore, the leftmost character corresponds to the highest-index Qiskit qubit, while the rightmost character corresponds to `q0` (D1).



The Pauli strings in the implementation are generated from the physical data-qubit labels to reduce indexing errors.



\---



\## Degeneracy and Syndrome Ambiguity



Different physical errors can produce the same syndrome.



Therefore, a measured syndrome does not necessarily identify a unique physical error.



For two errors \\(E\_1\\) and \\(E\_2\\):



$$

S(E\_1)=S(E\_2)

$$



implies that their product commutes with all stabilizers.



The errors are truly degenerate when:



$$

E\_1E\_2\\in\\mathcal{S}

$$



where \\(\\mathcal{S}\\) is the stabilizer group.



Thus:



$$

\\text{Same syndrome}\\neq\\text{necessarily degenerate}

$$



This distinction is important for understanding why a decoder is required.



\---



\## Why Decoding Is Required



Syndrome extraction identifies which stabilizers have been flipped, but the syndrome may correspond to multiple possible physical errors.



For example, different X errors can produce the same syndrome.



Therefore, the QEC process requires a decoder:



$$

\\text{Physical Error}

\\rightarrow

\\text{Syndrome}

\\rightarrow

\\text{Decoder}

\\rightarrow

\\text{Correction}

$$



The next stage of the project is to construct a \*\*boundary-aware Minimum-Weight Perfect Matching (MWPM) decoder\*\* that determines an appropriate correction from the measured syndrome.



\---



\## Current Progress



\### Completed



\* Rotated distance-3 Surface Code geometry

\* 9 data-qubit construction

\* Rough and smooth boundary identification

\* X- and Z-type stabilizer construction

\* Stabilizer commutation verification

\* Code parameter verification

\* Logical X and Z operators

\* Logical operator verification

\* Logical \\(|0\_L\\rangle\\) encoding

\* Encoding verification

\* Single-qubit X-error analysis

\* Single-qubit Z-error analysis

\* Ancilla-based syndrome extraction

\* Syndrome verification for single-qubit errors

\* Study of syndrome degeneracy and ambiguity



\### In Progress



\* Complete syndrome extraction for all Pauli errors

\* Automatic syndrome-to-error mapping

\* Boundary-aware decoding graph

\* MWPM decoder

\* Automatic correction

\* Logical error detection

\* Monte Carlo simulation

\* Logical error-rate analysis



\---



\## Future Work



The final implementation will extend the current Surface Code simulation to:



\* Boundary-aware MWPM decoding

\* Automatic X- and Z-error correction

\* Y-error and general Pauli-noise decoding

\* Logical error detection after correction

\* Monte Carlo simulation over different physical error rates

\* Logical error-rate analysis

\* Performance comparison with other topological codes

\* Extension toward Color Code implementation



