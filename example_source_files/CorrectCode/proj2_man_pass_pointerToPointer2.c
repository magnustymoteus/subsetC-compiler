int main() {
    int a = 0;
    int* b = &a;
    int **c = &b;
    int ***d = &c;
    a = ***d + 10;
 return 0; }