enum test {yes, no};
int main() {
    enum status {on, off};
    enum status x = off+no*10;
    switch(x) {
        case 10:
            printf("%d", yes);
            x = 20;
        case 11:
            printf("%d", 2);
            x++;
            break;
        case 69:
            printf("%d", 69);
            break;
        default:
            printf("%d", 420);
    }
    printf("%d", x);
 return 0; }