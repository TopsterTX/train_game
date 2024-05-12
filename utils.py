def convert_hex_to_ansi(hex_string):
    clear_hex = hex_string.strip("#")
    red = int(clear_hex[:2], 16)
    green = int(clear_hex[2:4], 16)
    blue = int(clear_hex[4:], 16)

    return f"\033[48:2::{red}:{green}:{blue}m \033[49m"
