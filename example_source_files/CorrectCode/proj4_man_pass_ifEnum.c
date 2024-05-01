#include <stdio.h>

enum boolean {
    FALSE,
    TRUE
};

int main() {
    enum boolean isTrue = TRUE;
    if (isTrue) {
        printf("%d", 1);
    } else {
        printf("%d", 0);
    }
 return 0; }