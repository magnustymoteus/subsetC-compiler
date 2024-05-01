#include <stdio.h>

enum Day {
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
};

int main() {
    enum Day today = TUESDAY;
    switch (today) {
        case MONDAY:
        case TUESDAY:
        case WEDNESDAY:
        case THURSDAY:
        case FRIDAY:
            printf("%c", 'a');
            break;
        case SATURDAY:
        case SUNDAY:
            printf("%c", 'b');
            break;
        default:
            printf("%c", 'c');
    }
 return 0; }