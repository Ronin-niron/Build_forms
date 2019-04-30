#! python

import os
import json
import subprocess
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from subprocess import PIPE
from tkinter.filedialog import askdirectory

result_symbol = 'не задан'
result_message = 'не задан'
type_selection = 'не задан'

setting_file = (os.getcwd() + '/Settings.txt')
doctype_list = {'1': '-чек продажи', '2': '-чек возврата', '3': '-чек анулирования', '4': '-новый'}


def select_close():
    try:
        sys.exit()
    except Exception:
        print('закрытия программы(select_close)', '!!!')


def create_form():
    global create, result_symbol, result_message

    def exit_setting():
        try:
            create.destroy()
        except Exception:
            print('закрытия программы(exit_setting)', '!!!')

    def change_symbol():
        global result_symbol
        result_symbol = str(mess_symbol.get())
        if int(result_symbol) == 0 or int(result_symbol) > 80:
            messagebox.showwarning('Error', 'Количество знаков в строке не должно быть 0 или больше 80')
        else:
            label_symbol = Label(create, text="Кол-во знаков " + str(mess_symbol.get()), width=25, height=1,
                                 font='times 11', relief=GROOVE)
            label_symbol.grid(column=3, row=2)
            label_symbol.config(bg='#e7f236')
            label_symbol_glob = Label(frame, text="Кол-во знаков " + str(mess_symbol.get()), width=25, height=1,
                                      font='times 11', relief=GROOVE)
            label_symbol_glob.grid(column=11, row=1)
            label_symbol_glob.config(bg='#e7f236')

    def select_paper():
        global result_message
        result_message = str(message.get())
        if int(result_message) == 0 or int(result_message) > 80:
            messagebox.showwarning('Error', 'Ширина бумаги не должна быть 0 или больше 80')
        else:
            label_paper_width = Label(frame, text="Ширина бумаги " + str(message.get()), width=25, height=1,
                                      font='times 11', relief=GROOVE)
            label_paper_width.grid(column=10, row=1)
            label_paper_width.config(bg='#e7f236')
            label_paper = Label(create, text="Ширина бумаги " + str(message.get()), width=25, height=1, font='times 11',
                                relief=GROOVE)
            label_paper.grid(column=3, row=1)
            label_paper.config(bg='#e7f236')

    def update_parameters():
        global tmp_line, json_insert, json_settings
        listbox.delete(1.0, 5.0)
        json_settings = {"columns": result_symbol, "paperWidth": result_message}
        json_insert = json.dumps(json_settings, sort_keys=True, indent=4)
        listbox.insert(1.0, json_insert)
        tmp_line = listbox.get(1.0, END)
        create.destroy()

    message = IntVar()
    mess_symbol = IntVar()
    create = Toplevel()
    create.title("Выбрать параметры шаблона")
    create.geometry("500x250")
    lab = Label(create, text="", width=50,
                height=10, font=('times', 12))
    lab.place(relx=.5, rely=.3, anchor="n")
    paper_change = Button(create, width=23, height=1, text="Ширина бумаги", command=select_paper)
    paper_change.grid(column=1, row=1)
    paper_entry = Entry(create, textvariable=message)
    paper_entry.grid(column=2, row=1)
    label_paper = Label(create, text="Ширина бумаги 1-80", width=25, height=1, font='times 11', relief=GROOVE)
    label_paper.grid(column=3, row=1)
    label_paper.config(bg='#FF0000')
    symbol_in_string = Button(create, text="Кол-во знаков в строке", width=23, height=1, command=change_symbol)
    symbol_in_string.grid(column=1, row=2)
    label_symbol = Label(create, text="Кол-во знаков не выбрано 1-80", width=25, height=1, font='times 11',
                         relief=GROOVE)
    label_symbol.grid(column=3, row=2)
    label_symbol.config(bg='#FF0000')
    symbol_entry = Entry(create, textvariable=mess_symbol)
    symbol_entry.grid(column=2, row=2)
    btn_cancel = Button(create, text="Cancel", command=exit_setting, width=5, height=1, font='times 11')
    btn_cancel.place(relx=.9, rely=.9, anchor="c")
    apply_form = Button(create, text="Apply", width=5, height=1, command=update_parameters, font='times 11')
    apply_form.place(relx=0.8, rely=0.9, anchor="c")
    create.mainloop()


def apply_global_text():
    listbox2.delete(0, END)
    tmp_line = listbox.get(1.0, END)
    for line in tmp_line.split("\n"):
        listbox2.insert(END, line)


def insert_settings():
    global tmp_line
    listbox.delete(4.0, END)
    settings = open(setting_file, 'r')
    for line in settings:
        listbox.insert(END, line)
    settings.close()


