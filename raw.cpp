#include "raw.h"
#include <string>
#include <iostream>

typedef struct Node {
    std::string data;
    struct Node* next;
} Node;

void createl(Node** top) {
    *top = nullptr;
}

bool pushel(Node** top, const char* str) {
    try {
        Node* new_node = new Node;
        new_node->data = std::string(str);
        new_node->next = *top;
        *top = new_node;
        return true;
    }
    catch (std::exception e) {
        return false;
    }
}

bool popel(Node** top) {
    try {
        if (*top == nullptr) {
            return false;
        }
        Node* temp = *top;
        *top = (*top)->next;
        delete temp;
        return true;
    }
    catch (std::exception e) {
        return false;
    }
}

bool isEmptyel(Node** top) {
    return *top == nullptr;
}

int countel(Node** top) {
    int count = 0;
    Node* current = *top;
    while (current != nullptr) {
        count++;
        current = current->next;
    }
    return count;
}

void clearel(Node** top) {
    while (*top != nullptr) {
        popel(top);
    }
}
