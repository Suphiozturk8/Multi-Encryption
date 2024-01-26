# t.me/Syupie

import os
import codecs
from random import choice
from marshal import dumps
from zlib import compress
from base64 import (
    b16encode,
    b32encode,
    b64encode,
    b85encode
)


encryption_funcs = [
    compress, b85encode,
    b32encode, b64encode,
    b16encode
]

decryption_funcs = {
    "compress": "decompress",
    "b85encode": "b85decode",
    "b32encode": "b32decode",
    "b64encode": "b64decode",
    "b16encode": "b16decode"
}

def encode(code, layers=1):
    original = code
    for _ in range(layers):
        funcs = []
        for index in range(len(encryption_funcs)):
            func = choice(encryption_funcs)
            while func in funcs:
                if len(funcs) != len(encryption_funcs):
                    func = choice(encryption_funcs)
                elif len(funcs) == len(encryption_funcs):
                    func = None
            funcs.append(func)
        encrypted = dumps(code)
        encrypted = funcs[0](encrypted)
        encrypted = funcs[1](encrypted)
        encrypted = funcs[2](encrypted)
        encrypted = funcs[3](encrypted)
        encrypted = funcs[4](encrypted)

        if (funcs[4].__name__ == "compress"):
            return encode(original, layers)

        code = run_template % (
            "loads",
            decryption_funcs[funcs[0].__name__],
            decryption_funcs[funcs[1].__name__],
            decryption_funcs[funcs[2].__name__],
            decryption_funcs[funcs[3].__name__],
            decryption_funcs[funcs[4].__name__],
            codecs.encode(
                encrypted.decode(),
                "rot_13"
            ).encode().decode(
                "utf-8", 
                "ignore"
            )
        )

    return code 


run_template = """

import codecs
from marshal import loads
from zlib import decompress
from base64 import (
    b16decode,
    b64decode,
    b32decode,
    b85decode
)

exec(
    %s(
        %s(
            %s(
                %s(
                    %s(
                        %s(
                            (
                                (lambda __, _: _(str("%s"), __))("rot_13", __import__("codecs").decode)
                            )
                        )
                    )
                )
            )
        )
    )
)

"""

file_name = input(
    "Entre a file path to encrypt:\n"
)

while not os.path.exists(file_name):
    print(
        f"\nThere is no file or directory with this name [{file_name}]"
    )
    file_name = input(
        "ReEnter the file path:\n"
    )

file_data = open(file_name, "r").read()

iterations = input(
    "\nHow many layers do you want?\n"
)

while not iterations.isnumeric():
    iterations = input(
        "\nEnter a valid value for layers:\n"
    )
    
if iterations == "":
    iterations = 2
else:
    iterations = int(iterations)

print(
    "\nEncoding..."
)

encrypted_data = encode(
    file_data, iterations
)

output_file_name = file_name.replace(
    ".py", "_encrypted.py"
)

open(output_file_name, "w").write(encrypted_data)

print(
    f"\nSaved as: {output_file_name}"
)
