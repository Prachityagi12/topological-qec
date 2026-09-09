import numpy as np
# ============================================================
# 1. TORIC CODE PARAMETERS
# ============================================================
L = 5
n_vertices = L * L
n_plaquettes = L * L
n_qubits = 2 * L * L

print("Code distance:", L)
print("Number of vertices:", n_vertices)
print("Number of plaquettes:", n_plaquettes)
print("Number of data qubits:", n_qubits)

# ============================================================
# 2. TORIC CODE GEOMETRY
# ============================================================
# Vertex numbering
vertex_id = {}

for x in range(L):
    for y in range(L):
        vertex = x * L + y
        vertex_id[(x, y)] = vertex

print("\nVertex mapping:")
for coordinate, vertex in vertex_id.items():
    print(coordinate, "->", vertex + 1)

# ============================================================
# 3. PHYSICAL QUBIT -> EDGE MAPPING
# ============================================================

qubit_edges = {}

qubit = 0

# ------------------------------------------------------------
# Horizontal edges: q1 - q25
# ------------------------------------------------------------

for x in range(L):
    for y in range(L):

        v1 = vertex_id[(x, y)]
        v2 = vertex_id[(x, (y + 1) % L)]

        qubit_edges[qubit] = (v1, v2)

        qubit += 1


# ------------------------------------------------------------
# Vertical edges: q26 - q50
# ------------------------------------------------------------

for x in range(L):
    for y in range(L):

        v1 = vertex_id[(x, y)]
        v2 = vertex_id[((x + 1) % L, y)]

        qubit_edges[qubit] = (v1, v2)

        qubit += 1


print("\nPhysical qubit edges:")

for q, edge in qubit_edges.items():
    print(f"q{q + 1}: v{edge[0] + 1} -- v{edge[1] + 1}")

import numpy as np

L = 5
n_qubits = 2 * L * L

# HX = np.zeros((25, 50), dtype=int)

# HZ = np.zeros((25, 50), dtype=int)

# # ============================================================
# 4. STABILIZER MATRICES
# ============================================================

HX = np.zeros((n_vertices, n_qubits), dtype=int)
HZ = np.zeros((n_plaquettes, n_qubits), dtype=int)

# ------------------------------------------------------------
# Helper functions for qubit numbering
# ------------------------------------------------------------

def horizontal_qubit(x, y):
    """
    Horizontal edge from (x,y) to (x,y+1).
    Returns zero-based qubit index.
    """
    return x * L + y


def vertical_qubit(x, y):
    """
    Vertical edge from (x,y) to (x+1,y).
    Returns zero-based qubit index.
    """
    return L * L + x * L + y


# ------------------------------------------------------------
# X-type stabilizers: Star operators A_v
# ------------------------------------------------------------

for x in range(L):
    for y in range(L):

        vertex = vertex_id[(x, y)]

        # Four edges touching vertex (x,y)
        q_left   = horizontal_qubit(x, (y - 1) % L)
        q_right  = horizontal_qubit(x, y)

        q_up     = vertical_qubit((x - 1) % L, y)
        q_down   = vertical_qubit(x, y)

        HX[vertex, q_left] = 1
        HX[vertex, q_right] = 1
        HX[vertex, q_up] = 1
        HX[vertex, q_down] = 1


# ------------------------------------------------------------
# Z-type stabilizers: Plaquette operators B_p
# ------------------------------------------------------------

for x in range(L):
    for y in range(L):

        plaquette = x * L + y

        # Four edges surrounding plaquette
        q_bottom = horizontal_qubit(x, y)
        q_top    = horizontal_qubit((x + 1) % L, y)

        q_left   = vertical_qubit(x, y)
        q_right  = vertical_qubit(x, (y + 1) % L)

        HZ[plaquette, q_bottom] = 1
        HZ[plaquette, q_top] = 1
        HZ[plaquette, q_left] = 1
        HZ[plaquette, q_right] = 1


print("\nHX shape:", HX.shape)
print(HX)

print("\nHZ shape:", HZ.shape)
print(HZ)

# ============================================================
# 5. STABILIZER COMMUTATION CHECK
# ============================================================

commutation = (HX @ HZ.T) % 2

print("\nCommutation matrix shape:", commutation.shape)

if np.all(commutation == 0):
    print("SUCCESS: All X-type and Z-type stabilizers commute.")
else:
    print("ERROR: Some stabilizers do not commute.")

# ============================================================
# 5. RANK CHECK
# ============================================================

# rank_HX = np.linalg.matrix_rank(HX % 2)
# rank_HZ = np.linalg.matrix_rank(HZ % 2)

# print("\nRank of HX:", rank_HX)
# print("Rank of HZ:", rank_HZ)

