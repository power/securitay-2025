#!/usr/bin/env python3

from Crypto.util.number import getPrime, bytes_to_long
import sympy

with open('flag.txt', 'rb') as f:
    flag = f.read()

msgs = [
    b'Did you know Securi-Tay is around the corner?',
    b'We cannot wait to see you at the largest Securi-Tay yet!',
    b'Dont you just love unicorns?',
    b'Only 2 days till Securi-Tay!!!',
    b'What number Securi-Tay is this? I forgot.',
    b'I heard Tristan has a pet parrot called Noah',
    b'Who is a good little parrot? Yes you are Noah! Oops.. forgot this was recording',
    b'WALDO MISSING.. IF FOUND PLEASE CONTACT AIMEE',
    b'Neighhhhhhhh. NEWS JUST IN! Waldo has turned himself in after getting hungry. Aimee, please collect your horse.',
    b'What will happen if you take a unicorns horn off? Find out more in my next message',
]

msgs.append(flag)

final_msgs *= 5
for msg in final_msgs:
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 3
    m = bytes_to_long(msgs)
    c = pow(m, e, n)
    with open('encrypted-messages.txt', 'a') as f:
        f.write(f'n: {n}\n')
        f.write(f'e: {e}\n')
        f.write(f'c: {c}\n\n')