def doc_type():
    global doctype_list, type_selection

    def print_list_doc_type():
        global line_doc_type, quantity
        line_doc_type = ''
        quantity = 0
        for key, value in doctype_list.items():
            line_doc_type += str(key + value + '\n')
            quantity += 1

    def exit_doc_type():
        try:
            doc_window.destroy()
        except Exception:
            print('закрытия программы(exit_setting)', '!!!')

    def update_type():
        global type_doc
        type_doc = str(type_selection.get())
        doc_window.destroy()

    def select_type():
        value = doctype_list[str(type_selection.get())]
        if type_selection.get() == 0 or type_selection.get() > quantity:
            messagebox.showwarning('Error', 'Не верный код документа')
        else:
            type_change_glob_label = Label(frame, text="Тип документа " + str(value), width=25,
                                           font='times 11', relief=GROOVE)
            type_change_glob_label.grid(column=1, row=1)
            type_change_glob_label.config(bg='#e7f236')
            type_change_label = Label(doc_window, text="Тип документа " + str(value), width=25, height=1,
                                      font='times 11', relief=GROOVE)
            type_change_label.grid(column=3, row=1)
            type_change_label.config(bg='#e7f236')

    print_list_doc_type()
    type_selection = IntVar()
    doc_window = Toplevel()
    doc_window.title("Выбрать параметры шаблона")
    doc_window.geometry("510x250")
    list_doc_type = Label(doc_window, text=line_doc_type, width=50, height=10, font=('times', 12))
    list_doc_type.place(relx=.2, rely=.2, anchor="n")
    type_change = Button(doc_window, width=25, height=1, text='Установить тип документа', command=select_type)
    type_change.grid(column=1, row=1)
    type_entry = Entry(doc_window, textvariable=type_selection)
    type_entry.grid(column=2, row=1)
    type_change_label = Label(doc_window, text='Тип документа не выбран', width=25, height=1, font='times 11',
                              relief=GROOVE)
    type_change_label.grid(column=3, row=1)
    type_change_label.config(bg='#FF0000')
    btn_cancel = Button(doc_window, text="Cancel", command=exit_doc_type, width=5, height=1, font='times 11')
    btn_cancel.place(relx=.9, rely=.9, anchor="c")
    apply_form = Button(doc_window, text="Apply", width=5, height=1, command=update_type, font='times 11')
    apply_form.place(relx=0.8, rely=0.9, anchor="c")


def settings_change():
    global setting_file, json_insert, json_settings

    def survey_of_choice():
        global json_insert, tmp_line, json_settings
        check_value1 = check_var1.get()
        check_value2 = check_var2.get()
        check_value3 = check_var3.get()
        check_value4 = check_var4.get()
        check_value5 = check_var5.get()
        check_value6 = check_var6.get()
        check_value7 = check_var7.get()
        check_value8 = check_var8.get()
        check_value9 = check_var9.get()
        check_value10 = check_var10.get()
        check_value11 = check_var11.get()
        check_value12 = check_var12.get()
        check_value_list = (check_value1, check_value2, check_value3, check_value4, check_value5, check_value6,
                            check_value7, check_value8, check_value9, check_value10, check_value11, check_value12)
        check_value_name = {1: '"pAlignment":"left"', 2: '{"pAlignment":"center"}', 3: '{"pAlignment":"right"}',
                            4: '{"pCharSize":"std_size"}', 5: '{"pCharSize":"dbl_height"}',
                            6: '{"pBarcodeW":1, "pBarcodeH":50, "pBarcodeHRI":"below" }', 7: '["aPrintBarcode", "code128"]',
                            8: '["aCutPaper", "partial"]', 9: '["aSendRawData", "1D284C0600304520200101"]',
                            10: '["aSendRawData", "1B2500"]', 11: '["aSendRawData", "1B2501"]',
                            12: '["aSendRawData", "1B4A40"]'}
        settings = open(setting_file, 'w')
        settings.write('\n\n\n"settings":[\n')
        settings.close()
        place_dict = 1
        for choice in check_value_list:
            place_dict += 1
            if choice:
                settings = open(setting_file, 'a')
                settings.write(str(check_value_name.get(place_dict)) + '\n')
                #json_dict = json.loads(json_insert)
                #insert_check_value = dict(check_value_name.get(place_dict))
                insert_check_dict = check_value_name.get(place_dict)
                new_json = {}
                new_json.update(json_settings)
                new_json.update(eval(insert_check_dict))
                last_json = json.dumps(new_json, sort_keys=True, indent=4)
                listbox.insert(END, last_json)
                create.destroy()
                settings.close()

    settings_window = Toplevel()
    settings_window.title("Выбрать параметры шаблона")
    settings_window.geometry("700x250")
    check_var1 = BooleanVar()
    check_var1.set(0)
    check1 = Checkbutton(settings_window, text="Выравнивание по левому краю", variable=check_var1, onvalue=1, offvalue=0)
    check1.place(relx=0.1, rely=0.1, anchor=W)
    check_var2 = BooleanVar()
    check_var2.set(0)
    check2 = Checkbutton(settings_window, text="Выравнивание по центру", variable=check_var2, onvalue=1, offvalue=0)
    check2.place(relx=0.1, rely=0.2, anchor=W)
    check_var3 = BooleanVar()
    check_var3.set(0)
    check3 = Checkbutton(settings_window, text="Выравнивание по правому краю", variable=check_var3, onvalue=1, offvalue=0)
    check3.place(relx=0.1, rely=0.3, anchor=W)
    check_var4 = BooleanVar()
    check_var4.set(0)
    check4 = Checkbutton(settings_window, text='{"pCharSize":"std_size"}', variable=check_var4, onvalue=1, offvalue=0)
    check4.place(relx=0.1, rely=0.4, anchor=W)
    check_var5 = BooleanVar()
    check_var5.set(0)
    check5 = Checkbutton(settings_window, text='{"pCharSize":"dbl_height"}', variable=check_var5, onvalue=1, offvalue=0)
    check5.place(relx=0.1, rely=0.5, anchor=W)
    check_var6 = BooleanVar()
    check_var6.set(0)
    check6 = Checkbutton(settings_window, text='{"pBarcodeW":1, "pBarcodeH":50, "pBarcodeHRI":"below" }', variable=check_var6, onvalue=1, offvalue=0)
    check6.place(relx=0.1, rely=0.6, anchor=W)
    check_var7 = BooleanVar()
    check_var7.set(0)
    check7 = Checkbutton(settings_window, text='["aPrintBarcode", "code128"]', variable=check_var7, onvalue=1, offvalue=0)
    check7.place(relx=0.1, rely=0.7, anchor=W)
    check_var8 = BooleanVar()
    check_var8.set(0)
    check8 = Checkbutton(settings_window, text='["aCutPaper", "partial"]', variable=check_var8, onvalue=1, offvalue=0)
    check8.place(relx=0.1, rely=0.8, anchor=W)
    check_var9 = BooleanVar()
    check_var9.set(0)
    check9 = Checkbutton(settings_window, text='["aSendRawData", "1D284C0600304520200101"]', variable=check_var9, onvalue=1, offvalue=0)
    check9.place(relx=0.1, rely=0.9, anchor=W)
    check_var10 = BooleanVar()
    check_var10.set(0)
    check10 = Checkbutton(settings_window, text='["aSendRawData", "1B2500"]', variable=check_var10, onvalue=1, offvalue=0)
    check10.place(relx=0.5, rely=0.1, anchor=W)
    check_var11 = BooleanVar()
    check_var11.set(0)
    check11 = Checkbutton(settings_window, text='["aSendRawData", "1B2501"]', variable=check_var11, onvalue=1, offvalue=0)
    check11.place(relx=0.5, rely=0.2, anchor=W)
    check_var12 = BooleanVar()
    check_var12.set(0)
    check12 = Checkbutton(settings_window, text='["aSendRawData", "1B4A40"]', variable=check_var12, onvalue=1, offvalue=0)
    check12.place(relx=0.5, rely=0.3, anchor=W)
    apply_form = Button(settings_window, text="Apply", width=5, height=1, command=survey_of_choice, font='times 11')
    apply_form.place(relx=0.8, rely=0.9, anchor="c")




