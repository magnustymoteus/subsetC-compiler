int main() {

int x = 478;
int b = -251454;

int** x_ptr = &x;
x_ptr = &b;
// error because int** = int*
 return 0; }
