int main() {

int x = 478;
int b = -251454;

int* b_ptr = &b;

int** x_ptr = &b_ptr;
x_ptr = &b;

// error because int** = int*
 return 0; }
