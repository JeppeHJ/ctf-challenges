Very, very simple ret2win challenge. Most of the exploit-code is provided as a template, and the solver will essentially only need to run the binary (to get the address of the win-function) as well as read the code_review.md to get the correct values to plug into the Python-script.

# Solution

The provided recipe.c shows the function ``secret_dough_recipe()`` which prints the flag. It also reveals the function ``vulnerable_dough_recipe()`` which employs ``gets()`` and no length-checking of user-input. This is also documented in the source as actual comments (from the senior dev!).

The provided binary also leaks the memory address of the ``secret_dough_recipe()``-function. 

With the handout is provided an ``exploit.py`` which has most of the exploit already written. The solver will need to identify the memory address of ``secret_dough_recipe()``, identify the "size" of RBP as well as the correct "PROMPT" to send the payload after.
