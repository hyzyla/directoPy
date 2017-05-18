from tkinter import *
import sys
from tkinter.ttk import *
from tkinter.messagebox import showerror, askokcancel, showinfo, askyesnocancel
from tkinter.filedialog import asksaveasfile, askopenfile
import os


class Application(Frame):

    @classmethod
    def get_filename(cls):
        folder_path = os.path.abspath(os.path.join(sys.argv[0], ".."))
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
        else:
            for i in range(1, 999999999):
                if not os.path.isfile(os.path.join(folder_path, "Новий файл {}.txt".format(i))):
                    file_name = os.path.join(folder_path, "Новий файл {}.txt".format(i))
                    break
        return os.path.join(folder_path, file_name)

    @classmethod
    def main(cls, filename=None):
        NoDefaultRoot()
        cls.root = Tk()
        if filename is None:
            cls.root.title("Текстовий редактор - " + os.path.basename(cls.get_filename()))
        else:
            cls.root.title("Текстовий редактор - " + os.path.basename(filename))
        cls.app = cls(cls.root, filename)
        cls.app.grid(sticky=N+S+E+W)
        cls.root.grid_columnconfigure(0, weight=1)
        cls.root.grid_rowconfigure(0, weight=1)
        cls.root.mainloop()

    def __init__(self, root, filename=None):
        super().__init__(root)
        self.filename = ""
        self.create_widgets()
        self.configure_widgets(filename)
        self.bind_widgets()
        self.grid_widgets()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def new_file(self, event=None):
        Application.main()

    def open_command(self, event=None):
        file = askopenfile(parent=self, mode='r')
        if file is not None:
            Application.main(file.name)

    def donothing(self):
        print("Nothing")

    def undo(self, event=None):
        self.text_box.edit_undo()

    def unhighlight(self, event=None):
        try:
            self.text_box.tag_delete("red")
        except:
            print("Не можу видалити виділення")

    def find(self, event=None):
        try:
            selection = self.text_box.selection_get()
            self.highlight_pattern(selection)
        except:
            print("Не можу виділити текст")

    def highlight_pattern(self, pattern, start="1.0", end="end"):
        self.text_box.tag_delete("red")
        start = self.text_box.index(start)
        end = self.text_box.index(end)
        self.text_box.mark_set("matchStart", start)
        self.text_box.mark_set("matchEnd", start)
        self.text_box.mark_set("searchLimit", end)
        self.text_box.tag_config("red", background='red')
        count = IntVar(self)
        while True:
            index = self.text_box.search(pattern, "matchEnd", "searchLimit", count=count, regexp=False)

            if index == "":
                break
            if count.get() == 0:
                break
            self.text_box.mark_set("matchStart", index)
            self.text_box.mark_set("matchEnd", '{}+{}c'.format(index, len(pattern)))
            self.text_box.tag_add("red", "matchStart", "matchEnd")

    def change_reg(self, event=None):
        self.cut()
        try:
            text = self.text_box.clipboard_get()
        except:
            print("Не можу змінити регістр")
        else:
            self.text_box.clipboard_clear()
            self.text_box.clipboard_append(text.swapcase())
            self.paste()

    def exit_command(self, event=None):
        ask = askyesnocancel(parent=self, title="Вийти", message="Ви хочете зберегти поточний файл?")
        if ask:
            self.save_command()
            Application.root.destroy()
        elif ask is not None:
            Application.root.destroy()

    def open_file(self, event=None, file_name=None):
        print("Д: Відкриття файлу...")
        self.text_box.delete("0.0", END)
        if os.path.isfile(file_name):
            text = open(file_name, 'r', encoding='utf8')
            self.text_box.insert('0.0', text.read())
            print("І: Файл було успішно відкрито...")
        else:
            print("І: Файл не існує...")

    def save_command(self, event=None):
        print(self.filename)
        file = open(self.filename, 'w')
        if file != '':
            data = self.text_box.get('1.0', END + '-1c')
            file.write(data)
            file.close()
            showinfo(parent=self, title="Успіх", message="Файл було успішно збережено")

    def save_as_command(self, event=None):
        file = asksaveasfile(parent=self, mode='w', initialfile=self.filename)
        if file is not None:
            # slice off the last character from get, as an extra return is added
            data = self.text_box.get('1.0', END + '-1c')
            file.write(data)
            file.close()
            showinfo(parent=self, title="Успіх", message="Файл було успішно збережено")

    def about_prog(self, event=None):
        w = Tk()
        w.title("Відомості про програму")
        w.minsize(width=400, height=100)
        options = dict(padx=10, pady=14, sticky=W+N)

        Label(w, text='Програма:').grid(column=0, row=0, **options)
        Label(w, text="Текстовий редактор").grid(column=1, row=0, **options)

        Label(w, text='Автор:').grid(column=0, row=1, **options)
        Label(w, text="Гизила Євгеній").grid(column=1, row=1, **options)

        Label(w, text='Версія:').grid(column=0, row=2, **options)
        Label(w, text="0.01").grid(column=1, row=2, **options)

        Label(w, text='Ліцензія:').grid(column=0, row=2, **options)
        Label(w, text="LGPL").grid(column=1, row=2, **options)

        Label(w, text='Опис:').grid(column=0, row=3, **options)
        Label(w, text="Текстовий редактор — комп'ютерна програма-застосунок,\n"
                      "призначена для створення й зміни текстових файлів \n"
                      "(вставки, видалення та копіювання тексту, заміни \n"
                      "змісту, сортування рядків), а також їх перегляду на \n"
                      "моніторі, виводу на друк, пошуку фрагментів тексту\n").grid(column=1, row=3, **options)

        w.mainloop()

    def copy(self, event=None):
        self.text_box.clipboard_clear()
        try:
            text = self.text_box.get("sel.first", "sel.last")
        except:
            print("Не можу скопіювати текс")
        else:
            self.text_box.clipboard_append(text)

    def cut(self, event=None):
        self.copy()
        try:
            self.text_box.delete("sel.first", "sel.last")
        except:
            print("Не можу вирізати текст")

    def paste(self, event=None):
        try:
            text = self.text_box.selection_get(selection='CLIPBOARD')
            self.text_box.insert('insert', text)
        except:
            print("Не можу вставити текст!")

    def create_widgets(self):
        self.text_box = Text(self, height=30, width=80, undo=True)
        self.menu_bar = Menu(self)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.task_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu = Menu(self.menu_bar, tearoff=0)

    def configure_widgets(self, filename=None):
        if filename is None:
            self.filename = self.get_filename()
        else:
            self.filename = filename

        self.open_file(file_name=self.filename)

        self.file_menu.add_command(label="Відкрити", command=self.open_command, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Новий", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Зберегти", command=self.save_command, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Зберегти як", command=self.save_as_command, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Вийти", command=self.exit_command, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        self.edit_menu.add_command(label="Відмінити", command=self.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Копіювати", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Вирізати", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Вставити", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Знайти виділене слово", command=self.find, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Зняти виділення", command=self.unhighlight, accelerator="Ctrl+G")
        self.menu_bar.add_cascade(label="Редагувати", menu=self.edit_menu)

        self.task_menu.add_command(label="Замінити регістр у слові", command=self.change_reg, accelerator="Ctrl+R")
        self.menu_bar.add_cascade(label="Завдання", menu=self.task_menu)

        self.help_menu.add_command(label="Про програму", command=self.about_prog)
        self.menu_bar.add_cascade(label="Відомості", menu=self.help_menu)
        Application.root.config(menu=self.menu_bar)

    def bind_widgets(self):
        self.bind_all("<Control-N>", self.new_file)
        self.bind_all("<Control-n>", self.new_file)
        self.bind_all("<Control-O>", self.open_command)
        self.bind_all("<Control-o>", self.open_command)
        self.bind_all("<Control-Shift-S>", self.save_as_command)
        self.bind_all("<Control-Shift-s>", self.save_as_command)
        self.bind_all("<Control-S>", self.save_command)
        self.bind_all("<Control-s>", self.save_command)
        self.bind_all("<Control-q>", self.exit_command)
        self.bind_all("<Control-Q>", self.exit_command)
        self.text_box.bind("<Control-z>", self.undo)
        self.text_box.bind("<Control-Z>", self.undo)
        self.text_box.bind("<Control-c>", self.copy)
        self.text_box.bind("<Control-C>", self.copy)
        self.text_box.bind("<Control-x>", self.cut)
        self.text_box.bind("<Control-X>", self.cut)
        self.text_box.bind("<Control-V>", self.paste)
        self.text_box.bind("<Control-v>", self.paste)
        self.text_box.bind("<Control-f>", self.find)
        self.text_box.bind("<Control-F>", self.find)
        self.text_box.bind("<Control-r>", self.change_reg)
        self.text_box.bind("<Control-R>", self.change_reg)
        self.text_box.bind("<Control-G>", self.unhighlight)
        self.text_box.bind("<Control-g>", self.unhighlight)

    def grid_widgets(self):
        options = dict(sticky=N+E+S+W, padx=3, pady=4)
        self.text_box.grid(column=0, row=0, **options)

if __name__ == '__main__':
    Application.main()
