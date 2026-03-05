import ctypes
import os

from stack_lib import Stack
data1=[]
data2=[]
class PythonBackend:
    def __init__(self): 
        self.obj = Stack()
        print("✅ PythonBackend: инициализирован")
    
    def push(self, s): 
        return self.obj.push(s)
    
    def pop(self): 
        return self.obj.pop()
    
    def isEmpty(self): 
        return self.obj.isEmpty()
    
    def count(self): 
        return self.obj.count()
    
    def clear(self): 
        self.obj.clear()
        return True

    def get_stack_data(self):
        return self.obj.data.copy()

    def display(self):
        if not self.obj.data:
            return "Стек пуст"
        
        result = "Стек (сверху вниз):\n"
        for i, item in enumerate(reversed(self.obj.data)):
            result += f"  [{len(self.obj.data)-i}] {item}\n"
        return result


class CppBackend:
    def __init__(self):
        dll_path = r'C:\Users\XDXDXD\source\Проекты1\PROGR\lib2\C++\x64\Debug\C++.dll'
        if not os.path.exists(dll_path):
            local_path = 'stack_raww.dll'
            if os.path.exists(local_path):
                dll_path = local_path
            else:
                raise Exception(f"DLL не найдена: {dll_path}")
        
        self.lib = ctypes.CDLL(dll_path)

        # ✅ ИСПРАВЛЕНО: все функции теперь работают с указателями
        self.lib.createl.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.createl.restype = None

        # ✅ ИСПРАВЛЕНО: pushel принимает Node** и const char*
        self.lib.pushel.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]
        self.lib.pushel.restype = ctypes.c_bool

        # ✅ ИСПРАВЛЕНО: popel принимает Node**
        self.lib.popel.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.popel.restype = ctypes.c_bool

        # ✅ ИСПРАВЛЕНО: isEmptyel принимает Node**
        self.lib.isEmptyel.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.isEmptyel.restype = ctypes.c_bool

        # ✅ ИСПРАВЛЕНО: countel принимает Node**
        self.lib.countel.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.countel.restype = ctypes.c_int

        # ✅ ИСПРАВЛЕНО: clearel принимает Node**
        self.lib.clearel.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.clearel.restype = None

        # ✅ ИСПРАВЛЕНО: создаем указатель
        self.top = ctypes.c_void_p()
        self.lib.createl(ctypes.byref(self.top))
        print("✅ CppBackend инициализирован")
    
    def push(self, s):
        try:
            data1.append(s)
            str_bytes = s.encode('utf-8') + b'\0'
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            result = self.lib.pushel(ctypes.byref(self.top), str_bytes)
            return result
        except Exception as e:
            print(f"❌ Ошибка push: {e}")
            return False
    
    def pop(self):
        try:
            data1.pop()
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            return self.lib.popel(ctypes.byref(self.top))
        except Exception as e:
            print(f"❌ Ошибка pop: {e}")
            return False
    
    def isEmpty(self):
        try:

            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            return self.lib.isEmptyel(ctypes.byref(self.top))
        except Exception as e:
            print(f"❌ Ошибка isEmpty: {e}")
            return True
    
    def count(self):
        try:
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            return self.lib.countel(ctypes.byref(self.top))
        except Exception as e:
            print(f"❌ Ошибка count: {e}")
            return 0
    
    def clear(self):
        try:
            data1.clear()
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            self.lib.clearel(ctypes.byref(self.top))
            return True
        except Exception as e:
            print(f"❌ Ошибка clear: {e}")
            return False

    def display(self):
        if len(data1)==0:
            return "Стек пуст"
        result = "Стек (сверху вниз):\n"
        for i, item in enumerate(reversed(data1)):
            result += f"  [{len(data1)-i}] {item}\n"
        return result
    
    def __del__(self):
        try:
            self.clear()
        except:
            pass


class CppSTLBackend:
    def __init__(self):
        dll_path = r'C:\Users\XDXDXD\source\Проекты1\PROGR\lib2\C++STL\x64\Debug\C++STL.dll'
        if not os.path.exists(dll_path):
            local_path = 'stack_stl.dll'
            if os.path.exists(local_path):
                dll_path = local_path
            else:
                raise Exception(f"DLL не найдена: {dll_path}")
        
        self.lib = ctypes.CDLL(dll_path)

        # ✅ ИСПРАВЛЕНО: все функции теперь работают с указателями
        self.lib.create.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.create.restype = None

        self.lib.pushe.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]
        self.lib.pushe.restype = ctypes.c_bool

        self.lib.pope.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.pope.restype = ctypes.c_bool

        self.lib.isEmptye.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.isEmptye.restype = ctypes.c_bool

        self.lib.counte.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.counte.restype = ctypes.c_int

        self.lib.cleare.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.cleare.restype = None

        self.top = ctypes.c_void_p()
        self.lib.create(ctypes.byref(self.top))
        print("✅ CppSTLBackend инициализирован")
    
    def push(self, s):
        try:
            data2.append(s)
            str_bytes = s.encode('utf-8') + b'\0'
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            result = self.lib.pushe(ctypes.byref(self.top), str_bytes)
            return result
        except Exception as e:
            print(f"❌ Ошибка push: {e}")
            return False
    
    def pop(self):
        try:
            data2.pop()
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            return self.lib.pope(ctypes.byref(self.top))
        except Exception as e:
            print(f"❌ Ошибка pop: {e}")
            return False
    
    def isEmpty(self):
        try:
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            return self.lib.isEmptye(ctypes.byref(self.top))
        except Exception as e:
            print(f"❌ Ошибка isEmpty: {e}")
            return True
    
    def count(self):
        try:
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            return self.lib.counte(ctypes.byref(self.top))
        except Exception as e:
            print(f"❌ Ошибка count: {e}")
            return 0
    
    def clear(self):
        try:
            data2.clear()
            # ✅ ИСПРАВЛЕНО: передаем указатель на top
            self.lib.cleare(ctypes.byref(self.top))
            return True
        except Exception as e:
            print(f"❌ Ошибка clear: {e}")
            return False
    
    def display(self):
        if len(data2)==0:
            return "Стек пуст"
        result = "Стек (сверху вниз):\n"
        for i, item in enumerate(reversed(data2)):
            result += f"  [{len(data2)-i}] {item}\n"
        return result
    
    def __del__(self):
        try:
            self.clear()
        except:
            pass
