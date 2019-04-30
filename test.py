from tkinter import *

class Test(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)

def test():
    r = Tk()
    t = Test(r)
    t.pack(fill='both', expand=1)
    r.mainloop()

editmenu = Menu(frame, tearoff=0)
editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: listbox.event_generate('<<Cut>>'))
editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: listbox.event_generate('<<Copy>>'))
editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: listbox.event_generate('<<Paste>>'))
menubar.add_cascade(label="Edit", menu=editmenu)


if __name__ == '__main__':
    test()