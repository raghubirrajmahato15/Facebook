import random

def generate_usernames(num_usernames, common_numbers):
    if common_numbers == 1:
        first_digit = int(input("Enter the first common digit (0-9): "))
        random_digits_list = [''.join(random.choices('0123456789', k=9)) for _ in range(num_usernames)]
        usernames = [f"{first_digit}{random_digits}" for random_digits in random_digits_list]
    elif common_numbers == 2:
        first_digit1 = int(input("Enter the first common digit (0-9): "))
        first_digit2 = int(input("Enter the second common digit (0-9): "))
        random_digits_list = [''.join(random.choices('0123456789', k=8)) for _ in range(num_usernames)]
        usernames = [f"{first_digit1}{first_digit2}{random_digits}" for random_digits in random_digits_list]
    else:
        print("Invalid input! Please enter 1 or 2 for common numbers.")
        return []

    return usernames

def save_usernames(usernames):
    with open("user.txt", "w") as file:
        for username in usernames:
            file.write(username + "\n")
    print(f"{len(usernames)} usernames saved to 'user.txt'.")

if __name__ == '__main__':
    num_usernames = int(input("Enter the number of usernames you want to create: "))
    common_numbers = int(input("Enter the number of first common digit of the phone number of your country (1 or 2): "))
    while common_numbers not in [1, 2]:
        print("Invalid input! Please enter 1 or 2 for common numbers.")
        common_numbers = int(input("Enter the number of common numbers (1 or 2): "))

    usernames = generate_usernames(num_usernames, common_numbers)
    save_usernames(usernames)
