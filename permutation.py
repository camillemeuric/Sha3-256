def rotate_left(x, n, w):
    return ((x << n) | (x >> (w - n))) % (1 << w)
"""
    Calculer la parité des 5×w colonnes (de 5 bits) de l’état, 
    puis calculer le ou exclusif entre deux colonnes voisines. 
    C[x] = A[x, 0] ⊕ A[x, 1] ⊕ A[x, 2] ⊕ A[x, 3] ⊕ A[x, 4] , x = 0, 1, 2, 3, 4
    D[x] = C[x − 1] ⊕ rot(C[x + 1], 1) , x = 0, 1, 2, 3, 4
    A[x, y] = A[x, y] ⊕ D[x] , x, y = 0, 1, 2, 3, 4
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


def liste_tri_dim(w):
    B = []
    for i in range(5):
        C = []
        for j in range(5):
            C.append([0] * w)
        B.append(C)
    return B


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
def pi(A, w):
    #B = [[[0] * w for i in range(5)] for i in range(5)]
    B = liste_tri_dim(w)

    for x in range(5):
        for y in range(5):
            B[y][(2 * x + 3 * y) % 5] = A[x][y]
            #B[(3 * x + 2 * y) % 5][x] = A[x][y]

    return B

def chi(A, w):
    B = liste_tri_dim(w)

    for x in range(5):
        for y in range(5):
            B[x][y] = A[x][y] ^ ((~A[(x + 1) % 5][y]) & A[(x + 2) % 5][y])

    return B


#constant RC[i] differs depending on which round i is being executed. 

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

    # XOR the lane at [0, 0] with the corresponding round constant
    A[0][0] = A[0][0] ^ RC[round_index]

    return A


