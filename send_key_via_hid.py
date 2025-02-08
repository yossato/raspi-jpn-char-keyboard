import time
import unicodedata
import argparse

# HIDデバイスへの書き込み用の関数
def write_to_hid(f, data):
    f.write(data)
    f.flush()

# 通常キーとModifier（Shift）キーの対応表
key_map = {
        'a': (b'\x04', False), 'b': (b'\x05', False), 'c': (b'\x06', False), 'd': (b'\x07', False),
    'e': (b'\x08', False), 'f': (b'\x09', False), 'g': (b'\x0a', False), 'h': (b'\x0b', False),
    'i': (b'\x0c', False), 'j': (b'\x0d', False), 'k': (b'\x0e', False), 'l': (b'\x0f', False),
    'm': (b'\x10', False), 'n': (b'\x11', False), 'o': (b'\x12', False), 'p': (b'\x13', False),
    'q': (b'\x14', False), 'r': (b'\x15', False), 's': (b'\x16', False), 't': (b'\x17', False),
    'u': (b'\x18', False), 'v': (b'\x19', False), 'w': (b'\x1a', False), 'x': (b'\x1b', False),
    'y': (b'\x1c', False), 'z': (b'\x1d', False), 'A': (b'\x04', True), 'B': (b'\x05', True),
    'C': (b'\x06', True), 'D': (b'\x07', True), 'E': (b'\x08', True), 'F': (b'\x09', True),
    'G': (b'\x0a', True), 'H': (b'\x0b', True), 'I': (b'\x0c', True), 'J': (b'\x0d', True),
    'K': (b'\x0e', True), 'L': (b'\x0f', True), 'M': (b'\x10', True), 'N': (b'\x11', True),
    'O': (b'\x12', True), 'P': (b'\x13', True), 'Q': (b'\x14', True), 'R': (b'\x15', True),
    'S': (b'\x16', True), 'T': (b'\x17', True), 'U': (b'\x18', True), 'V': (b'\x19', True),
    'W': (b'\x1a', True), 'X': (b'\x1b', True), 'Y': (b'\x1c', True), 'Z': (b'\x1d', True),
    '1': (b'\x1e', False), '2': (b'\x1f', False), '3': (b'\x20', False), '4': (b'\x21', False),
    '5': (b'\x22', False), '6': (b'\x23', False), '7': (b'\x24', False), '8': (b'\x25', False),
    '9': (b'\x26', False), '0': (b'\x27', False), ' ': (b'\x2c', False), 
    

    '1': (b'\x1E', False),
    '2': (b'\x1F', False),
    '3': (b'\x20', False),
    '4': (b'\x21', False),
    '5': (b'\x22', False),
    '6': (b'\x23', False),
    '7': (b'\x24', False),
    '8': (b'\x25', False),
    '9': (b'\x26', False),
    '0': (b'\x27', False),
    '!': (b'\x1E', True),
    '\"': (b'\x1F', True),
    '#': (b'\x20', True),
    '$': (b'\x21', True),
    '%': (b'\x22', True),
    '&': (b'\x23', True),
    '\'': (b'\x24', True),
    '(': (b'\x25', True),
    ')': (b'\x26', True),
    # '': (b'\x27', True), # Shift + 0 は何も入力されない
    '-': (b'\x2D', False),
    '^': (b'\x2E', False),
    '@': (b'\x2F', False),
    '[': (b'\x30', False),
    ']': (b'\x31', False),
    # ']': (b'\x32', False), # 重複
    ';': (b'\x33', False), # 重複
    ':': (b'\x34', False),
    # ',': (b'\x35', False), # 全角半角
    ',': (b'\x36', False),
    '.': (b'\x37', False),
    '/': (b'\x38', False),
    '=': (b'\x2D', True),
    '~': (b'\x2E', True),
    '`': (b'\x2F', True),
    '{': (b'\x30', True),
    '}': (b'\x31', True),
    # '}': (b'\x32', True), #重複
    '+': (b'\x33', True),
    '*': (b'\x34', True),
    # '': (b'\x35', True), # Shift + 全角半角
    '<': (b'\x36', True),
    '>': (b'\x37', True),
    '?': (b'\x38', True),
    # '?': (b'\x38', True),

    'Enter': (b'\x28',False),
    'F5': (b'\x3E', False),
    'カタカナひらがな': (b'88', False), # カタカナひらがな
    '全角半角': (b'\x35', False)    # Zenkaku/Hankaku, 英語のキーボードだとチルダっぽい
}

# 1文字を送信する関数
def press_key(f, char):
    if char in key_map:
        key_code, requires_shift = key_map[char]
        modifier = b'\x02' if requires_shift else b'\x00'
        write_to_hid(f, modifier + b'\x00' + key_code + b'\x00\x00\x00\x00\x00')
        time.sleep(0.01)
        write_to_hid(f, b'\x00\x00\x00\x00\x00\x00\x00\x00')
        time.sleep(0.01)
    else:
        print(f"Key map error for character: {char}")

# 半角英数字か判定する関数
def is_ascii(char):
    try:
        return unicodedata.name(char).startswith("LATIN") or char.isascii()
    except ValueError:
        return False


# 1文字を送信する関数
def press_key(f, char):
    if char == '\n':
        # 改行文字の場合は「Enter」キーを押す
        key_code, requires_shift = key_map['Enter']
    elif char in key_map:
        key_code, requires_shift = key_map[char]
    else:
        print(f"Key map error for character: {char}")
        return

    modifier = b'\x02' if requires_shift else b'\x00'
    write_to_hid(f, modifier + b'\x00' + key_code + b'\x00\x00\x00\x00\x00')
    time.sleep(0.01)
    write_to_hid(f, b'\x00\x00\x00\x00\x00\x00\x00\x00')
    time.sleep(0.01)



# Unicode文字列をHIDデバイスに送信
def send_unicode_string(device_path, text):
    with open(device_path, 'wb') as f:
        for char in text:
            if char == '\n':
                press_key(f, 'Enter')
            elif is_ascii(char):
                press_key(f, '全角半角')
                press_key(f, char)
                press_key(f, '全角半角')
            else:
                unicode_code = ord(char)
                unicode_hex = f"{unicode_code:X}"
                for digit in unicode_hex:
                    press_key(f, digit)
                press_key(f, 'F5')
                press_key(f, 'Enter')
            time.sleep(0.1)

# メイン関数
def main():
    parser = argparse.ArgumentParser(description="Send Unicode strings to HID device.")
    parser.add_argument("-d","--device_path", help="Path to the HID device.")
    parser.add_argument("-t", "--text", help="Text to send to the HID device.")
    args = parser.parse_args()

    try:
        with open(args.text, 'r', encoding='utf-8') as file:
            content = file.read()
            send_unicode_string(args.device_path, content)
    except FileNotFoundError:
        print(f"Error: File '{args.file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()