root = Tk()
root.title("Build Form")
root.wm_geometry("%dx%d+%d+%d" % (1200, 600, 0, 0))
frame = ttk.Frame(root, padding=(7, 7, 11, 11))
frame.grid(column=0, row=0, sticky=(N, S, E, W))
type_change = Label(frame, text='Тип документа не выбран', width=25, font='times 11', relief=GROOVE)
type_change.grid(column=1, row=1)
type_change.config(bg='#FF0000')
btn_info = ttk.Button(frame, text="Создать шаблон", command=create_form)
btn_info.grid(column=2, row=1)
btn_info_label = ttk.Button(frame, text="Добавить Settings", command=insert_settings)
btn_info_label.grid(column=3, row=1)
btn_develop = ttk.Button(frame, text="Тип документа", command=doc_type)
btn_develop.grid(column=4, row=1)
btn_trade = ttk.Button(frame, text="Кнопка 4")
btn_trade.grid(column=5, row=1)
btn_master = ttk.Button(frame, text='Выбор настроек', command=settings_change)
btn_master.grid(column=6, row=1)
btn_close = ttk.Button(frame, command=select_close, text='Exit')
btn_close.grid(column=9, row=1)
apply = ttk.Button(root, text="apply", command=apply_global_text)
apply.place(relx=0.035, rely=0.9, anchor="c")
label_paper_width = Label(frame, text="Бумага не выбрана", width=23, height=1, font='times 11', relief=GROOVE)
label_paper_width.grid(column=10, row=1)
label_paper_width.config(bg='#FF0000')
label_symbol_glob = Label(frame, text="Кол-во знаков не выбрано", width=23, height=1, font='times 11', relief=GROOVE)
label_symbol_glob.grid(column=11, row=1)
label_symbol_glob.config(bg='#FF0000')
listbox = Text(root, width=70, height=25, font=('times', 12), selectbackground='BLUE')
listbox.place(x=4, y=50)
edit_menu = Menu(listbox, tearoff=0)
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: listbox.event_generate('<<Cut>>'))
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: listbox.event_generate('<<Copy>>'))
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: listbox.event_generate('<<Paste>>'))
listbox.bind("<Button-3>", lambda event: edit_menu.post(event.x_root, event.y_root))
listbox2 = Listbox(root, width=70, height=25, font=('times', 12), selectbackground='BLUE')
listbox2.place(x=600, y=50)
root.mainloop()
