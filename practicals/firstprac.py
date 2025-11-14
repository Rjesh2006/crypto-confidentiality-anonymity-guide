import random
my_dict = {
    1: "alpha",
    2: "bravo",
    3: "charlie",
    4: "delta",
    5: "echo",
    6: "magic"
}

def generate_password(dictionary, length):
    values = list(dictionary.values())          
    selected_values = [random.choice(values) for i in range(length)]  
    password = " ".join(selected_values)       
    return password, selected_values

password_length = 5
new_password, selected_values = generate_password(my_dict, password_length)

print(f"Generated Password: {new_password}")
print(f"Values Selected: {selected_values}")
