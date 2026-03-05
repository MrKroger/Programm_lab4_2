# -*- coding: utf-8 -*-
import sys
import os
from tkinter import *
from tkinter import ttk, messagebox
from backends import PythonBackend, CppBackend, CppSTLBackend

class ArrowButton:
    def __init__(self, parent, direction="right", size=60, color="#007bff", command=None):
        self.direction = direction
        self.size = size
        self.color = color
        self.hover_color = "#0056b3"
        self.pressed_color = "#004085"
        self.command = command
        self.canvas = Canvas(parent, width=size, height=size, bg=parent.cget('bg'), highlightthickness=0)
        if direction == "left": self._draw_left_triangle(size)
        elif direction == "right": self._draw_right_triangle(size)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.is_pressed = False
    
    def _draw_left_triangle(self, size):
        self.shape = self.canvas.create_polygon(
            size - 10, 10, 10, size // 2, size - 10, size - 10,
            fill=self.color, outline="#0056b3", width=2, smooth=False)
    
    def _draw_right_triangle(self, size):
        self.shape = self.canvas.create_polygon(
            10, 10, size - 10, size // 2, 10, size - 10,
            fill=self.color, outline="#0056b3", width=2, smooth=False)
    
    def _on_click(self, event):
        self.is_pressed = True
        self.canvas.itemconfig(self.shape, fill=self.pressed_color)
    
    def _on_release(self, event):
        self.is_pressed = False
        if self.command: self.command()
        self._on_leave(None)
    
    def _on_enter(self, event):
        if not self.is_pressed: self.canvas.itemconfig(self.shape, fill=self.hover_color)
    
    def _on_leave(self, event):
        if not self.is_pressed: self.canvas.itemconfig(self.shape, fill=self.color)
    
    def pack(self, **kwargs): self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs): self.canvas.grid(**kwargs)

Flag=[]
def fff(self):
    try:
        Flag.index(self.active_language)
        return True
    except Exception as e:
        return False

