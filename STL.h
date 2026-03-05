#pragma once
#include <stack>
#include <string>
#include <iostream>

extern "C" {
	typedef struct MyStack;
	__declspec(dllexport) void create(MyStack** top);
	__declspec(dllexport) bool pushe(MyStack** top, const char* str);
	__declspec(dllexport) bool pope(MyStack** top);
	__declspec(dllexport) bool isEmptye(MyStack** top);
	__declspec(dllexport) int counte(MyStack** top);
	__declspec(dllexport) void cleare(MyStack** top);
}