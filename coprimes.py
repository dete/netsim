prime_numbers = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 
                 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]

for n in range(25, 37):
    for p in prime_numbers:
        print(f"{n} - {p%n}")