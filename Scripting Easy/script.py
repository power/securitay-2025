import string
import random
import base64
flag="SECURI-TAY{eed38d366ee999a2ebdeb51ab5c53232}"
flag+="}"
alphabet = string.ascii_lowercase+string.ascii_uppercase+string.punctuation+string.digits
def main():
    index = 0
    text = ""
    while True:
        if (index < len(flag)):
            for i in range(random.randint(1,5)):
                text += ''.join(random.sample(alphabet,len(alphabet)))
            text += "!!!"+flag[index:index+5]
            index += 5
        else:
            for i in range(random.randint(1,5)):
                text += ''.join(random.sample(alphabet,len(alphabet)))
            final = text.encode()
            final = base64.b64encode(final)
            for i in range(9):
                print(i)
                final = base64.b64encode(final)  
            a = open("text.txt", "a")
            a.write(str(final))
            a.close()
            break
    return

if __name__ == "__main__":
    main()