# ============================================================
# 5. RANK CHECK OVER GF(2)
# ============================================================

def gf2_rank(matrix):
    """
    Calculate rank of a binary matrix over GF(2).
    """

    A = matrix.copy() % 2
    rows, cols = A.shape

    rank = 0

    for col in range(cols):

        # Find a pivot row
        pivot = None

        for row in range(rank, rows):
            if A[row, col] == 1:
                pivot = row
                break

        if pivot is None:
            continue

        # Swap pivot row with current rank row
        A[[rank, pivot]] = A[[pivot, rank]]

        # Eliminate all other 1s in this column
        for row in range(rows):
            if row != rank and A[row, col] == 1:
                A[row] = (A[row] + A[rank]) % 2

        rank += 1

        if rank == rows:
            break

    return rank


rank_HX = gf2_rank(HX)
rank_HZ = gf2_rank(HZ)

print("\nRank of HX over GF(2):", rank_HX)
print("Rank of HZ over GF(2):", rank_HZ)


# ============================================================
# 6. NUMBER OF LOGICAL QUBITS
# ============================================================

k = n_qubits - rank_HX - rank_HZ

print("Number of logical qubits:", k)

# ============================================================
# 7. PAULI NOISE MODEL
# ============================================================

def generate_pauli_error(n_qubits, p):
    """
    Generate a random Pauli error on n_qubits.

    I -> no error
    X -> bit-flip error
    Y -> both X and Z component
    Z -> phase-flip error
    """

    error = np.random.choice(
        ['I', 'X', 'Y', 'Z'],
        size=n_qubits,
        p=[1 - p, p/3, p/3, p/3]
    )

    return error


# Test
p = 0.1

error = generate_pauli_error(n_qubits, p)

# ###### EXample Test with exactly 2 error
# error = np.array(['I'] * n_qubits)

# error[21] = 'X'   # q22
# error[41] = 'Z'   # q42
######### Example 

print("\nRandom Pauli error:")
print(error)

print("\nNumber of errors:", np.sum(error != 'I'))


# ============================================================
# 8. SYNDROME CALCULATION
# ============================================================

def calculate_syndrome(error, HX, HZ):
    """
    Calculate X and Z stabilizer syndromes
    for a given Pauli error.
    """

    # Convert Pauli error into binary X and Z components

    x_error = np.array([
        1 if e in ['X', 'Y'] else 0
        for e in error
    ])

    z_error = np.array([
        1 if e in ['Z', 'Y'] else 0
        for e in error
    ])

    # X stabilizers detect Z errors
    syndrome_X = (HZ @ x_error) % 2

    # Z stabilizers detect X errors
    syndrome_Z = (HX @ z_error) % 2

    return syndrome_X, syndrome_Z



# Calculate syndrome
syndrome_X, syndrome_Z = calculate_syndrome(
    error, HX, HZ
)

print("\nX-type syndrome:")
print(syndrome_X)

print("\nZ-type syndrome:")
print(syndrome_Z)

print("\nNumber of violated X-type stabilizers:",
      np.sum(syndrome_X))

print("Number of violated Z-type stabilizers:",
      np.sum(syndrome_Z))

#############
############
############
# ============================================================
# ============================================================
# 10. TORIC CODE DECODER - MINIMUM WEIGHT PERFECT MATCHING
# ============================================================

import networkx as nx


