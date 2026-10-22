
from modified_Huffman.compress import compress_file
from modified_Huffman.decompress import decompress_file

INPUT_FILE = "input.txt"
COMPRESSED_FILE = "compressed.bin"
OUTPUT_FILE = "output.txt"


def handle_compress():
    min_limit = float(input("Enter minimum limit (e.g. 0.05): "))
    details = compress_file(INPUT_FILE, COMPRESSED_FILE, min_limit)
    print(f"Compressed successfully! {details['encoded_bit_length']} bits")


def handle_both():
    handle_compress()
    decompress_file(COMPRESSED_FILE, OUTPUT_FILE)
    print("Decompressed successfully!")


def display_menu():
    print("\n===== Huffman Compression =====")
    print("1. Compress only")
    print("2. Compress & Decompress")
    print("3. Exit")


def main():
    menu_actions = {
        "1": handle_compress,
        "2": handle_both
    }

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
