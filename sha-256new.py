import sys
import binascii

from permutation import chi, theta, rho, pi, iota

"""
    Fonction  d'initialisation de l'algorithme
    args: 
        message: correspond au flux d'entrée
        r : le nombre de bits par bloc de sortie

"""
def pad(message, r):
    # Padding function according to SHA-3 standard
    binary_message = ''.join(format(char, '08b') for char in message)
    
    # Adding the final '1' bit
    binary_message += '1'
    
    # Calculate the number of zero bits needed
    zero_bits = (r - len(binary_message)) % r
    binary_message += '0' * (zero_bits - 1)

    #binary_message += format(0x1F, '08b')
    # Ensuring the total length is a multiple of the block size
    #while len(binary_message) % r != 0:
     #   binary_message += '0'
    binary_message += '1'

    return binary_message






  
def xor_state(state, block):
    # XOR each lane of the state with the corresponding block
    for i in range(5):
        for j in range(5):
            # Check if the block has enough elements
            if i < len(block) and j < len(block[i]):
                # XOR individual elements of the state and block
                state[i][j] ^= block[i][j]

    return state




def state_to_bits(state):
    # Convertir les chaînes de bits en une seule chaîne binaire
    return ''.join(''.join(str(bit) for bit in row) for row in state)



def keccak_f(state, w):
    # Perform the rounds
    for i in range(24):  # (12 + 2 * l) pour 64 bit l=6
        state = theta(state, w)
        state = rho(state, w)
        state = pi(state, w)
        state = chi(state, w)
        state = iota(state, i, w)

    # Convertir les entiers de grande taille en bits individuels
    for x in range(5):
        for y in range(5):
            state[x][y] = format(state[x][y], '064b')[-w:]

    return state

    

def sponge(message, r, d):
    w = 64  # Using w=64 for SHA-3

    # Padding the input message
    padded_message = pad(message, r)

    # Breaking the padded message into blocks
    blocks = [padded_message[i:i + r] for i in range(0, len(padded_message), r)]

    # Initialize the state
    state = [[0] * 5 for _ in range(5)]

    # Absorb phase
    for block in blocks:
        # Reshape block to match the dimensions of state[i][j]
        block_reshaped = [[int(bit) for bit in row] for row in zip(*[iter(block)] * 8)]

        state = xor_state(state, block_reshaped)

        print(f'State After XOR:\n{state}')  # Ajout d'une impression pour suivre le déroulement

        state = keccak_f(state, w)

        print(f'State After Keccak_f:\n{state}')  # Ajout d'une impression pour suivre le déroulement

    # Squeeze phase
    output = state_to_bits(state)[:d]

    print(f'Binary Output:\n{output}')  # Ajout d'une impression pour suivre le déroulement

    # Convert the binary string to a hex string
    hex_output = hex(int(output, 2))[2:]
    #hex_output = format(int(output, 2), f'0{len(output)//4}x')



    # Ensure the hex string has the correct length
    hex_output = hex_output.zfill(len(hex_output) + len(hex_output) % 2)

    return hex_output






#capacity = 512 r = 1088, ns = 256
def print_sha3_256(data_name, data):
    r = 1088  # taille des blocs
    ns = 256   # Nombre de blocs de sortie 

    hash_value = sponge(data, r, ns)
    hash_bytes = binascii.unhexlify(hash_value)
    hash_hex = binascii.hexlify(hash_bytes).decode()
    print(f'SHA3-256 ({data_name}) = {hash_hex}')


if __name__ == "__main__":
    files = sys.argv[1:]
    
    if not files:
        # Lecture à partir de l'entrée standard
        data_name = "stdin"
        data = sys.stdin.buffer.read()
        print_sha3_256(data_name, data)
    else:
        for file_path in files:
            with open(file_path, 'rb') as file: # en r cela marche et rb ca MARCHE PAAAS
                data_name = file_path
                data = file.read()
                print_sha3_256(data_name, data)