def mwpm_decoder(syndrome, error_type):
    """
    Decode a Toric Code syndrome using
    Minimum Weight Perfect Matching (MWPM).

    error_type = 'X':
        X-component errors
        Syndrome is measured by Z-type stabilizers -> HZ

    error_type = 'Z':
        Z-component errors
        Syndrome is measured by X-type stabilizers -> HX
    """

    # --------------------------------------------------------
    # 1. Select the correct parity-check matrix
    # --------------------------------------------------------

    if error_type == 'X':
        H = HZ

    elif error_type == 'Z':
        H = HX

    else:
        raise ValueError("error_type must be 'X' or 'Z'")


    # --------------------------------------------------------
    # 2. Find syndrome defects
    # --------------------------------------------------------

    defects = np.where(syndrome == 1)[0]


    # No defects -> no correction
    if len(defects) == 0:
        return np.zeros(n_qubits, dtype=int)


    # On a torus, number of defects must be even
    if len(defects) % 2 != 0:
        raise ValueError(
            "Invalid syndrome: odd number of defects."
        )


    # --------------------------------------------------------
    # 3. Build the actual syndrome graph
    # --------------------------------------------------------
    #
    # Each physical qubit connects two stabilizers.
    #
    # Therefore:
    #
    #       stabilizer ---- physical qubit ---- stabilizer
    #
    # becomes an edge in the syndrome graph.
    #
    # This automatically gives the correct lattice geometry.
    # --------------------------------------------------------

    syndrome_graph = nx.Graph()

    syndrome_graph.add_nodes_from(range(H.shape[0]))


    for q in range(n_qubits):

        # Find the two stabilizers touching physical qubit q
        connected_stabilizers = np.where(H[:, q] == 1)[0]


        if len(connected_stabilizers) != 2:
            raise ValueError(
                f"Qubit {q} is connected to "
                f"{len(connected_stabilizers)} stabilizers "
                f"instead of 2."
            )


        a, b = connected_stabilizers

        # Edge represents physical qubit q
        syndrome_graph.add_edge(
            a,
            b,
            weight=1,
            qubit=q
        )


    # --------------------------------------------------------
    # 4. Build complete graph between syndrome defects
    # --------------------------------------------------------
    #
    # Edge weight = shortest path distance
    # between two defects.
    # --------------------------------------------------------

    matching_graph = nx.Graph()

    matching_graph.add_nodes_from(defects)


    for i in range(len(defects)):

        for j in range(i + 1, len(defects)):

            a = defects[i]
            b = defects[j]

            # Shortest path on the ACTUAL toric lattice
            path = nx.shortest_path(
                syndrome_graph,
                source=a,
                target=b,
                weight="weight"
            )

            distance = len(path) - 1

            matching_graph.add_edge(
                a,
                b,
                weight=distance
            )


    # --------------------------------------------------------
    # 5. Minimum Weight Perfect Matching
    # --------------------------------------------------------

    matching = nx.algorithms.matching.min_weight_matching(
        matching_graph,
        weight="weight"
    )


    # --------------------------------------------------------
    # 6. Convert matched pairs into physical corrections
    # --------------------------------------------------------

    correction = np.zeros(n_qubits, dtype=int)


    for a, b in matching:

        # Find shortest physical path between matched defects
        path = nx.shortest_path(
            syndrome_graph,
            source=a,
            target=b,
            weight="weight"
        )


        # Every edge in this path corresponds
        # to one physical data qubit
        for u, v in zip(path[:-1], path[1:]):

            q = syndrome_graph[u][v]["qubit"]

            # Toggle the correction on that qubit
            correction[q] ^= 1


    return correction


# ============================================================
# 10.1 Decode X and Z components separately
# ============================================================

x_correction = mwpm_decoder(
    syndrome_X,
    error_type='X'
)

z_correction = mwpm_decoder(
    syndrome_Z,
    error_type='Z'
)


# ============================================================
# 10.2 Combine X and Z corrections
# ============================================================

decoded_error = np.array(['I'] * n_qubits)


for q in range(n_qubits):

    if x_correction[q] == 1 and z_correction[q] == 0:

        decoded_error[q] = 'X'

    elif x_correction[q] == 0 and z_correction[q] == 1:

        decoded_error[q] = 'Z'

    elif x_correction[q] == 1 and z_correction[q] == 1:

        decoded_error[q] = 'Y'


# ============================================================
# 10.3 Print decoded correction
# ============================================================

print("\nDecoded correction:")
print(decoded_error)

print(
    "Number of decoded errors:",
    np.sum(decoded_error != 'I')
)


# ============================================================
# 11. APPLY CORRECTION
# ============================================================

def pauli_multiply(p1, p2):

    if p1 == 'I':
        return p2

    if p2 == 'I':
        return p1

    if p1 == p2:
        return 'I'

    if {p1, p2} == {'X', 'Z'}:
        return 'Y'

    if {p1, p2} == {'X', 'Y'}:
        return 'Z'

    if {p1, p2} == {'Y', 'Z'}:
        return 'X'


def apply_correction(error, correction):

    residual = np.array(['I'] * n_qubits)

    for q in range(n_qubits):

        residual[q] = pauli_multiply(
            error[q],
            correction[q]
        )

    return residual


# ------------------------------------------------------------
# Apply decoded correction
# ------------------------------------------------------------

residual_error = apply_correction(
    error,
    decoded_error
)

print("\nResidual error after correction:")
print(residual_error)


# ------------------------------------------------------------
# Calculate residual syndrome
# ------------------------------------------------------------

residual_syndrome_X, residual_syndrome_Z = calculate_syndrome(
    residual_error,
    HX,
    HZ
)

print("\nResidual X-type syndrome:")
print(residual_syndrome_X)

print("\nResidual Z-type syndrome:")
print(residual_syndrome_Z)


# ------------------------------------------------------------
# Check whether syndrome is completely corrected
# ------------------------------------------------------------

if (
    np.all(residual_syndrome_X == 0)
    and
    np.all(residual_syndrome_Z == 0)
):

    print("\nSUCCESS: Syndrome completely corrected!")

else:

    print("\nERROR: Residual syndrome remains.")

