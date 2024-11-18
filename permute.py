from typing import NamedTuple

big_primes = [
    1050102301, 1247853853, 1491637913, 1555099697, 1770895913, 2360565041, 2699967689, 3543971273,
    3928052101, 4427000933, 5211180353, 5362167379, 5494099469, 5571094003, 5631892697, 5643215959,
    5780515193, 5971283867, 5992374977, 6298234643, 6395295623, 6465897299, 7287098869, 7458436879,
    7515392509, 7775304011, 7783469821, 7898758529, 8255153561, 8263242319, 8572194353, 9669899927]

class Params(NamedTuple):
    n: int
    cp1: int
    cp2: int
    inv1: int
    inv2: int
    offset1: int
    offset2: int
    xor_range: int
    xor1: int
    xor2: int

def modinv(a, n):
    # Iterative implementation of the Extended Euclidean Algorithm
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r != 1:
        raise Exception(f"No modular inverse for a={a} modulo n={n}")
    if t < 0:
        t += n
    return t


def create_params(n, salt):
    cp1 = big_primes[salt % len(big_primes)] % n
    inv1 = modinv(cp1, n)
    salt = salt >> 8
    offset1 = salt % n
    salt = salt >> 24

    cp2 = big_primes[salt % len(big_primes)] % n
    inv2 = modinv(cp2, n)
    salt = salt >> 8
    offset2 = salt % n
    salt = salt >> 24

    xor_range = 1 << n.bit_length()-1
    xor_mask = xor_range - 1

    xor1 = salt & xor_mask
    salt = salt >> 32

    xor2 = salt & xor_mask
    salt = salt >> 32

    return Params(n, cp1, cp2, inv1, inv2, offset1, offset2, xor_range, xor1, xor2)

def permute(i, p):
    result = i

    # XOR the result with the first xor value if it's in the range
    if result < p.xor_range:
        result ^= p.xor1

    # Apply the first linear transformation
    result = (result * p.cp1 + p.offset1) % p.n

    # XOR the result with the second xor value if it's in the range
    if result < p.xor_range:
        result ^= p.xor2

    # Apply the second linear transformation
    result = (result * p.cp2 + p.offset2) % p.n

    return result

def inverse(y, p):
    result = y

    # Undo the second linear transformation
    result = ((result + p.n - p.offset2) * p.inv2) % p.n

    # Undo the second XOR (if it's in range)
    if result < p.xor_range:
        result ^= p.xor2

    # Undo the first linear transformation
    result = ((result + p.n - p.offset1) * p.inv1) % p.n

    # Undo the first XOR (if it's in range)
    if result < p.xor_range:
        result ^= p.xor1

    return result

# Example usage
for n in range(10, 10000):
    import random
    import mmh3

    # NOTE: In production, we'll use the secure hash of the message as the salt, so
    # for testing, we use a simple hash function that has good distribution properties.
    salt = mmh3.hash128("permute", seed=random.randint(0, 2**32-1))

    # # Test the bijection and its inverse
    # print(f"n: {n}, salt: 0x{salt:016x}")
    params = create_params(n, salt)
    # print(f"cp1: {params.cp1}, inv1: {params.inv1}, offset1: {params.offset1}, "
    #       f"cp2: {params.cp2}, inv2: {params.inv2}, offset2: {params.offset2}, "
    #       f"xor_range: {params.xor_range}, xor1: 0x{params.xor1:04x}, xor2: 0x{params.xor2:04x}")

    for i in range(n):
        permuted = permute(i, params)
        assert permuted < n and permuted >= 0 # Ensure the result is in the range [0, n)
        inversed = inverse(permuted, params)
        # print(f"Original: {i}, Permuted: {permuted}, Inversed: {inversed}")
        assert inversed == i  # Ensure invertibility