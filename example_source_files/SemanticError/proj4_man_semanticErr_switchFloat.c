int main() {
    const float a = 10.12;
    // switch statement must have int as value
    switch(a) {
        case 1:
            printf("%d", 1);
            break;
        case 2:
            printf("%d", 2);
            break;
        default:
            printf("%d", 3);
    }
}