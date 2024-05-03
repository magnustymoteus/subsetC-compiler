struct Node {
    struct Node* left_child; struct Node* right_child; int value; int arr[5];
};
#include <stdio.h>
int main() {
    struct Node node;
    node.arr[1]=69;
    struct Node other_node;
    struct Node* other_node_ptr = &other_node;
    other_node_ptr->arr[4] = 420;
    node.left_child = other_node_ptr;
    printf("%d", node.left_child->arr[4]);
    return 0;
}