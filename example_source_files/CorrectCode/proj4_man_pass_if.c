#include <stdio.h>

int main() {
    int x = 10;
    if(x > 5) {
        printf("%d", 1);
        if(x >= 7) {
            printf("%d", 2);
            if(x == 11) {
                printf("%d", 3);
            }
            else {
                printf("%d", 4);
            }
        }
    }
 return 0; }