# ============================================================
# 12. LOGICAL OPERATORS
# ============================================================

Z_L1 = np.zeros(n_qubits, dtype=int)
Z_L2 = np.zeros(n_qubits, dtype=int)

# Z_L1: horizontal non-contractible loop
# fixed x = 0, varying y
for y in range(L):
    q = horizontal_qubit(0, y)
    Z_L1[q] = 1

# Z_L2: vertical non-contractible loop
# fixed y = 0, varying x
for x in range(L):
    q = vertical_qubit(x, 0)
    Z_L2[q] = 1


# ------------------------------------------------------------
# Logical X operators
# ------------------------------------------------------------

X_L1 = np.zeros(n_qubits, dtype=int)
X_L2 = np.zeros(n_qubits, dtype=int)

# X_L1: dual loop crossing Z_L1 once
# horizontal edges with fixed y = 0, varying x
for x in range(L):
    q = horizontal_qubit(x, 0)
    X_L1[q] = 1

# X_L2: dual loop crossing Z_L2 once
# vertical edges with fixed x = 0, varying y
for y in range(L):
    q = vertical_qubit(0, y)
    X_L2[q] = 1


# ------------------------------------------------------------
# Print logical operators
# ------------------------------------------------------------

print("\nLogical operators:")

print("Z_L1:", np.where(Z_L1 == 1)[0] + 1)
print("Z_L2:", np.where(Z_L2 == 1)[0] + 1)

print("X_L1:", np.where(X_L1 == 1)[0] + 1)
print("X_L2:", np.where(X_L2 == 1)[0] + 1)


# ------------------------------------------------------------
# Logical operator commutation check
# ------------------------------------------------------------

def symplectic_commutation(x, z):
    """
    Returns 1 if two Pauli operators anticommute,
    and 0 if they commute.
    """

    return np.dot(x, z) % 2


print("\nLogical operator commutation:")

print("X_L1 with Z_L1:",
      symplectic_commutation(X_L1, Z_L1))

print("X_L1 with Z_L2:",
      symplectic_commutation(X_L1, Z_L2))

print("X_L2 with Z_L1:",
      symplectic_commutation(X_L2, Z_L1))

print("X_L2 with Z_L2:",
      symplectic_commutation(X_L2, Z_L2))

# ============================================================
# 13. LOGICAL ERROR CHECK
# ============================================================

def pauli_components(error):
    """
    Convert Pauli error into binary X and Z components.
    """

    x = np.array([
        1 if e in ['X', 'Y'] else 0
        for e in error
    ])

    z = np.array([
        1 if e in ['Z', 'Y'] else 0
        for e in error
    ])

    return x, z


def logical_commutation(error, logical_x, logical_z):
    """
    Check commutation between a Pauli error
    and a logical Pauli operator.
    """

    x_error, z_error = pauli_components(error)

    # Symplectic product
    return (
        np.dot(x_error, logical_z)
        +
        np.dot(z_error, logical_x)
    ) % 2

def is_logical_error(residual_error):

    # Calculate residual syndrome
    residual_X, residual_Z = calculate_syndrome(
        residual_error,
        HX,
        HZ
    )

    # Non-zero syndrome means a physical error remains.
    # This is NOT counted as a logical error.
    if (
        not np.all(residual_X == 0)
        or
        not np.all(residual_Z == 0)
    ):
        return False

    zero = np.zeros(n_qubits, dtype=int)

    # Check commutation with all four logical operators
    checks = [
        logical_commutation(residual_error, X_L1, zero),
        logical_commutation(residual_error, zero, Z_L1),
        logical_commutation(residual_error, X_L2, zero),
        logical_commutation(residual_error, zero, Z_L2)
    ]

    # Zero syndrome + anticommutes with a logical operator
    # means a non-trivial logical error.
    return any(check == 1 for check in checks)

# # ============================================================
# # Test logical error detection
# # ============================================================

# if decoded_error is not None:

#     logical_error = is_logical_error(residual_error)

#     print("\nLogical error check:")

#     if logical_error:
#         print("LOGICAL ERROR DETECTED")
#     else:
#         print("NO LOGICAL ERROR")

# # ============================================================
# # Test logical error detection
# # ============================================================

# test_residual = np.array(['I'] * n_qubits)

# logical_error = is_logical_error(test_residual)

# print("\nLogical error check:")
# print("LOGICAL ERROR DETECTED" if logical_error else "NO LOGICAL ERROR")


# ============================================================
# Test: deliberately create a logical X error
# ============================================================

test_residual = np.array(['I'] * n_qubits)

for q in np.where(X_L1 == 1)[0]:
    test_residual[q] = 'X'

print("\nTesting X_L1 as residual error:")

logical_error = is_logical_error(test_residual)

