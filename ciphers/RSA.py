# RSA Algorithm: Digital Signature Version
# Switch public key and private key

from textwrap import wrap
from typing import List, Tuple

from .utils import PrimeGenerator


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
def rsa_encryption(message: str, private_key: Tuple[int, int]) -> str:
    e, n = private_key
    block_size = len(str(n))
    padding_message = convert_and_padding(message, block_size - 1)

    m = text_to_block(padding_message, block_size - 1)
    c = []
    for block in m:
        ci = pow(block, e, n)
        c.append(ci)

    return format(int(block_to_text(c, block_size)), '064x')


# Decrypt the ciphertext with RSA Algorithm
def rsa_decryption(ciphertext: str, public_key: Tuple[int, int]) -> str:
    d, n = public_key
    block_size = len(str(n))
    padding_ciphertext = convert_and_padding(ciphertext, block_size)

    c = text_to_block(padding_ciphertext, block_size)
    m = []
    for block in c:
        mi = pow(block, d, n)
        m.append(mi)
    return format(int(block_to_text(m, block_size - 1)), '064x')


# Generate rsa key
def generate_rsa_key():
    p = PrimeGenerator.random()
    q = PrimeGenerator.random()
    n = p * q
    toi = (p - 1) * (q - 1)
    e = PrimeGenerator.random()
    d = pow(e, -1, toi)
    private_key = [e, n]
    public_key = [d, n]
    return [private_key, public_key]


# Add padding to the message so its length divisible by block size
def convert_and_padding(message: str, block_size: int):
    int_message = str(int(message, 16))
    length = len(int_message)
    padding_length = block_size - (length % block_size)
    padding = "0" * padding_length
    return padding + int_message


# Main program to test
if __name__ == "__main__":
    private_key, public_key = generate_rsa_key()
    with open('test/default.pub', 'w') as f:
        f.write(str(public_key))
    with open('test/default.pri', 'w') as f:
        f.write(str(private_key))
    count = 0
    tries = 10
    for i in range(tries):
        private_key, public_key = generate_rsa_key()
        # print("Nilai p dan q\t\t:", p, ",", q)
        # print("Nilai n dan toi\t\t:", n, ",", toi)
        print("Private key (e, n)\t:", private_key[0], ",", private_key[1])
        print("Public key (d, n)\t:", public_key[0], ",", public_key[1])

        # Contoh Penggunaan: Noted untuk Jojo
        with open('test/surat.txt', 'rb') as f:
            text_bytes = f.read()
        message = "02c15036e137e4f03c000df14f2dd365fc9f209cd5ddbf143daed5cbad8c7e52"
        print("Plaintext\t\t:", message)

        ciphertext = rsa_encryption(message, private_key)
        print("Ciphertext\t\t:", ciphertext)

        decrypted_ciphertext = rsa_decryption(ciphertext, public_key)
        print("Decrypted ciphertext\t:", decrypted_ciphertext)

        if (decrypted_ciphertext == message):
            print("PASSED", end="\n\n")
            count += 1

    print("Dari", tries, "percobaan, persentase berhasil adalah: ", end="")
    print(int(count * 100 / float(tries)), "%")
