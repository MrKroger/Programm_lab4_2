class Stack:
    def __init__(self):
        self.data = []

    def push(self, value: str):
        try:
            self.data.append(value)
            return True
        except Exception as e:
            return False

    def pop(self):
        if not self.isEmpty():
            self.data.pop()
            return True
        return False

    def isEmpty(self):
        if len(self.data) <= 0:
            return True
        return False

    def count(self): return len(self.data)

    def print_stack(self):
        for item in reversed(self.data):
            print(item)

    def clear(self):
        self.data.clear()

