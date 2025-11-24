import tkinter as tk
from tkinter import messagebox
import math

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color="#333333", fg_color="white", hover_color="#444444", width=0, height=0):
        super().__init__(parent, borderwidth=0, highlightthickness=0, bg="black") 
        
        self.command = command 
        
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Configure>", self.draw) 

    def draw(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        pad = 4 
        
        self.create_oval(pad, pad, width-pad, height-pad, fill=self.bg_color, outline=self.bg_color, tags="shape")
        self.create_text(width/2, height/2, text=self.text, fill=self.fg_color, font=('Arial', 14), tags="text")

    def on_press(self, event):
        self.itemconfig("shape", fill="red") 
        self.itemconfig("text", fill="white")

    def on_release(self, event):
        self.itemconfig("shape", fill=self.bg_color)
        self.itemconfig("text", fill=self.fg_color)
        if self.command:
            self.command()


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("320x500") 
        self.root.resizable(True, True)
        self.root.configure(bg="black")

        self.input_text = tk.StringVar()

        input_frame = self.create_display()
        input_frame.pack(side=tk.TOP, fill=tk.BOTH)

        btns_frame = self.create_buttons()
        btns_frame.pack(expand=True, fill=tk.BOTH)

        self.root.bind("<Key>", self.process_key)
        
        
        self.root.bind('<Return>', lambda event: self.btn_equal())
        self.root.bind('<BackSpace>', lambda event: self.btn_backspace())
        self.root.bind('<Escape>', lambda event: self.btn_clear()) 
        

    def process_key(self, event):
        char = event.char
        
        
        if char in '0123456789.+-*/':
            self.on_click(char)

    def create_display(self):
        frame = tk.Frame(self.root, bd=0, bg="black")
       
        input_field = tk.Entry(frame, font=('Arial', 30, 'bold'), textvariable=self.input_text, 
                               bg="black", fg="#FF0000", bd=0, justify=tk.RIGHT, 
                               insertbackground="#FF0000", state="readonly", readonlybackground="black", takefocus=0)
        
        input_field.pack(side=tk.TOP, fill=tk.BOTH, ipady=20, padx=10, pady=10) 
        return frame
    
    def create_buttons(self):
        
        frame = tk.Frame(self.root, bg="black")
        
        buttons = [
            ('C', 1, 0), ('DEL', 1, 1), ('√', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3) 
        ]

        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(1, 6):
            frame.rowconfigure(i, weight=1)

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            colspan = btn[3] if len(btn) > 3 else 1
            
            cmd = lambda x=text: self.on_click(x)
            
            if text in ['/', '*', '-', '+', '=']:
                bg_c = "#292828" 
                fg_c = "white"
            elif text in ['C', 'DEL', '√']:
                bg_c = "#292828" 
                fg_c = "black"
            else:
                bg_c = "#292828" 
                fg_c = "white"

           
            rbtn = RoundedButton(frame, text=text, command=cmd, bg_color=bg_c, fg_color=fg_c)
            
            rbtn.grid(row=row, column=col, columnspan=colspan, sticky="nsew")
            
        return frame

    def on_click(self, char):
        if char == 'C':
            self.btn_clear()
        elif char == 'DEL':
            self.btn_backspace()
        elif char == '=':
            self.btn_equal()
        elif char == '√':
            self.btn_sqrt()
        else:
            current_text = self.input_text.get()
            if char == '.':
                 last_number = self.get_last_number(current_text)
                 if '.' in last_number:
                     return
            self.input_text.set(current_text + str(char))

    def get_last_number(self, text):
        import re
        parts = re.split(r'[+\-*/]', text)
        return parts[-1] if parts else ""

    def btn_clear(self):
        self.input_text.set("")

    def btn_backspace(self):
        text = self.input_text.get()
        self.input_text.set(text[:-1])

    def btn_equal(self):
        try:
            content = self.input_text.get()
            if not content: return
            allowed = set("0123456789.+-*/ ")
            if not set(content).issubset(allowed):
                raise ValueError
            result = str(eval(content)) 
            self.input_text.set(result)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль")
            self.input_text.set("")
        except Exception:
            messagebox.showerror("Ошибка", "Ошибка вычисления")

    def btn_sqrt(self):
        try:
            content = self.input_text.get()
            if not content: return
            val = float(eval(content))
            if val < 0: raise ValueError
            self.input_text.set(str(math.sqrt(val)))
        except ValueError:
             messagebox.showerror("Ошибка", "Отрицательное число")
        except Exception:
             messagebox.showerror("Ошибка", "Ошибка данных")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
