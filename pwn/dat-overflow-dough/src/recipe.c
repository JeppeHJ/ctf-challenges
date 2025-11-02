// recipe.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

void secret_dough_recipe(void) {
    int fd = open("flag.txt", O_RDONLY);
    sendfile(1, fd, NULL, 100);
}

void vulnerable_dough_recipe() {
    char recipe[16];
    puts("Please enter the name of the recipe you want to retrieve:");
    // Using gets() here is NOT a good idea!! We are not checking the size of the input from the user!
    // The recipe-buffer can only store 16 bytes and the user can input more than that. This could lead to buffer overflows.
    // If an attacker has the address of the secret_dough_recipe function, they could exploit this vulnerability to see our secret recipe!!
    gets(recipe);
}

void public_dough_recipe() {
    puts("Here is the recipe for you!");
    puts("3 eggs and some milk");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    vulnerable_dough_recipe();
    puts("Enjoy baking!");
    return 0;
}
