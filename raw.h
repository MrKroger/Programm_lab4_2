#pragma once
#include <stdio.h>
#include <iostream>
#include <string>

extern "C" {
    typedef struct Node;
    __declspec(dllexport) void createl(Node** top);
    __declspec(dllexport) bool pushel(Node** top, const char* str);
    __declspec(dllexport) bool popel(Node** top);
    __declspec(dllexport) bool isEmptyel(Node** top);
    __declspec(dllexport) int countel(Node** top);
    __declspec(dllexport) void clearel(Node** top);
}