if logical_error:
    print("LOGICAL ERROR DETECTED")
else:
    print("NO LOGICAL ERROR")


# ============================================================
# 13.1 EXHAUSTIVE SINGLE-QUBIT ERROR TEST
# ============================================================

def test_single_qubit_error(pauli):

    failures = []

    for q in range(n_qubits):

        # Create exactly one error
        error = np.array(['I'] * n_qubits)
        error[q] = pauli

        # ----------------------------------------------------
        # Calculate syndrome
        # ----------------------------------------------------

        syndrome_X, syndrome_Z = calculate_syndrome(
            error,
            HX,
            HZ
        )

        # ----------------------------------------------------
        # Decode X component
        # ----------------------------------------------------

        x_correction = mwpm_decoder(
            syndrome_X,
            error_type='X'
        )

        # ----------------------------------------------------
        # Decode Z component
        # ----------------------------------------------------

        z_correction = mwpm_decoder(
            syndrome_Z,
            error_type='Z'
        )

        # ----------------------------------------------------
        # Construct Pauli correction
        # ----------------------------------------------------

        correction = np.array(['I'] * n_qubits)

        for i in range(n_qubits):

            if x_correction[i] == 1 and z_correction[i] == 0:
                correction[i] = 'X'

            elif x_correction[i] == 0 and z_correction[i] == 1:
                correction[i] = 'Z'

            elif x_correction[i] == 1 and z_correction[i] == 1:
                correction[i] = 'Y'

        # ----------------------------------------------------
        # Apply correction
        # ----------------------------------------------------

        residual_error = apply_correction(
            error,
            correction
        )

        # ----------------------------------------------------
        # Check residual syndrome
        # ----------------------------------------------------

        residual_X, residual_Z = calculate_syndrome(
            residual_error,
            HX,
            HZ
        )

        # ----------------------------------------------------
        # Check success
        # ----------------------------------------------------

        if (
            not np.all(residual_X == 0)
            or
            not np.all(residual_Z == 0)
            or
            is_logical_error(residual_error)
        ):
            failures.append(q)

    return failures


# ============================================================
# Run test for X, Z and Y errors
# ============================================================

x_failures = test_single_qubit_error('X')
z_failures = test_single_qubit_error('Z')
y_failures = test_single_qubit_error('Y')


# ============================================================
# Print results
# ============================================================

print("\n================================")
print("EXHAUSTIVE SINGLE-QUBIT TEST")
print("================================")

print("\nX errors:")
print("Passed:", n_qubits - len(x_failures), "/", n_qubits)
print("Failed qubits:", x_failures)

print("\nZ errors:")
print("Passed:", n_qubits - len(z_failures), "/", n_qubits)
print("Failed qubits:", z_failures)

print("\nY errors:")
print("Passed:", n_qubits - len(y_failures), "/", n_qubits)
print("Failed qubits:", y_failures)


total_failures = (
    len(x_failures)
    + len(z_failures)
    + len(y_failures)
)

print("\nTotal failures:", total_failures, "/ 150")

if total_failures == 0:
    print("SUCCESS: All 150 single-qubit errors were corrected.")
else:
    print("ERROR: Some single-qubit errors were not corrected.")

# ============================================================
# 12. SINGLE MONTE CARLO TRIAL
# ============================================================

def run_one_trial(p):

    # --------------------------------------------------------
    # 1. Generate random physical Pauli error
    # --------------------------------------------------------

    error = generate_pauli_error(
        n_qubits,
        p
    )

    # --------------------------------------------------------
    # 2. Calculate syndrome
    # --------------------------------------------------------

    syndrome_X, syndrome_Z = calculate_syndrome(
        error,
        HX,
        HZ
    )

    # --------------------------------------------------------
    # 3. Decode X component using MWPM
    # --------------------------------------------------------

    x_correction = mwpm_decoder(
        syndrome_X,
        error_type='X'
    )

    # --------------------------------------------------------
    # 4. Decode Z component using MWPM
    # --------------------------------------------------------

    z_correction = mwpm_decoder(
        syndrome_Z,
        error_type='Z'
    )

    # --------------------------------------------------------
    # 5. Construct Pauli correction
    # --------------------------------------------------------

    correction = np.array(
        ['I'] * n_qubits
    )

    for q in range(n_qubits):

        if x_correction[q] == 1 and z_correction[q] == 0:
            correction[q] = 'X'

        elif x_correction[q] == 0 and z_correction[q] == 1:
            correction[q] = 'Z'

        elif x_correction[q] == 1 and z_correction[q] == 1:
            correction[q] = 'Y'

    # --------------------------------------------------------
    # 6. Apply correction
    # --------------------------------------------------------

    residual_error = apply_correction(
        error,
        correction
    )

    # --------------------------------------------------------
    # 7. Calculate residual syndrome
    # --------------------------------------------------------

    residual_X, residual_Z = calculate_syndrome(
        residual_error,
        HX,
        HZ
    )

    # --------------------------------------------------------
    # # 8. Physical decoder success/failure
    # # --------------------------------------------------------

    # if (
    #     np.all(residual_X == 0)
    #     and
    #     np.all(residual_Z == 0)
    # ):
    #     return True

    # return False
    # 8. Decoder failure
    # --------------------------------------------------------

    if not np.all(residual_X == 0) or not np.all(residual_Z == 0):
        return False

    # Syndrome is zero, now check logical error
    if is_logical_error(residual_error):
        return False

    # Zero syndrome + no logical error
    return True

