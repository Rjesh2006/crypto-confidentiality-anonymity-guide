# using dictionary 
my_dict = {
    1: "alpha",
    2: "bravo",
    3: "charlie",
    4: "delta",
    5: "echo",
    6: "magic"
}
attempt=0
secret_password = "magic"

for key, word in my_dict.items():
    print(f"Trying: {word}")
    attempt += 1
    if word == secret_password:
        print(f"Password found! It is: {word}")
        break
print (f"attempt: {attempt}")


# using string
import itertools

def brute_force_numeric(password, max_length=6):
    digits = '0123456789'
    attempts = 0

    for length in range(1, max_length + 1):
        for guess in map(''.join, itertools.product(digits, repeat=length)):
            attempts += 1
            if guess == password:
                print(f"Password found: {guess}")
                print(f"Attempts: {attempts}")
                return guess
    print("Password not found.")
    return None

# Example usage
password = "1234"
brute_force_numeric(password, max_length=4)
