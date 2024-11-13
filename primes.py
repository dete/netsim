import sympy

def cheeky_prime_test(n):
    if n in [2, 3, 5]:
        return True
    if n < 2 or (n % 2) == 0 or (n % 3) == 0 or (n % 5) == 0:
        return False
    if n < 49:
        return True
    if (n %  7) == 0 or (n % 11) == 0 or (n % 13) == 0 or (n % 17) == 0 or \
       (n % 19) == 0 or (n % 23) == 0 or (n % 29) == 0 or (n % 31) == 0 or \
       (n % 37) == 0 or (n % 41) == 0 or (n % 43) == 0 or (n % 47) == 0:
        return False
    if n < 2809:
        return True
    if n < 65077:
        if n in [8321, 31621, 42799, 49141, 49981]:
            return False
        else:
            return pow(2, n >> 1, n) in [1, n - 1]

    if n < 341531:
        return miller_rabin(n, [9345883071009581737])
    if n < 885594169:
        return miller_rabin(n, [725270293939359937, 3569819667048198375])

    return False


def miller_rabin(n, bases):
    # Write n - 1 as d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Test each base
    for a in bases:
        if a >= n:
            a %= n
        if a < 2:
            return True

        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Checking all numbers from 1 to 1,000,000 against both Miller-Rabin and sympy's isprime for comparison
limit = 1000000
import time

for i in range(limit):
    if cheeky_prime_test(i) != sympy.isprime(i):
        print(f"{i} mismatch: {cheeky_prime_test(i)} {sympy.isprime(i)}")
        exit()

# start_time = time.time()
# miller_rabin_results = [miller_rabin(n) for n in range(1, limit + 1)]
# miller_rabin_time = time.time() - start_time
# print(f"Miller-Rabin test took {miller_rabin_time:.2f} seconds")

start_time = time.time()
cheeky_results = [cheeky_prime_test(n) for n in range(1, limit + 1)]
cheeky_time = time.time() - start_time
print(f"Cheeky test took {cheeky_time:.2f} seconds")

start_time = time.time()
sympy_results = [sympy.isprime(n) for n in range(1, limit + 1)]
sympy_time = time.time() - start_time
print(f"Sympy test took {sympy_time:.2f} seconds")

# Check how many results matched and if there were any mismatches
# mismatch_count = sum(1 for i in range(limit) if miller_rabin_results[i] != sympy_results[i])
# print(f"Mismatch count: {mismatch_count}")
