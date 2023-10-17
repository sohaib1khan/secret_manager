from cryptography.fernet import Fernet
import sqlite3
import os

# Read or generate and save the key
try:
    with open(".master-key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(".master-key.key", "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)
conn = sqlite3.connect('.secrets.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS secrets
             (name TEXT, encrypted_value BLOB)''')
conn.commit()

def retrieve_secret(name):
    c.execute("SELECT encrypted_value FROM secrets WHERE name=?", (name,))
    encrypted_value = c.fetchone()
    if encrypted_value:
        try:
            decrypted_value = cipher_suite.decrypt(encrypted_value[0])
            return decrypted_value.decode()
        except:
            print("Invalid key - unable to decrypt secret.")
            return None
    else:
        return None

def add_secret(name, value):
    encrypted_value = cipher_suite.encrypt(value.encode())
    c.execute("INSERT INTO secrets (name, encrypted_value) VALUES (?, ?)", (name, encrypted_value))
    conn.commit()

def delete_secret(name):
    c.execute("DELETE FROM secrets WHERE name=?", (name,))
    conn.commit()

if os.path.exists("config.txt"):
    with open("config.txt", "r") as f:
        api_key = f.read().strip()
    add_secret('my_api_key', api_key)
    os.remove("config.txt")

def list_secrets():
    c.execute("SELECT name FROM secrets")
    all_secrets = c.fetchall()
    if all_secrets:
        print("List of existing secrets:")
        for secret in all_secrets:
            print(f"- {secret[0]}")
    else:
        print("No secrets found.")

def main():
    try:
        while True:
            print("Welcome to the secret manager!")
            print()
            action = input("Would you like to (a)dd a new secret, (r)etrieve a secret, (d)elete a secret, or (l)ist all secrets? (a/r/d/l): ")
            if action.lower() == 'a':
                name = input("Enter the name of the secret: ")
                value = input("Enter the secret value: ")
                add_secret(name, value)
            elif action.lower() == 'r':
                name = input("Enter the name of the secret you want to retrieve: ")
                value = retrieve_secret(name)
                if value:
                    print(f"The value of {name} is {value}")
                else:
                    print("Secret not found.")
            elif action.lower() == 'd':
                name = input("Enter the name of the secret you want to delete: ")
                if retrieve_secret(name):
                    delete_secret(name)
                    print(f"The secret {name} has been deleted.")
                else:
                    print("Secret not found.")
            elif action.lower() == 'l':
                list_secrets()
            else:
                print("Invalid option. Please try again.")

            cont = input("Would you like to continue? (y/n): ")
            if cont.lower() == 'n':
                print("Exiting program, Goodbye!")
                break
            elif cont.lower() == 'y':
                continue
            else:
                print("Invalid option. Please try again.")

    except KeyboardInterrupt:
        print("\nExiting program, Goodbye!")  # Printed when Ctrl+C is pressed

if __name__ == "__main__":
    main()
