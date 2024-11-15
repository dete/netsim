big_primes = [
    1050102301, 1247853853, 1491637913, 1555099697, 1770895913, 2360565041, 2699967689, 3543971273,
    3928052101, 4427000933, 5211180353, 5362167379, 5494099469, 5571094003, 5631892697, 5643215959,
    5780515193, 5971283867, 5992374977, 6298234643, 6395295623, 6465897299, 7287098869, 7458436879,
    7515392509, 7775304011, 7783469821, 7898758529, 8255153561, 8263242319, 8572194353, 9669899927]

def extract_params(n, salt):
    coprime = big_primes[(salt & 0xFFFFFFFF) % len(big_primes)] % n
    salt = salt >> 32

    offset = (salt & 0xFFFFFFFF) % n
    salt = salt >> 32

    mask_length = n.bit_length()-1
    mask_range = 1 << mask_length
    mask = mask_range - 1
    xor_mask = salt & mask

    return coprime, offset, mask_range, xor_mask

def permute(i, n, salt):
    coprime, offset, mask_range, xor_mask = extract_params(n, salt)
    result = (i * coprime + offset) % n
    if result < mask_range:
        result ^= xor_mask
    return result

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

def inverse(y, n, salt):
    coprime, offset, mask_range, xor_mask = extract_params(n, salt)
    if y < mask_range:
        y ^= xor_mask
    return ((y + n - offset) * modinv(coprime, n)) % n

# Example usage
for n in range(10, 257):
    import random
    import mmh3

    # NOTE: In production, we'll use the secure hash of the message as the salt, so
    # for testing, we use a simple hash function that has good distribution properties.
    salt = mmh3.hash128("permute", seed=random.randint(0, 2**32-1))

    # Test the bijection and its inverse
    print(f"n: {n}, salt: {salt}")
    coprime, offset, mask_range, xor_mask = extract_params(n, salt)
    print(f"coprime: {coprime}, offset: {offset}, mask_range: {mask_range}, xor_mask: {xor_mask}\n--")

    for i in range(n):
        permuted = permute(i, n, salt)
        assert permuted < n and permuted >= 0 # Ensure the result is in the range [0, n)
        inversed = inverse(permuted, n, salt)
        # print(f"Original: {i}, Permuted: {permuted}, Inversed: {inversed}")
        assert inversed == i  # Ensure invertibility