#include "stl.h"
#include <stack>
#include <string>
#include <iostream>

typedef struct MyStack {
    std::stack<std::string> stack;
} MyStack;

void create(MyStack** top) {
    *top = new MyStack();
}

bool pushe(MyStack** top, const char* str) {
    try {
        if (*top == nullptr) {
            return false;
        }
        (*top)->stack.push(std::string(str));
        return true;
    }
    catch (std::exception e) {
        return false;
    }
}

bool pope(MyStack** top) {
    try {
        if (*top == nullptr || (*top)->stack.empty()) {
            return false;
        }
        (*top)->stack.pop();
        return true;
    }
    catch (std::exception e) {
        return false;
    }
}

bool isEmptye(MyStack** top) {
    if (*top == nullptr) return true;
    return (*top)->stack.empty();
}

int counte(MyStack** top) {
    if (*top == nullptr) return 0;
    return (*top)->stack.size();
}

void cleare(MyStack** top) {
    if (*top == nullptr) return;
    while (!(*top)->stack.empty()) {
        (*top)->stack.pop();
    }
}