class StackApp:
    """Основной класс приложения"""
    def __init__(self):
        self.root = Tk()
        self.root.title("Реализация СТЕКА на языках")
        self.root.geometry('900x800')
        self.root.configure(bg='#f5f5f5')
        self.backends = self._load_backends()
        self.texts = list(self.backends.keys())
        if not self.texts:
            messagebox.showerror("Ошибка", "Не удалось загрузить ни один бэкенд!")
            sys.exit(1)
        self.current_index = 0
        self.current_backend = self.backends[self.texts[self.current_index]]
        self.active_language = self.texts[self.current_index]
        self.language_flags = {lang: False for lang in self.texts}
        self.language_flags[self.texts[self.current_index]] = True
        self.stack_data = []
        self._create_interface()
        self.root.mainloop()
    
    def _load_backends(self):
        backends = {}
        print("=" * 50)
        print("ЗАГРУЗКА БЭКЕНДОВ")
        print("=" * 50)
        try:
            backends["Python"] = PythonBackend()
            print("✅ PythonBackend: OK")
        except Exception as e:
            print(f"❌ PythonBackend: {e}")
        try:
            backends["C (raw)"] = CppBackend()
            print("✅ CppBackend (raw): OK")
        except Exception as e:
            print(f"❌ CppBackend (raw): {e}")
        try:
            backends["C++ (STL)"] = CppSTLBackend()
            print("✅ CppSTLBackend: OK")
        except Exception as e:
            print(f"❌ CppSTLBackend: {e}")
        print("\n" + "=" * 50)
        print(f"✅ Доступные языки: {list(backends.keys())}")
        print("=" * 50)
        return backends
    
    def _update_language_flags(self, new_index):
        for lang in self.language_flags:
            self.language_flags[lang] = False
        
        selected_language = self.texts[new_index]
        self.language_flags[selected_language] = True
        self.active_language = selected_language
        self.current_index = new_index
        
        self.current_backend = self.backends[selected_language]
        
        self._add_output(f"\n🔄 Смена языка на: {selected_language}")
        self._add_output(f"📊 Активный бэкенд: {type(self.current_backend).__name__}")
    
    def _add_output(self, text):
        self.output_text.insert(END, text + "\n")
        self.output_text.see(END)
    
    def _scroll_left(self):
        new_index = (self.current_index - 1) % len(self.texts)
        self._update_language_flags(new_index)
        self.display_text.set(self.texts[self.current_index])
        self.counter_text.set(f"{self.current_index + 1}/{len(self.texts)}")
        for i in range(3):
            color = ["#ff6666", "#ffff66", "#66b3ff"][i]
            self.display_frame.configure(highlightbackground=color)
            self.root.update()
            self.root.after(30)
        self.display_frame.configure(highlightbackground="#007bff")
    
    def _scroll_right(self):
        """Прокрутка вправо"""
        new_index = (self.current_index + 1) % len(self.texts)
        self._update_language_flags(new_index)
        self.display_text.set(self.texts[self.current_index])
        self.counter_text.set(f"{self.current_index + 1}/{len(self.texts)}")
        for i in range(3):
            color = ["#ff6666", "#ffff66", "#66b3ff"][i]
            self.display_frame.configure(highlightbackground=color)
            self.root.update()
            self.root.after(30)
        self.display_frame.configure(highlightbackground="#007bff")
    
    def _create_stack(self):
        self._add_output(f"\n▶ ИНИЦИАЛИЗАЦИЯ СТЕКА")
        self._add_output(f"   Язык: {self.active_language}")
        self._add_output(f"   Бэкенд: {type(self.current_backend).__name__}")
        if not fff(self):
            if hasattr(self.current_backend, 'clear'):
                self.current_backend.clear()
            if self.active_language == "Python" and hasattr(self.current_backend, 'get_stack_data'):
                self.stack_data = self.current_backend.get_stack_data()
            else:
                self.stack_data = []
            self._add_output(f"   Статус: Стек готов к работе")
            Flag.append(self.active_language)
    
    def _push(self):
        if fff(self):
            dialog = Toplevel(self.root)
            dialog.title("Ввод строки")
            dialog.geometry("300x150")
            dialog.transient(self.root)
            dialog.grab_set()
        
            Label(dialog, text="Введите строку для добавления:", 
                font=("Arial", 10)).pack(pady=10)
        
            entry = Entry(dialog, width=30, font=("Arial", 10))
            entry.pack(pady=5)
            entry.focus()
        
            def on_ok():
                value = entry.get()
                if value:
                    self._execute_push(value)
                dialog.destroy()
        
            def on_cancel():
                dialog.destroy()
        
            Button(dialog, text="OK", command=on_ok, width=10).pack(side=LEFT, padx=20, pady=10)
            Button(dialog, text="Отмена", command=on_cancel, width=10).pack(side=RIGHT, padx=20, pady=10)
        
            dialog.wait_window()
        else: self._add_output(f" Может создашь Stack для начала?")
    
    def _execute_push(self, value):
        self._add_output(f"\n➕ PUSH (добавление)")
        self._add_output(f"   Язык: {self.active_language}")
        self._add_output(f"   Значение: {value}")
        
        try:
            if hasattr(self.current_backend, 'push'):
                result = self.current_backend.push(value)
                if result:
                    self._add_output(f"   Результат: Успешно добавлено")
                    if self.active_language == "Python" and hasattr(self.current_backend, 'get_stack_data'):
                        self.stack_data = self.current_backend.get_stack_data()
                else:
                    self._add_output(f"❌ Ошибка добавления")
            else:
                self._add_output(f"❌ Метод push не реализован")
        except Exception as e:
            self._add_output(f"❌ Ошибка: {e}")
    
    def _pop(self):
        if fff(self):
            self._add_output(f"\n➖ POP (удаление)")
            self._add_output(f"   Язык: {self.active_language}")
        
            try:
                if hasattr(self.current_backend, 'pop'):
                    result = self.current_backend.pop()
                    if result:
                        self._add_output(f"   Результат: Успешно удалено")
                    else:
                        self._add_output(f"⚠ Стек пуст или ошибка удаления")
                else:
                    self._add_output(f"❌ Метод pop не реализован")
            except Exception as e:
                self._add_output(f"❌ Ошибка: {e}")
        else: self._add_output(f" Может создашь Stack для начала?")

    
    def _is_empty(self):
        if fff(self):
            self._add_output(f"\n🔍 IS EMPTY (проверка на пустоту)")
            self._add_output(f"   Язык: {self.active_language}")
            try:
                if hasattr(self.current_backend, 'isEmpty'):
                    is_empty = self.current_backend.isEmpty()
                    status = "ПУСТ" if is_empty else "НЕ ПУСТ"
                    self._add_output(f"   Результат: Стек {status}")
                else:
                    self._add_output(f"❌ Метод isEmpty не реализован")
            except Exception as e:
                self._add_output(f"❌ Ошибка: {e}")
        else: self._add_output(f" Может создашь Stack для начала?")
    
    def _count(self):
        if fff(self):
            self._add_output(f"\n📊 COUNT (подсчет элементов)")
            self._add_output(f"   Язык: {self.active_language}")
        
            try:
                if hasattr(self.current_backend, 'count'):
                    count = self.current_backend.count()
                    self._add_output(f"   Количество элементов: {count}")
                else:
                    self._add_output(f"❌ Метод count не реализован")
            except Exception as e:
                self._add_output(f"❌ Ошибка: {e}")
        else: self._add_output(f" Может создашь Stack для начала?")
    
    def _clear(self):
        if fff(self):
            self._add_output(f"\n🧹 CLEAR (очистка стека)")
            self._add_output(f"   Язык: {self.active_language}")
            try:
                if hasattr(self.current_backend, 'clear'):
                    self.current_backend.clear()
                    self._add_output(f"   Результат: Стек очищен")
                    Flag.remove(self.active_language)
                    if self.active_language == "Python" and hasattr(self.current_backend, 'get_stack_data'):
                        self.stack_data = self.current_backend.get_stack_data()
                    else:
                        self.stack_data = []
                else:
                    self._add_output(f"❌ Метод clear не реализован")
            except Exception as e:
                self._add_output(f"❌ Ошибка: {e}")
        else: self._add_output(f" Может создашь Stack для начала?")
    
    def _display_content(self):
        if fff(self):
            self._add_output(f"\n📋 СОДЕРЖИМОЕ СТЕКА")
            self._add_output(f"   Язык: {self.active_language}")
        
            content = self.current_backend.display()
            for line in content.split('\n'):
                if line.strip():
                    self._add_output(f"   {line}")
        else: self._add_output(f" Может создашь Stack для начала?")
    
    def _safe_exit(self):
        response = messagebox.askyesno("Подтверждение", "Выйти из программы?")
        if response:
            self._add_output(f"\n👋 Завершение работы...")
            self.root.after(500, lambda: (self.root.quit(), self.root.destroy(), sys.exit(0)))
    
    def _button_action(self, button_num):
        button_name = self.button_texts[button_num]
        
        self._add_output(f"\n{'='*31}")
        self._add_output(f"ДЕЙСТВИЕ: {button_name}")
        self._add_output(f"ЯЗЫК: {self.active_language}")
        self._add_output(f"БЭКЕНД: {type(self.current_backend).__name__}")
        self._add_output(f"{'='*31}")
        
        actions = [
            self._create_stack,
            self._push,
            self._pop,
            self._is_empty,
            self._count,
            self._clear,
            self._display_content,
            self._safe_exit
        ]
        
        if button_num < len(actions):
            actions[button_num]()
        
        self._add_output(f"\n{'─'*31}")
    
    def _clear_output(self):
        self.output_text.delete(1.0, END)
        self._add_output("ВЫВОД ОЧИЩЕН")
        self._add_output("=" * 30)
        self._add_output(f"Текущий язык: {self.active_language}")
        self._add_output("Состояние флагов:")
        for lang, flag in self.language_flags.items():
            status = "АКТИВЕН" if flag else "неактивен"
            self._add_output(f"  {lang}: {status}")
    
    def _create_interface(self):
        main_container = Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        left_frame = Frame(main_container, bg='#f5f5f5')
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        top_frame = Frame(left_frame, bg='#ffffff', relief=RAISED, bd=2)
        top_frame.pack(fill=X, pady=(0, 20))
        
        Label(top_frame, text="Выбор языка", font=("Arial", 12, "bold"), 
              bg='#007bff', fg='white', padx=10, pady=5).pack(fill=X)
        
        arrows_container = Frame(top_frame, bg='#ffffff', padx=20, pady=20)
        arrows_container.pack()
        
        self.counter_text = StringVar()
        self.counter_text.set(f"1/{len(self.texts)}")
        
        counter_label = Label(arrows_container, 
                             textvariable=self.counter_text,
                             font=("Arial", 11, "bold"),
                             bg='#ffffff',
                             fg='#007bff')
        counter_label.pack(pady=(0, 10))
        
        arrows_display_frame = Frame(arrows_container, bg='#ffffff')
        arrows_display_frame.pack()
        
        left_btn = ArrowButton(arrows_display_frame, "left", 60, "#007bff", self._scroll_left)
        left_btn.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        self.display_frame = Frame(arrows_display_frame,
                                   bg='white',
                                   highlightbackground="#007bff",
                                   highlightcolor="#007bff",
                                   highlightthickness=2,
                                   relief="solid",
                                   bd=0,
                                   width=200,
                                   height=80)
        self.display_frame.grid(row=0, column=1, padx=10, pady=10)
        self.display_frame.pack_propagate(False)
        
        self.display_text = StringVar()
        self.display_text.set(self.texts[self.current_index])
        
        display_label = Label(self.display_frame,
                             textvariable=self.display_text,
                             font=("Arial", 10),
                             bg='white',
                             fg='#333333',
                             wraplength=180,
                             justify="center")
        display_label.pack(expand=True, fill=BOTH, padx=10, pady=10)
        
        right_btn = ArrowButton(arrows_display_frame, "right", 60, "#28a745", self._scroll_right)
        right_btn.grid(row=0, column=2, padx=(10, 0), pady=10)
        
        bottom_frame = Frame(left_frame, bg='#ffffff', relief=RAISED, bd=2)
        bottom_frame.pack(fill=BOTH, expand=True)
        
        Label(bottom_frame, 
              text="Операции со стеком", 
              font=("Arial", 12, "bold"),
              bg='#28a745',
              fg='white',
              padx=10,
              pady=5).pack(fill=X)
        
        buttons_container = Frame(bottom_frame, bg='#ffffff', padx=20, pady=20)
        buttons_container.pack(fill=BOTH, expand=True)
        
        style = ttk.Style()
        style.configure("Custom.TButton", padding=10, font=("Arial", 10))
        
        self.button_texts = [
            "1. Создать стек (init)",
            "2. Push (добавить)", 
            "3. Pop (удалить)",
            "4. Is Empty (проверить пустоту)",
            "5. Count (подсчитать)",
            "6. Clear (очистить)",
            "7. Отобразить содержимое",
            "8. Завершение"
        ]
        
        for i in range(8):
            btn = ttk.Button(buttons_container, 
                            text=self.button_texts[i],
                            style="Custom.TButton",
                            command=lambda idx=i: self._button_action(idx))
            btn.pack(fill=X, pady=3)
        
        status_frame = Frame(main_container, bg='#ffffff', width=250, relief=SUNKEN, bd=2)
        status_frame.pack(side=RIGHT, fill=Y, padx=(10, 0))
        status_frame.pack_propagate(False)
        
        Label(status_frame, 
              text="СТЕК", 
              font=("Arial", 14, "bold"),
              bg='#007bff',
              fg='white',
              padx=10,
              pady=10).pack(fill=X)
        
        output_container = Frame(status_frame, bg='#f8f9fa', padx=10, pady=10)
        output_container.pack(fill=BOTH, expand=True)
        
        text_frame = Frame(output_container)
        text_frame.pack(fill=BOTH, expand=True)
        
        self.output_text = Text(text_frame,
                                wrap=WORD,
                                font=("Consolas", 10),
                                bg='white',
                                fg='#212529',
                                relief=FLAT,
                                bd=1,
                                height=20)
        self.output_text.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)
        
        bottom_buttons_frame = Frame(status_frame, bg='#ffffff', pady=10)
        bottom_buttons_frame.pack(fill=X, side=BOTTOM, padx=10)
        
        clear_button = ttk.Button(bottom_buttons_frame,
                                 text="Очистить вывод",
                                 command=self._clear_output)
        clear_button.pack(fill=X)
        
        self._add_output("ПРОГРАММА ЗАПУЩЕНА")
        self._add_output("=" * 30)
        self._add_output("Доступные операции со стеком:")
        self._add_output("  • Создать стек (init)")
        self._add_output("  • Push (добавить элемент)")
        self._add_output("  • Pop (удалить элемент)")
        self._add_output("  • Is Empty (проверить пустоту)")
        self._add_output("  • Count (подсчитать элементы)")
        self._add_output("  • Clear (очистить стек)")
        self._add_output("  • Отобразить содержимое")
        self._add_output("=" * 30)
        self._add_output("Начальное состояние флагов:")
        for lang, flag in self.language_flags.items():
            status = "АКТИВЕН" if flag else "неактивен"
            self._add_output(f"  {lang}: {status}")
        self._add_output("\n" + "=" * 30)

if __name__ == "__main__":
    app = StackApp()