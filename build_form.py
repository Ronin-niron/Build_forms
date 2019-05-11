#! python
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

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
            label_symbol_glob = Label(frame, text="Кол-во знаков " + str(mess_symbol.get()), width=23, height=1,
                                      font='times 11', relief=GROOVE)
            label_symbol_glob.grid(column=11, row=1)
            label_symbol_glob.config(bg='#e7f236')

    def select_paper():
        global result_message
        result_message = str(message.get())
        if int(result_message) == 0 or int(result_message) > 80:
            messagebox.showwarning('Error', 'Ширина бумаги не должна быть 0 или больше 80')
        else:
            label_paper_width = Label(frame, text="Ширина бумаги " + str(message.get()), width=23, height=1,
                                      font='times 11', relief=GROOVE)
            label_paper_width.grid(column=10, row=1)
            label_paper_width.config(bg='#e7f236')
            label_paper = Label(create, text="Ширина бумаги " + str(message.get()), width=25, height=1, font='times 11',
                                relief=GROOVE)
            label_paper.grid(column=3, row=1)
            label_paper.config(bg='#e7f236')

    def update_parameters():
        global tmp_line, json_insert, json_settings, lines_dict
        listbox.delete(1.0, 5.0)
        lines_dict = []
        json_settings = {"columns": result_symbol, "paperWidth": result_message, "lines": lines_dict}
        json_insert = json.dumps(json_settings, sort_keys=False, indent=4)
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
    temp_line = listbox.get(1.0, END)
    for line in temp_line.split("\n"):
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
            type_choice_label = Label(doc_window, text="Тип документа " + str(value), width=25, height=1,
                                      font='times 11', relief=GROOVE)
            type_choice_label.grid(column=3, row=1)
            type_choice_label.config(bg='#e7f236')

    print_list_doc_type()
    type_selection = IntVar()
    doc_window = Toplevel()
    doc_window.title("Выбрать параметры шаблона")
    doc_window.geometry("510x250")
    list_doc_type = Label(doc_window, text=line_doc_type, width=50, height=10, font=('times', 12))
    list_doc_type.place(relx=.2, rely=.2, anchor="n")
    type_choice = Button(doc_window, width=25, height=1, text='Установить тип документа', command=select_type)
    type_choice.grid(column=1, row=1)
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
        check_value_name = ({"pAlignment": "left"}, {"pAlignment": "center"}, {"pAlignment": "right"},
                            {"pCharSize": "std_size"}, {"pCharSize": "dbl_height"},
                            {"pBarcodeW": 1, "pBarcodeH": 50, "pBarcodeHRI": "below"}, ["aPrintBarcode", "code128"],
                            ["aCutPaper", "partial"], ["aSendRawData", "1D284C0600304520200101"],
                            ["aSendRawData", "1B2500"], ["aSendRawData", "1B2501"], ["aSendRawData", "1B4A40"])
        place_dict = -1
        settings_parameter = []
        for choice in check_value_list:
            place_dict += 1
            if choice:
                insert_check_dict = check_value_name[place_dict]
                settings_parameter.append(insert_check_dict)
        line_settings = {"settings": settings_parameter}
        json_settings.update(line_settings)
        new_json = json.dumps(json_settings, sort_keys=False, indent=4, ensure_ascii=False, skipkeys=True)
        listbox.delete(1.0, END)
        listbox.insert(1.0, new_json)
        settings_window.destroy()

    settings_window = Toplevel()
    settings_window.title("Выбрать параметры шаблона")
    settings_window.geometry("700x250")
    check_var1 = BooleanVar()
    check_var1.set(0)
    check1 = Checkbutton(settings_window, text="Выравнивание по левому краю", variable=check_var1, onvalue=1,
                         offvalue=0)
    check1.place(relx=0.1, rely=0.1, anchor=W)
    check_var2 = BooleanVar()
    check_var2.set(0)
    check2 = Checkbutton(settings_window, text="Выравнивание по центру", variable=check_var2, onvalue=1, offvalue=0)
    check2.place(relx=0.1, rely=0.2, anchor=W)
    check_var3 = BooleanVar()
    check_var3.set(0)
    check3 = Checkbutton(settings_window, text="Выравнивание по правому краю", variable=check_var3, onvalue=1,
                         offvalue=0)
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
    check6 = Checkbutton(settings_window, text='{"pBarcodeW":1, "pBarcodeH":50, "pBarcodeHRI":"below" }',
                         variable=check_var6, onvalue=1, offvalue=0)
    check6.place(relx=0.1, rely=0.6, anchor=W)
    check_var7 = BooleanVar()
    check_var7.set(0)
    check7 = Checkbutton(settings_window, text='["aPrintBarcode", "code128"]', variable=check_var7, onvalue=1,
                         offvalue=0)
    check7.place(relx=0.1, rely=0.7, anchor=W)
    check_var8 = BooleanVar()
    check_var8.set(0)
    check8 = Checkbutton(settings_window, text='["aCutPaper", "partial"]', variable=check_var8, onvalue=1, offvalue=0)
    check8.place(relx=0.1, rely=0.8, anchor=W)
    check_var9 = BooleanVar()
    check_var9.set(0)
    check9 = Checkbutton(settings_window, text='["aSendRawData", "1D284C0600304520200101"]', variable=check_var9,
                         onvalue=1, offvalue=0)
    check9.place(relx=0.1, rely=0.9, anchor=W)
    check_var10 = BooleanVar()
    check_var10.set(0)
    check10 = Checkbutton(settings_window, text='["aSendRawData", "1B2500"]', variable=check_var10, onvalue=1,
                          offvalue=0)
    check10.place(relx=0.5, rely=0.1, anchor=W)
    check_var11 = BooleanVar()
    check_var11.set(0)
    check11 = Checkbutton(settings_window, text='["aSendRawData", "1B2501"]', variable=check_var11, onvalue=1,
                          offvalue=0)
    check11.place(relx=0.5, rely=0.2, anchor=W)
    check_var12 = BooleanVar()
    check_var12.set(0)
    check12 = Checkbutton(settings_window, text='["aSendRawData", "1B4A40"]', variable=check_var12, onvalue=1,
                          offvalue=0)
    check12.place(relx=0.5, rely=0.3, anchor=W)
    apply_form = Button(settings_window, text="Apply", width=5, height=1, command=survey_of_choice, font='times 11')
    apply_form.place(relx=0.8, rely=0.9, anchor="c")


