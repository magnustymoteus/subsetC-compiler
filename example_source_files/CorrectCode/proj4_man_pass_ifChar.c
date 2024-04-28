#include <stdio.h>

int main() {
    char c = 'a';
    if(c == 'b') {
        printf("%c", 'y');
    }
    else if(c == 'a') {
        printf("%c", 'n');
        if(c >= 50) {
            printf("%f", 6.9);
        }
        else {
            printf("%d", 420);
        }
    }
 return 0; }