# ============================================================
# 13.2 EXHAUSTIVE TWO-QUBIT ERROR TEST
# ============================================================

def test_two_qubit_errors():

    failures = []

    paulis = ['X', 'Y', 'Z']

    # --------------------------------------------------------
    # Choose every possible pair of physical qubits
    # --------------------------------------------------------

    for q1 in range(n_qubits):

        for q2 in range(q1 + 1, n_qubits):

            # ------------------------------------------------
            # Try all 9 Pauli combinations
            # ------------------------------------------------

            for p1 in paulis:

                for p2 in paulis:

                    # Create identity error
                    error = np.array(['I'] * n_qubits)

                    # Put two errors
                    error[q1] = p1
                    error[q2] = p2

                    # ------------------------------------------------
                    # Calculate syndrome
                    # ------------------------------------------------

                    syndrome_X, syndrome_Z = calculate_syndrome(
                        error,
                        HX,
                        HZ
                    )

                    # ------------------------------------------------
                    # Decode X component
                    # ------------------------------------------------

                    x_correction = mwpm_decoder(
                        syndrome_X,
                        error_type='X'
                    )

                    # ------------------------------------------------
                    # Decode Z component
                    # ------------------------------------------------

                    z_correction = mwpm_decoder(
                        syndrome_Z,
                        error_type='Z'
                    )

                    # ------------------------------------------------
                    # Construct Pauli correction
                    # ------------------------------------------------

                    correction = np.array(['I'] * n_qubits)

                    for q in range(n_qubits):

                        if x_correction[q] == 1 and z_correction[q] == 0:
                            correction[q] = 'X'

                        elif x_correction[q] == 0 and z_correction[q] == 1:
                            correction[q] = 'Z'

                        elif x_correction[q] == 1 and z_correction[q] == 1:
                            correction[q] = 'Y'

                    # ------------------------------------------------
                    # Apply correction
                    # ------------------------------------------------

                    residual_error = apply_correction(
                        error,
                        correction
                    )

                    # ------------------------------------------------
                    # Calculate residual syndrome
                    # ------------------------------------------------

                    residual_X, residual_Z = calculate_syndrome(
                        residual_error,
                        HX,
                        HZ
                    )

                    # ------------------------------------------------
                    # Check whether decoding was successful
                    # ------------------------------------------------

                    if (
                        not np.all(residual_X == 0)
                        or
                        not np.all(residual_Z == 0)
                        or
                        is_logical_error(residual_error)
                    ):

                        failures.append(
                            (q1, q2, p1, p2)
                        )

    return failures


# ============================================================
# Run exhaustive two-qubit test
# ============================================================

two_qubit_failures = test_two_qubit_errors()


# ============================================================
# Print results
# ============================================================

total_two_qubit_cases = 1225 * 9

print("\n================================")
print("EXHAUSTIVE TWO-QUBIT TEST")
print("================================")

print(
    "Total test cases:",
    total_two_qubit_cases
)

print(
    "Passed:",
    total_two_qubit_cases - len(two_qubit_failures),
    "/",
    total_two_qubit_cases
)

print(
    "Failed:",
    len(two_qubit_failures),
    "/",
    total_two_qubit_cases
)

if len(two_qubit_failures) == 0:

    print(
        "SUCCESS: All two-qubit errors were corrected."
    )

else:

    print(
        "ERROR: Some two-qubit errors were not corrected."
    )

    print("\nFirst few failures:")
    print(two_qubit_failures[:10])

# ============================================================
# 13.3 TARGETED THREE-QUBIT ERROR TEST
# ============================================================

