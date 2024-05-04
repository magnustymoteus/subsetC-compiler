#include <stdio.h>
struct Test {
    int arr3[20];
};
struct Test2 {
    int arr[21]; int *ptr;
};
union Something {
    int arr1[5]; int arr[10]; int arr3[15]; int arr2[10]; struct Test* t; struct Test2* t2;
};
int main() {
    union Something s;
    s.arr1[3] = 420;
    s.arr[8] = 69;
    struct Test t;
    s.t = &t;
    printf("%d", s.arr1[3]);
    return 0;
}