def add_string():
    list_option_select = []
    list_fmt_d = ('#002', '#003', '#004', '#005', '#021', '#022')
    list_fmt_u = '#001'
    list_fmt_s = '#020'
    list_fmt_f = ('#030', '#031', '#032', '#033', '#034', '#035')
    list_fmt_struct_tm = ('#025', '#026', '#027', '#028', '#029')
    fmt_parameter = []

    list_options_menu = {0: "Серийный номер КСА (БУ)", 1: "Регистрационный номер КСА в СККО", 2: "УНП владельца",
                         3: "Порядковый номер текущей регистрации КСА", 4: "Количество перерегистраций в БЭП",
                         5: "Уникальный идентификатор документа (СКНО)", 6: "Номер отчёта по данным из БЭП",
                         7: "Номер смены (для X-отчёта, Z-отчёта)", 8: "Текущее локальное время БУ (RTC)",
                         9: "Дата/время открытия текущей смены (для X-отчёта)",
                         10: "Дата/время открытия последней смены (для Z-отчёта)",
                         11: "Дата/время закрытия последней смены (для Z-отчёта)",
                         12: "Дата/время регистрации последнего документа", 13: "Итог по документу",
                         14: "Пред-итог по документу", 15: "Скидка (надбавка) на пред-итог",
                         16: "Суммарная скидка (надбавка) по позициям", 17: "Общая скидка (надбавка) по документу",
                         18: "Скидка (надбавка) на позицию в чеке продажи/возврата"}

    code_options = {"Серийный номер КСА (БУ)": "#001", "Регистрационный номер КСА в СККО": "#002",
                    "УНП владельца": "#003", "Порядковый номер текущей регистрации КСА": "#004",
                    "Количество перерегистраций в БЭП": "#005", "Уникальный идентификатор документа (СКНО)": "#020",
                    "Номер отчёта по данным из БЭП": "#021", "Номер смены (для X-отчёта, Z-отчёта)": "#022",
                    "Текущее локальное время БУ (RTC)": "#025",
                    "Дата/время открытия текущей смены (для X-отчёта)": "#026",
                    "Дата/время открытия последней смены (для Z-отчёта)": "#027",
                    "Дата/время закрытия последней смены (для Z-отчёта)": "#028",
                    "Дата/время регистрации последнего документа": "#029", "Итог по документу": "#030",
                    "Пред-итог по документу": "#031", "Скидка (надбавка) на пред-итог": "#032",
                    "Суммарная скидка (надбавка) по позициям": "#033", "Общая скидка (надбавка) по документу": "#034",
                    "Скидка (надбавка) на позицию в чеке продажи/возврата": "#035"}

    def apply_string():
        global temp_string, json_insert, fmt_parameter
        number_in_listbox = listbox_option_select.size()
        if number_in_listbox == 1:
            for line in listbox_option_select.get(0, END):
                code_line = code_options.get(line)
                temp_string = {"var": code_line, "fmt": fmt_parameter}
        elif number_in_listbox > 1:
            code_line = []
            for line in listbox_option_select.get(0, END):
                code_line.append(code_options.get(line))
                temp_string = {"var": code_line, "fmt": fmt_parameter}
        text = listbox.get(1.0, END)
        text_dict = []
        text_dict = eval(text)
        value_lines = text_dict.get("lines")
        if len(value_lines) != 0:
            if temp_string in value_lines:
                lines_dict.append(value_lines)
            else:
                lines_dict.append(temp_string)
        else:
            lines_dict.append(temp_string)
        text_dict.update({"lines": lines_dict})
        json_insert = json.dumps(text_dict, sort_keys=False, indent=4)
        listbox.delete(0.0, END)
        listbox.insert(1.0, json_insert)
        string_window.destroy()

    def date_time_checkbox():
        label_date = Label(string_window, text="Date Parameter", height=1, width=14, font='times 10', relief=GROOVE)
        label_date.place(x=600, y=10)
        label_date.config(bg='#7FFFD4')
        check_var_date = IntVar(value=0)
        check_var_date.set(0)
        check1 = Radiobutton(string_window, text="dd/mm/yyyy", variable=check_var_date, value=0)
        check1.place(x=600, y=40)
        check2 = Radiobutton(string_window, text="yyyy/mm/dd", variable=check_var_date, value=1)
        check2.place(x=600, y=60)
        check3 = Radiobutton(string_window, text="dd.mm.yyyy", variable=check_var_date, value=2)
        check3.place(x=600, y=80)
        check4 = Radiobutton(string_window, text="yyyy.mm.dd", variable=check_var_date, value=3)
        check4.place(x=600, y=100)
        check5 = Radiobutton(string_window, text="dd.mm.yy", variable=check_var_date, value=4)
        check5.place(x=600, y=120)
        check6 = Radiobutton(string_window, text="yy.mm.dd", variable=check_var_date, value=5)
        check6.place(x=600, y=140)
        label_time = Label(string_window, text="Time Parameter", height=1, width=14, font='times 10', relief=GROOVE)
        label_time.place(x=600, y=180)
        label_time.config(bg='#7FFFD4')
        check_var_time = IntVar(value=0)
        check_var_time.set(0)
        check7 = Radiobutton(string_window, text="HH/MM/SS", variable=check_var_time, value=0)
        check7.place(x=600, y=200)
        check8 = Radiobutton(string_window, text="HH-MM-SS", variable=check_var_time, value=1)
        check8.place(x=600, y=220)
        check9 = Radiobutton(string_window, text="HH:MM:SS", variable=check_var_time, value=2)
        check9.place(x=600, y=240)
        check10 = Radiobutton(string_window, text="HH/MM", variable=check_var_time, value=3)
        check10.place(x=600, y=260)
        check11 = Radiobutton(string_window, text="HH-MM", variable=check_var_time, value=4)
        check11.place(x=600, y=280)
        check12 = Radiobutton(string_window, text="HH:MM", variable=check_var_time, value=5)
        check12.place(x=600, y=300)

    def add():
        real_list.clear()
        select = standard_option_select.get()
        list_option_select.append(select)
        listbox_option_select.delete(0, END)
        for item in list_option_select:
            listbox_option_select.insert(END, item)
            real_list.append(item)
        if code_options.get(select) in list_fmt_d:
            if len(fmt_parameter) != 0:
                fmt_parameter.append('%d')
            else:
                fmt_parameter = '%d'
        elif code_options.get(select) in list_fmt_u:
            if len(fmt_parameter) != 0:
                fmt_parameter.append('%u')
            else:
                fmt_parameter = '%u'
        elif code_options.get(select) in list_fmt_s:
            if len(fmt_parameter) != 0:
                fmt_parameter.append('%s')
            else:
                fmt_parameter = '%s'
        elif code_options.get(select) in list_fmt_f:
            if len(fmt_parameter) != 0:
                fmt_parameter.append('%f')
            else:
                fmt_parameter = '%f'
        elif code_options.get(select) in list_fmt_struct_tm:
            date_time_checkbox()
            fmt_parameter = ''

    def add_entry():
        real_list.clear()
        select = nonstandard_option_selection.get()
        list_option_select.append(select)
        listbox_option_select.delete(0, END)
        for item in list_option_select:
            listbox_option_select.insert(END, item)
            real_list.append(item)

    def del_select():
        global real_list
        select = list(listbox_option_select.curselection())
        select.reverse()
        for i in select:
            listbox_option_select.delete(i)
            del list_option_select[i]
        real_list = list(listbox_option_select.get(0, END))

    def clear_list():
        listbox_option_select.delete(0, END)
        list_option_select.clear()

    def move_up():
        idxs = listbox_option_select.curselection()
        if not idxs:
            return
        for pos in idxs:
            if pos == 0:
                continue
            text = listbox_option_select.get(pos)
            listbox_option_select.delete(pos)
            listbox_option_select.insert(pos-1, text)

    def move_down():
        idxs = listbox_option_select.curselection()
        if not idxs:
            return
        for pos in idxs:
            text = listbox_option_select.get(pos)
            listbox_option_select.delete(pos)
            listbox_option_select.insert(pos+1, text)





    real_list = []
    fmt_parameter = []
    nonstandard_option_selection = StringVar()
    string_window = Toplevel()
    string_window.title("Добавление строки в шаблон")
    string_window.geometry("850x550")
    string_window.config(bg='#E6E6FA')
    standard_option_select = StringVar(string_window)
    standard_option_select.set(list_options_menu.get(0))
    label_menu = Label(string_window, text='Стандартные :', height=1, width=15, font='times 11', relief=GROOVE)
    label_menu.grid(column=1, row=1)
    label_menu.config(bg='#e7f236')
    option_menu = OptionMenu(string_window, standard_option_select, *list_options_menu.values())
    option_menu.grid(column=2, row=1)
    option_menu.config(width=50, height=1)
    button_menu = Button(string_window, width=10, height=1, text="Добавить", command=add)
    button_menu.grid(column=3, row=1)
    label_entry = Label(string_window, text='Не стандартные :', height=1, width=15, font='times 11', relief=GROOVE)
    label_entry.grid(column=1, row=2)
    label_entry.config(bg='#e7f236')
    option_entry = Entry(string_window, textvariable=nonstandard_option_selection)
    option_entry.grid(column=2, row=2)
    option_entry.config(width=55)
    button_entry = Button(string_window, width=10, height=1, text="Добавить", command=add_entry)
    button_entry.grid(column=3, row=2)
    listbox_option_select = Listbox(string_window, width=55, height=15, font=('times', 12), selectbackground='BLUE')
    listbox_option_select.place(x=50, y=100)
    label_option_select = Label(string_window, text='Список выбранных параметров', height=1, width=25, font='times 11',
                                relief=RIDGE)
    label_option_select.place(x=165, y=75)
    label_option_select.config(bg='#7FFFD4')
    del_element_button = Button(string_window, width=15, height=1, text="Удалить элемент", command=del_select)
    del_element_button.place(x=135, y=410)
    clear_button = Button(string_window, width=15, height=1, text="Очистить список", command=clear_list)
    clear_button.place(x=275, y=410)
    move_up__button = Button(string_window, width=3, height=1, text="▲", command=move_up)
    move_up__button.place(x=505, y=195)
    move_down__button = Button(string_window, width=3, height=1, text="▼", command=move_down)
    move_down__button.place(x=505, y=230)
    apply_form = Button(string_window, text="Apply", width=5, height=1, command=apply_string, font='times 11')
    apply_form.place(relx=0.8, rely=0.9, anchor="c")

    mainloop()


root = Tk()
root.title("Build Form")
root.wm_geometry("%dx%d+%d+%d" % (1200, 600, 0, 0))
root.config(bg='#E6E6FA')
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
btn_trade = ttk.Button(frame, text="Добавить строку", command=add_string)
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