def test_three_qubit_errors(num_trials=1000):

    results = {
        "SUCCESS": 0,
        "LOGICAL_ERROR": 0,
        "DECODER_FAILURE": 0
    }

    paulis = ['X', 'Y', 'Z']

    for _ in range(num_trials):

        # ----------------------------------------------------
        # Randomly choose 3 different physical qubits
        # ----------------------------------------------------

        q1, q2, q3 = np.random.choice(
            n_qubits,
            size=3,
            replace=False
        )

        # ----------------------------------------------------
        # Randomly choose Pauli error on each qubit
        # ----------------------------------------------------

        p1 = np.random.choice(paulis)
        p2 = np.random.choice(paulis)
        p3 = np.random.choice(paulis)

        # ----------------------------------------------------
        # Create the 3-qubit error
        # ----------------------------------------------------

        error = np.array(['I'] * n_qubits)

        error[q1] = p1
        error[q2] = p2
        error[q3] = p3

        # ----------------------------------------------------
        # Calculate syndrome
        # ----------------------------------------------------

        syndrome_X, syndrome_Z = calculate_syndrome(
            error,
            HX,
            HZ
        )

        # ----------------------------------------------------
        # MWPM decoding
        # ----------------------------------------------------

        x_correction = mwpm_decoder(
            syndrome_X,
            error_type='X'
        )

        z_correction = mwpm_decoder(
            syndrome_Z,
            error_type='Z'
        )

        # ----------------------------------------------------
        # Construct Pauli correction
        # ----------------------------------------------------

        correction = np.array(['I'] * n_qubits)

        for q in range(n_qubits):

            if x_correction[q] == 1 and z_correction[q] == 0:
                correction[q] = 'X'

            elif x_correction[q] == 0 and z_correction[q] == 1:
                correction[q] = 'Z'

            elif x_correction[q] == 1 and z_correction[q] == 1:
                correction[q] = 'Y'

        # ----------------------------------------------------
        # Apply correction
        # ----------------------------------------------------

        residual_error = apply_correction(
            error,
            correction
        )

        # ----------------------------------------------------
        # Calculate residual syndrome
        # ----------------------------------------------------

        residual_X, residual_Z = calculate_syndrome(
            residual_error,
            HX,
            HZ
        )

        # ----------------------------------------------------
        # Classify result
        # ----------------------------------------------------

        if (
            not np.all(residual_X == 0)
            or
            not np.all(residual_Z == 0)
        ):

            results["DECODER_FAILURE"] += 1

        elif is_logical_error(residual_error):

            results["LOGICAL_ERROR"] += 1

        else:

            results["SUCCESS"] += 1

    return results


# ============================================================
# Run three-qubit test
# ============================================================

three_qubit_results = test_three_qubit_errors(
    num_trials=1000
)


# ============================================================
# Print results
# ============================================================

print("\n================================")
print("TARGETED THREE-QUBIT TEST")
print("================================")

print("Number of trials:", 1000)

print(
    "Successful corrections:",
    three_qubit_results["SUCCESS"]
)

print(
    "Logical errors:",
    three_qubit_results["LOGICAL_ERROR"]
)

print(
    "Decoder failures:",
    three_qubit_results["DECODER_FAILURE"]
)

# ============================================================
# 13. MONTE CARLO SIMULATION
# ============================================================

#### for single trial
# result = run_one_trial(0.02)

# print("\nMonte Carlo single trial:")
# print("SUCCESS" if result else "FAILURE")
######### for check only

# # ============================================================
# # 13. MONTE CARLO SIMULATION
# # ============================================================

def monte_carlo(p, num_trials=1000):

    successes = 0
    failures = 0

    for _ in range(num_trials):

        result = run_one_trial(p)

        if result:
            successes += 1
        else:
            failures += 1

    success_rate = successes / num_trials
    failure_rate = failures / num_trials

    return success_rate, failure_rate      #THIS WAS FOR BINARY SYNDROME NOT FOR MWPM DECODER


# Run simulation
p = 0.02
num_trials = 1000

success_rate, failure_rate = monte_carlo(
    p,
    num_trials
)

print("\n================================")
print("MONTE CARLO RESULTS")
print("================================")

print("Physical error probability:", p)
print("Number of trials:", num_trials)

print("Successful trials:", int(success_rate * num_trials))
print("Failed trials:", int(failure_rate * num_trials))

print("Success rate:", success_rate)
print("Failure rate:", failure_rate)

# ============================================================
# 14. MONTE CARLO FOR DIFFERENT ERROR PROBABILITIES
# ============================================================

p_values = [0.01, 0.02, 0.03, 0.04, 0.05,
            0.06, 0.07, 0.08, 0.09, 0.10]

failure_rates = []

num_trials = 1000

for p in p_values:

    success_rate, failure_rate = monte_carlo(
        p,
        num_trials
    )

    failure_rates.append(failure_rate)

    print(
        f"p = {p:.2f} | "
        f"Success rate = {success_rate:.3f} | "
        f"Failure rate = {failure_rate:.3f}"
    )

