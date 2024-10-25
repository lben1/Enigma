import string
import random

# Function to apply switchboard settings
def switchboard(message, switchboardconf):
    switchboard_map = {}
    if switchboardconf:  # Only process if switchboardconf is provided
        for pair in switchboardconf.split(','):
            key, value = pair.split('=')
            switchboard_map[key.upper()] = value.upper()
            switchboard_map[value.upper()] = key.upper()  # Reverse mapping for decoding

    transformed_message = ""
    for char in message.upper():
        if char in switchboard_map:
            transformed_message += switchboard_map[char]
        else:
            transformed_message += char
    return transformed_message

# Function to rotate the rotor
def rotate(rotor, steps):
    return rotor[steps:] + rotor[:steps]

# Function to pass a character through a rotor
def pass_through_rotor(char, rotor, alphabet=string.ascii_uppercase):
    index = alphabet.find(char)
    if index != -1:
        return rotor[index]
    else:
        return char

# Function to pass a character through a rotor in reverse (decoding)
def pass_through_rotor_reverse(char, rotor, alphabet=string.ascii_uppercase):
    index = rotor.find(char)
    if index != -1:
        return alphabet[index]
    else:
        return char

# Function to pass a character through a reflector (symmetric substitution)
def reflector(char, reflector_map, alphabet=string.ascii_uppercase):
    index = alphabet.find(char)
    if index != -1:
        return reflector_map[index]
    else:
        return char

# Function to rotate rotors based on encryption/decryption step
def rotate_rotors(rotor_positions, rotors):
    rotor_positions[0] = (rotor_positions[0] + 1) % 26
    rotors[0] = rotate(rotors[0], 1)

    # Rotate the second rotor when the first one completes a full rotation
    if rotor_positions[0] == 0:
        rotor_positions[1] = (rotor_positions[1] + 1) % 26
        rotors[1] = rotate(rotors[1], 1)

        # Rotate the third rotor when the second one completes a full rotation
        if rotor_positions[1] == 0:
            rotor_positions[2] = (rotor_positions[2] + 1) % 26
            rotors[2] = rotate(rotors[2], 1)

# Unified Enigma function (works for both encryption and decryption)
def enigma_machine(message, switchboardconf, rotors, rotor_positions, reflector_map):
    alphabet = string.ascii_uppercase
    processed_message = ""

    # Step 1: Apply switchboard (plugboard) transformation at the beginning
    message = switchboard(message, switchboardconf)

    # Step 2: Pass each character through the rotors and reflector
    for char in message.upper():
        if char in alphabet:
            # Rotate the rotors
            rotate_rotors(rotor_positions, rotors)

            # Step 2.1: Pass the character through each rotor
            for rotor in rotors:
                char = pass_through_rotor(char, rotor)

            # Step 2.2: Reflect the character
            char = reflector(char, reflector_map)

            # Step 2.3: Pass the character back through each rotor (in reverse order)
            for rotor in reversed(rotors):
                char = pass_through_rotor_reverse(char, rotor)

        processed_message += char

    # Step 3: Apply switchboard (plugboard) transformation at the end
    processed_message = switchboard(processed_message, switchboardconf)

    return processed_message

# Function to validate rotor positions (A-Z input)
def get_rotor_position(rotor_num):
    while True:
        pos = input(f"Enter the starting position for Rotor {rotor_num} (A-Z): ").upper()
        if pos in string.ascii_uppercase:
            return string.ascii_uppercase.index(pos)
        else:
            print("Invalid input. Please enter a letter between A and Z.")

# Function to format message into four-letter groups
def format_four_letter_groups(message):
    message = message.replace(" ", "")  # Remove spaces if any
    if len(message) % 4 != 0:
        # If the last group has fewer than 4 letters, add random letters to complete it
        message += ''.join(random.choices(string.ascii_uppercase, k=4 - len(message) % 4))
    return ' '.join(message[i:i+4] for i in range(0, len(message), 4))

# Main loop to process multiple messages
def main():
    # Store initial rotor and plugboard configurations
    rotor_positions = [get_rotor_position(i + 1) for i in range(3)]
    initial_rotor_positions = rotor_positions.copy()  # Save initial rotor positions
    switchboardconf = input("Enter switchboard settings, EG A=H,B=E etc, press enter to skip: ")
    last_output_message = None

    while True:
        # Menu options
        print("\nSelect an option to continue:")
        print("1) Enter more text using the same initial rotor and plugboard selection")
        print("2) Edit Rotor and Plugboard Selection")
        print("3) Display the last output as four-letter groups")
        print("0) Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            message = input("Enter the message to be processed (spaces will be removed): ").replace(" ", "").upper()
            rotor_positions = initial_rotor_positions.copy()  # Reset rotor positions before processing
        elif choice == '2':
            # Get new rotor positions and switchboard configuration
            rotor_positions = [get_rotor_position(i + 1) for i in range(3)]
            initial_rotor_positions = rotor_positions.copy()  # Save new initial rotor positions
            rotoerpx = input("Enter rotor position, eg 3,1,2: ")

            switchboardconf = input("Enter plugboard settings, EG A=H,B=E etc, press enter to skip: ")
            message = input("Enter the message to be processed (spaces will be removed): ").replace(" ", "").upper()
        elif choice == '3':
            if last_output_message:
                formatted_message = format_four_letter_groups(last_output_message)
                print(f"Last output in four-letter groups: {formatted_message}")
            else:
                print("No previous output to display.")
            continue
        else:
            print("Invalid choice, please try again.")
            continue

        # Define the rotors (simple rotor examples)
        rotor1 = "LPGSZMHAEOQKVXRFYBUTNICJDW"
        rotor2 = "SLVGBTFXJQOHEWIRZYAMKPCNDU"
        rotor3 = "CJGDPSHKTURAWZXFMYNQOBVLIE"
        rotors = [rotor1, rotor2, rotor3]

        # Define a simple reflector (basic substitution, should be symmetric)
        reflector_map = "IMETCGFRAYSQBZXWLHKDVUPOJN"

        # Process the message using the Enigma machine (both for encryption and decryption)
        output_message = enigma_machine(message, switchboardconf, rotors, rotor_positions, reflector_map)
        last_output_message = output_message  # Store the last processed message
        print(f"Processed Message: {output_message}")


if __name__ == "__main__":
    main()
