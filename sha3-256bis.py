import hashlib

def sha3_256_file(filename):
    sha3 = hashlib.sha3_256()

    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha3.update(chunk)

    return sha3.hexdigest()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sha3_256.py <filename>")
    else:
        filename = sys.argv[1]
        result = sha3_256_file(filename)
        print(f'SHA3-256 ({filename}) = {result}')
