import argparse
import sys
import os
try:
    from PIL import Image
except ImportError:
    print("[-] Error: 'Pillow' library is not installed. Run 'pip install Pillow'")
    sys.exit(1)

# A unique delimiter to know where our hidden message ends
DELIMITER = "====STOP===="

def text_to_binary(text: str) -> str:
    """Converts a string of text into a sequence of binary bits."""
    # Convert each character to its 8-bit binary representation
    return ''.join([format(ord(char), "08b") for char in text])

def binary_to_text(binary_data: str) -> str:
    """Converts a sequence of binary bits back into a readable string."""
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    
    decoded_text = ""
    for byte in all_bytes:
        decoded_text += chr(int(byte, 2))
        # If we detect our delimiter, we stop translating
        if decoded_text.endswith(DELIMITER):
            return decoded_text[:-len(DELIMITER)]
            
    return decoded_text

def hide_message(image_path: str, secret_message: str, output_path: str):
    """Embeds a secret message into the image using LSB steganography."""
    try:
        img = Image.open(image_path)
        # Ensure image is in RGB mode (Red, Green, Blue)
        img = img.convert("RGB")
    except Exception as e:
        print(f"[-] Error opening image: {e}")
        sys.exit(1)

    # Append our delimiter so the decoder knows when to stop
    full_message = secret_message + DELIMITER
    binary_message = text_to_binary(full_message)
    message_length = len(binary_message)

    pixels = img.load()
    width, height = img.size
    
    # Calculate capacity: 3 bits per pixel (1 bit for R, 1 for G, 1 for B)
    max_capacity = width * height * 3
    if message_length > max_capacity:
        print(f"[-] Error: Image is too small! Needs capacity for {message_length} bits, but only has {max_capacity}.")
        sys.exit(1)

    bit_index = 0
    print(f"[*] Hiding {len(secret_message)} characters ({message_length} bits) into '{image_path}'...")

    # Iterate through every pixel
    for y in range(height):
        for x in range(width):
            if bit_index < message_length:
                # Get current RGB values
                r, g, b = pixels[x, y]

                # Modify the Least Significant Bit (LSB) of each color channel
                # using bitwise operations
                if bit_index < message_length:
                    r = (r & ~1) | int(binary_message[bit_index])
                    bit_index += 1
                if bit_index < message_length:
                    g = (g & ~1) | int(binary_message[bit_index])
                    bit_index += 1
                if bit_index < message_length:
                    b = (b & ~1) | int(binary_message[bit_index])
                    bit_index += 1

                # Update the pixel with the slightly modified colors
                pixels[x, y] = (r, g, b)
            else:
                break # Message fully hidden

    # Save as PNG to avoid compression data loss (JPG will destroy the LSB)
    try:
        img.save(output_path, "PNG")
        print(f"[+] Success! Secret image saved as '{output_path}'")
    except Exception as e:
        print(f"[-] Error saving image: {e}")

def extract_message(image_path: str):
    """Extracts a hidden message from the LSBs of the image."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
    except Exception as e:
        print(f"[-] Error opening image: {e}")
        sys.exit(1)

    pixels = img.load()
    width, height = img.size
    binary_data = ""

    print(f"[*] Extracting hidden data from '{image_path}'...")

    # Extract the LSB from every color channel of every pixel
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Translate the massive binary string back to text
    secret_text = binary_to_text(binary_data)
    
    if secret_text:
        print("\n[+] Secret Message Found:")
        print("="*50)
        print(secret_text)
        print("="*50)
    else:
        print("[-] No hidden message found (or delimiter missing).")

def main():
    parser = argparse.ArgumentParser(description="LSB Steganography Tool (Data Smuggler)")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Action to perform")

    # Hide sub-command
    hide_parser = subparsers.add_parser("hide", help="Hide a secret message inside an image")
    hide_parser.add_argument("-i", "--image", required=True, help="Path to the original image (e.g., normal.jpg)")
    hide_parser.add_argument("-m", "--message", required=True, help="The secret message to hide")
    hide_parser.add_argument("-o", "--output", default="secret.png", help="Path to save the modified image (MUST be .png)")

    # Extract sub-command
    extract_parser = subparsers.add_parser("extract", help="Extract a hidden message from an image")
    extract_parser.add_argument("-i", "--image", required=True, help="Path to the manipulated image (e.g., secret.png)")

    args = parser.parse_args()

    print("="*55)
    print("🕵️  Data Smuggler - LSB Steganography Tool")
    print("="*55)

    if args.command == "hide":
        # Force .png extension to prevent data loss
        if not args.output.lower().endswith(".png"):
            print("[!] Warning: Output file must be a PNG to preserve hidden data. Forcing .png extension.")
            args.output = args.output.rsplit('.', 1)[0] + ".png"
        hide_message(args.image, args.message, args.output)
    
    elif args.command == "extract":
        extract_message(args.image)

if __name__ == "__main__":
    main()
