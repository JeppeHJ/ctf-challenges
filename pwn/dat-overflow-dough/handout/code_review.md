#### Code Review of recipe.c

Dear intern, upon reviewing your code, I have left some comments in there that highlight some of the issues I found. But I want to elaborate a little bit here.

#### Understanding vulnerabilities through exploitation

So one day this 1337 hacker in a hoodie reviewed my first C-code, a program similar to yours. He used a "buffer overflow" vulnerability to *redirect program-flow*.
With just a few lines of Python code, he managed to make my program execute a function that was supposed to be secret.

He taught me that in a 64-bit program like yours, when a function is called, the memory consists of:

1) The local variables
2) A register called `RBP` (not important for now)
3) A return address showing the program where to jump back to when returning from the function

And so if one of the local variables is a buffer we can write to with no size protections, then we can overwrite all remaining local variables (if any), the RBP register, and then the return address, fully controlling where the program jumps to.

So, a payload should consist of:

1) Enough bytes to exactly fill the buffer +
2) Bytes to overwrite RBP +
3) The memory address of the function you want to re-direct execution to.

What this actually achieves is it **"overwrites" the saved return address on the stack**. This is the value that **RIP (the Instruction Pointer)** will take when the function returns. This is important because RIP is the register that holds the memory address of the next instruction!

So, if we can write the address of a secret function into that saved return address, then when the function returns, **RIP "points" at that address and it jumps to that function!**

I think the hacker called this "ret2win". It was amazing! He also taught me how to use [pwntools](https://docs.pwntools.com) to build such an exploit; a cool Python framework many pwn'erZ use.

#### No PIE/ASLR

I will not bore you too much with "stack protections", but it is important to understand what the difference is between "no-PIE" and "PIE". You compiled with the ``no-pie no-aslr`` flags.

So when you compile with these flags, that means memory addresses are static. No matter how many times you run the program, the *memory addresses stay the same*. This is not the case when you compile with the ``pie``-flag!

What this means for your program is that a smart attacker can obtain the address of the ``secret_dough_recipe()``-function very easily and write an exploit to return to this function!
There are many ways and tools to obtain the memory addresses of functions in a binary, e.g. `objdump` or a decompiler.

###### exploit.py

I realize this can be a little hard to understand which is why I provided you with an `exploit.py` script to show you how someone could do this to your program. You will need to fill out some variables though, but the Pwntools template will take care of the rest!
