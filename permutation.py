"""
    Effectue une rotation circulaire vers la gauche sur un entier.

    Args:
        x (int): L'entier à rotationner.
        n (int): Le nombre de bits à décaler.
        w (int): La largeur de l'entier en bits.

    Returns:
        int: L'entier après la rotation.
"""
def rotate_left(x, n, w):
    return ((x << n) | (x >> (w - n))) % (1 << w)

"""
    Applique l'opération de permutation Theta à la matrice d'état A.

    Args:
        A (list): La matrice d'état.
        w (int): La largeur des mots en bits.
    Returns:
        list: La matrice d'état mise à jour après l'opération Theta.
"""
def theta(A, w):
    C = [0] * 5
    D = [0] * 5

    for x in range(5):
        C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]

    for x in range(5):
        D[x] = C[(x - 1) % 5] ^ rotate_left(C[(x + 1) % 5], 1, w)#calcul indices modulo 5 pour A[i][j]
    for x in range(5):
        for y in range(5):
            A[x][y] = A[x][y] ^ D[x]

    return A

"""
    Crée une liste tridimensionnelle de largeur w remplie de zéros.

    Args:
        w (int): La largeur des mots en bits.

    Returns:
        list: Une liste tridimensionnelle remplie de zéros.
"""
def liste_tri_dim(w):
    B = []
    for i in range(5):
        C = []
        for j in range(5):
            C.append([0] * w)
        B.append(C)
    return B

"""
    Applique l'opération de permutation Rho à la matrice d'état A.

    Args:
        A (list): La matrice d'état.
        w (int): La largeur des mots en bits.

    Returns:
        list: La matrice d'état mise à jour après l'opération Rho.
"""
def rho(A, w):
    #C = [[[0] * w for _ in range(5)] for _ in range(5)]
    B = liste_tri_dim(w)

    # Rotation constants (rotation offsets)
    rotation_offsets = [
        [  0,  1, 62, 28, 27, ],
        [ 36, 44,  6, 55, 20, ],
        [  3, 10, 43, 25, 39, ],
        [ 41, 45, 15, 21,  8, ],
        [ 18,  2, 61, 56, 14, ]
    ]

    for x in range(5):
        for y in range(5):
            B[x][y] = rotate_left(A[x][y], rotation_offsets[x][y], w)

    return B

"""
Permutation des 25 mots avec un motif fixé:
a[3i+2j][i] = a[i][j]
"""
"""
    Applique l'opération de permutation Pi à la matrice d'état A.

    Args:
        A (list): La matrice d'état.
        w (int): La largeur des mots en bits.

    Returns:
        list: La matrice d'état mise à jour après l'opération Pi.
"""
def pi(A, w):
    B = liste_tri_dim(w)

    for x in range(5):
        for y in range(5):
            B[y][(2 * x + 3 * y) % 5] = A[x][y]
            #B[(3 * x + 2 * y) % 5][x] = A[x][y]

    return B

"""
    Applique l'opération de permutation Chi à la matrice d'état A.

    Args:
        A (list): La matrice d'état.
        w (int): La largeur des mots en bits.

    Returns:
        list: La matrice d'état mise à jour après l'opération Chi.
"""
def chi(A, w):
    B = liste_tri_dim(w)

    for x in range(5):
        for y in range(5):
            B[x][y] = A[x][y] ^ ((~A[(x + 1) % 5][y]) & A[(x + 2) % 5][y])

    return B



"""
    Applique l'opération de permutation Iota à la matrice d'état A.

    Args:
        A (list): La matrice d'état.
        round_index (int): L'indice du tour.
        w (int): La largeur des mots en bits.

    Returns:
        list: La matrice d'état mise à jour après l'opération Iota.
"""
def iota(A, round_index, w):
    # Round constants for SHA-3 (64 bits each)
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
        0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]

    #constant RC[i] differs depending on which round i is being executed. 
    A[0][0] = A[0][0] ^ RC[round_index]

    return A


