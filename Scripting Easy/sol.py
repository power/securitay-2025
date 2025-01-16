import base64
import re
def main():
    a = open("text.txt", "r")
    contents = a.read()
    a.close()
    rem_b64 = base64.b64decode(contents)
    for i in range(9):
        rem_b64 = base64.b64decode(rem_b64)
    final = re.findall(r"!!!([a-zA-Z0-9\-\{\}]{5})", str(rem_b64))
    print(''.join(final))
    return

if __name__ == "__main__":
    main()