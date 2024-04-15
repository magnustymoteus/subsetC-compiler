int main() {
	int a = 4;
	int *b = &a;
	int **c = &b;
	**c = 10;
 return 0; }