# RC table
RC = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008
]

def rot(W, r):
    return ((W >> (64 - (r % 64))) + (W << (r % 64))) % (1 << 64)

def round(A, RC):
    # θ
    C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
    #print(C)
    D = [C[x-1] ^  rot(C[(x+1) % 5], 1) for x in range(5)]
    #print(D)
    A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]
    #print(A)

    # ρ dan π
    (x, y) = (1, 0)
    cur = A[x][y]
    for t in range(24):
        (x, y) = (y, (2*x + 3*y) % 5)
        old_cur = cur
        cur = A[x][y]
        A[x][y] = rot(old_cur, (t+1)*(t+2)//2)
    #print(A)
    
    # χ
    for y in range(5):
        B = [A[x][y] for x in range(5)]
        for x in range(5):
            A[x][y] = B[x] ^ ((~B[(x+1) % 5]) & B[(x+2) % 5])

    # ι
    A[0][0] ^= RC

    return A

def get(x):
    sum = 0
    for i in range(8):
        sum += x[i] << (8*i)
    return sum

def put(x):
    return list((x >> (8*i)) % 256 for i in range(8))

def keccakPermutation(state):
    A = [[get(state[8*(x+5*y) : 8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
    #print(A)
    # 24 Round
    for i in range(24):
        A = round(A, RC[i])
    #print(A)
    state = bytearray(200)
    for x in range(5):
        for y in range(5):
            state[8*(x+5*y) : 8*(x+5*y)+8] = put(A[x][y])
    return state

def keccak(r, c, inputBytes, d, outputBytesLen):
    state = bytearray(200)
    rInBytes = r//8
    nBlock = 0
    i = 0
    # Absorbing
    while (i < len(inputBytes)):
        nBlock = min(len(inputBytes) - i, rInBytes)
        for idx in range(nBlock):
            # XOR setiap elemen S (state) dengan blok Pi (input)
            state[idx] ^= inputBytes[idx + i]
        i += nBlock
        if (nBlock == rInBytes):
            state = keccakPermutation(state)
            #print(state)
            nBlock = 0
    #print(state)

    # Padding
    state[nBlock] ^= d
    if (((d & 0x80) != 0) and (nBlock == (rInBytes-1))):
        state = keccakPermutation(state)
    state[rInBytes-1] ^= 0x80
    #print(state)
    state = keccakPermutation(state)
    #print(state)
    
    # Squeezing
    Z = bytearray()
    while(outputBytesLen > 0):
        nBlock = min(outputBytesLen, rInBytes)
        Z += state[0:nBlock]
        outputBytesLen -= nBlock
        if (outputBytesLen > 0):
            state = keccakPermutation(state)
    return Z

# SHA3-256
print(keccak(1088, 512, b'hehehe\r\n', 0x06, 256//8).hex())