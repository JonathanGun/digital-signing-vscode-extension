# RSA Algorithm

from textwrap import wrap
from typing import List, Tuple
from utils import PrimeGenerator

def text_to_block(message: str, block_size: int) -> List[int]:
    messages = list(map(int, wrap(message, block_size)))
    return messages

def block_to_text(m: List[int], block_size: int) -> str:
    output = []
    print_format = "0" + str(block_size) + "d"
    for block in m:
        output.append(format(block, print_format))
    return "".join(output)

# Encrypt the ciphertext with RSA Algorithm
def rsa_encryption(message: str, public_key: Tuple[int, int]) -> str:
    e, n = public_key
    block_size = len(str(n))
    padding_message = convert_and_padding(message, block_size - 1)
    
    m = text_to_block(padding_message, block_size - 1)
    c = []
    for block in m:
        ci = pow(block, e, n)
        c.append(ci)

    return format(int(block_to_text(c, block_size)), '32x')

# Decrypt the ciphertext with RSA Algorithm
def rsa_decryption(ciphertext: str, private_key: Tuple[int, int]) -> str:
    d, n = private_key
    block_size = len(str(n))
    padding_ciphertext = convert_and_padding(ciphertext, block_size)
    
    c = text_to_block(padding_ciphertext, block_size)
    m = []
    for block in c:
        mi = pow(block, d, n)
        m.append(mi)
    
    return format(int(block_to_text(m, block_size - 1)), '32x')

# Generate rsa key
def generate_rsa_key():
    p = PrimeGenerator.random()
    q = PrimeGenerator.random()
    n = p * q
    toi = (p - 1) * (q - 1)
    e = PrimeGenerator.random()
    d = pow(e, -1, toi)
    public_key = [e, n]
    private_key = [d, n]
    return [public_key, private_key]

# Add padding to the message so its length divisible by block size
def convert_and_padding(message: str, block_size: int):
    int_message = str(int(message, 16))
    length = len(int_message)
    padding_length = block_size - (length % block_size)
    padding = "0" * padding_length
    return padding + int_message

# Main program to test
if (__name__ == "__main__"):
    count = 0
    tries = 500
    for i in range(tries):
        p = PrimeGenerator.random()
        q = PrimeGenerator.random()
        n = p * q
        toi = (p - 1) * (q - 1)
        e = PrimeGenerator.random()

        d = pow(e, -1, toi)
        public_key = (e, n)
        private_key = (d, n)
        print("Nilai p dan q\t\t:", p, ",", q)
        print("Nilai n dan toi\t\t:", n, ",", toi)
        print("Public key (e, n)\t:", public_key[0], ",", public_key[1])
        print("Private key (d, n)\t:", public_key[0], ",", public_key[1])

        with open ('../test/test-1.txt', 'rb') as f:
            text = f.read()
        
        # Contoh Penggunaan: Noted untuk Jojo
        message = "5e4cd91d2e1599bb7e649f535dfaa570b012dc7fd9af39fc700d716d20b34f2b"
        print("Plaintext\t\t:", message)

        ciphertext = rsa_encryption(message, public_key)
        print("Ciphertext\t\t:", ciphertext)

        decrypted_ciphertext = rsa_decryption(ciphertext, private_key)
        print("Decrypted ciphertext\t:", decrypted_ciphertext)

        if (decrypted_ciphertext == message):
            print("PASSED", end="\n\n")
            count += 1

    print("Dari", tries, "percobaan, persentase berhasil adalah: ", end="")
    print(int(count * 100 / float(tries)), "%")