# ============================================================
# 15. PLOT: PHYSICAL ERROR RATE vs FAILURE RATE
# Physical error probability vs decoder failure rate using MWPM
# ============================================================

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.plot(
    p_values,
    failure_rates,
    marker='o'
)

plt.xlabel("Physical Error Probability (p)")
plt.ylabel("Decoder Failure Rate")

plt.title("Toric Code: Physical Error Probability vs decoder failure rate")

plt.grid(True)

plt.show()

# ============================================================
# 16. LOGICAL ERROR RATE
# ============================================================

def run_one_logical_trial(p):

    # --------------------------------------------------------
    # 1. Generate random physical error
    # --------------------------------------------------------

    error = generate_pauli_error(
        n_qubits,
        p
    )

    # --------------------------------------------------------
    # 2. Calculate syndrome
    # --------------------------------------------------------

    syndrome_X, syndrome_Z = calculate_syndrome(
        error,
        HX,
        HZ
    )

    # --------------------------------------------------------
    # 3. MWPM decoding
    # --------------------------------------------------------

    x_correction = mwpm_decoder(
        syndrome_X,
        error_type='X'
    )

    z_correction = mwpm_decoder(
        syndrome_Z,
        error_type='Z'
    )

    # --------------------------------------------------------
    # 4. Construct Pauli correction
    # --------------------------------------------------------

    correction = np.array(
        ['I'] * n_qubits
    )

    for q in range(n_qubits):

        if x_correction[q] == 1 and z_correction[q] == 0:
            correction[q] = 'X'

        elif x_correction[q] == 0 and z_correction[q] == 1:
            correction[q] = 'Z'

        elif x_correction[q] == 1 and z_correction[q] == 1:
            correction[q] = 'Y'

    # --------------------------------------------------------
    # 5. Apply correction
    # --------------------------------------------------------

    residual_error = apply_correction(
        error,
        correction
    )

    # --------------------------------------------------------
    # 6. Check residual syndrome
    # --------------------------------------------------------

    residual_X, residual_Z = calculate_syndrome(
        residual_error,
        HX,
        HZ
    )

    # --------------------------------------------------------
    # 7. Residual physical error
    # --------------------------------------------------------

    if (
        not np.all(residual_X == 0)
        or
        not np.all(residual_Z == 0)
    ):
        return "DECODER_FAILURE"

    # --------------------------------------------------------
    # 8. Check logical error
    # --------------------------------------------------------

    if is_logical_error(residual_error):
        return "LOGICAL_ERROR"

    # --------------------------------------------------------
    # 9. Successful correction
    # --------------------------------------------------------

    return "SUCCESS"

# ============================================================
# SINGLE LOGICAL TRIAL
# ============================================================

p = 0.02

result = run_one_logical_trial(p)

print("\n================================")
print("SINGLE LOGICAL TRIAL")
print("================================")
print("Physical error probability:", p)
print("Result:", result)


# ============================================================
# 17. MONTE CARLO FOR LOGICAL ERROR RATE
# ============================================================

def monte_carlo_logical(p, num_trials=1000):

    successes = 0
    decoder_failures = 0
    logical_errors = 0

    for _ in range(num_trials):

        result = run_one_logical_trial(p)

        if result == "SUCCESS":
            successes += 1

        elif result == "DECODER_FAILURE":
            decoder_failures += 1

        elif result == "LOGICAL_ERROR":
            logical_errors += 1

    success_rate = successes / num_trials
    decoder_failure_rate = decoder_failures / num_trials
    logical_error_rate = logical_errors / num_trials

    return (
        success_rate,
        decoder_failure_rate,
        logical_error_rate
    )

# ============================================================
# 18. LOGICAL ERROR RESULTS
# ============================================================

logical_error_rates = []
logical_decoder_failures = []
logical_success_rates = []

num_trials = 10000

print("\n================================")
print("LOGICAL ERROR RATE RESULTS")
print("================================")

for p in p_values:

    success_rate, decoder_failure_rate, logical_error_rate = (
        monte_carlo_logical(p, num_trials)
    )

    logical_success_rates.append(success_rate)
    logical_decoder_failures.append(decoder_failure_rate)
    logical_error_rates.append(logical_error_rate)

    print(
        f"p = {p:.2f} | "
        f"Success = {success_rate:.3f} | "
        f"Decoder failure = {decoder_failure_rate:.3f} | "
        f"Logical error = {logical_error_rate:.3f}"
    )



# ============================================================
# 19. PLOT: PHYSICAL ERROR PROBABILITY vs LOGICAL ERROR RATE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    p_values,
    logical_error_rates,
    marker='o'
)

plt.xlabel("Physical Error Probability (p)")
plt.ylabel("Logical Error Rate")

plt.title(
    "Toric Code: Physical Error Probability vs Logical Error Rate"
)

plt.grid(True)

plt.show()



