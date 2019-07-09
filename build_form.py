#! python
import json
import os
import socket
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfile
import gc
import ast
import re

new_form = ''
ip_entry_socket = ''
code_line = []
fmt_parameter = []
example_text = []
no_type_string = []
checkpoint = 0
setting_file = (os.getcwd() + '/Settings.txt')
message = ''
flag_for_save_json = 0


def select_close():
    try:
        line = listbox.get(1.0, END)
        if line is not '\n':
            answer = messagebox.askyesno('Возможно будут утеряны даннные', 'Форма не пуста, '
                                                                           'не забудьте сохранить шаблон.'
                                                                           '\nЗакрыть программу?')
            if answer:
                sys.exit()
        else:
            sys.exit()
    except Exception as err:
        messagebox.showwarning('Ошибка при закрытии программы', 'str(%s)' % err)


def create_form():
    global create, message, no_type_string, checkpoint
    list_locale = {0: 'Locale - RU', 1: 'Locale - EN', 2: 'Locale - BY'}
    value_locate = {'Locale - EN': "en_EN.UTF-8", 'Locale - RU': "ru_RU.UTF-8", 'Locale - BY': "be_BY.UTF-8"}

    def exit_setting():
        try:
            create.destroy()
        except Exception as err:
            messagebox.showwarning('Ошибка при закрытии программы', 'str(%s)' % err)

    def update_parameters():
        global tmp_line, json_insert, json_settings, lines_dict, checkpoint, message
        check = 0
        try:
            line = listbox.get(1.0, END)
            if line is not '\n' or None:
                answer = messagebox.askyesno('Возможно будут утеряны даннные', 'Форма не пуста.\n'
                                                                               'Очистить форму и создать новый шаблон?')
                if not answer:
                    check = 1
                    raise Exception
            gc.collect()  # clear memory
            listbox.delete(1.0, END)
            listbox2.delete(0, END)
            checkpoint = 0
            message = ''
            result_signs = mess_symbol.get()
            if result_signs == 0 or result_signs > 80:
                messagebox.showwarning('Error', 'Количество знаков в строке не должно быть 0 или больше 80')
            result_paper = message_paper.get()
            if result_paper == 0 or result_paper > 80:
                messagebox.showinfo('Error', 'Ширина бумаги не должна быть 0 или больше 80')
            lines_dict = []
            select = locale_select.get()
            locale = value_locate.get(select)
            version = version_symbol.get()
            json_settings = {"columns": result_signs, "paperWidth": result_paper, "locale": locale,
                             "version": version, "lines": lines_dict}
            json_insert = json.dumps(json_settings, sort_keys=False, indent=4, ensure_ascii=False)
            listbox.insert(1.0, json_insert)
            tmp_line = listbox.get(1.0, END)
            create.destroy()
        except Exception as err:
            if check == 0:
                messagebox.showwarning('Ошибка при добавлении', 'str(%s)' % err)

    message_paper = IntVar()
    mess_symbol = IntVar()
    version_symbol = IntVar()
    create = Toplevel()
    create.title("Выбрать параметры шаблона")
    create.geometry("360x200")
    paper_entry = Entry(create, textvariable=message_paper)
    paper_entry.grid(column=2, row=1)
    paper_entry.config(width=28)
    label_paper = Label(create, text="Ширина бумаги 1-80", width=22, height=1, font='times 11', relief=GROOVE)
    label_paper.grid(column=1, row=1)
    label_paper.config(bg='#e84343')
    label_symbol = Label(create, text="Кол-во знаков в строке 1-80", width=22, height=1, font='times 11', relief=GROOVE)
    label_symbol.grid(column=1, row=2)
    label_symbol.config(bg='#e84343')
    symbol_entry = Entry(create, textvariable=mess_symbol)
    symbol_entry.grid(column=2, row=2)
    symbol_entry.config(width=28)
    label_version = Label(create, text="Версия", width=22, height=1, font='times 11', relief=GROOVE)
    label_version.grid(column=1, row=3)
    label_version.config(bg='#e84343')
    version_entry = Entry(create, textvariable=version_symbol)
    version_entry.grid(column=2, row=3)
    version_entry.config(width=28)
    btn_cancel = Button(create, text="Закрыть", command=exit_setting, width=8, height=1, font='times 11',
                        relief=GROOVE, activebackground='light blue')
    btn_cancel.place(relx=0.85, rely=0.9, anchor="c")
    apply_form = Button(create, text="Применить", width=9, height=1, command=update_parameters, font='times 11',
                        relief=GROOVE, activebackground='light blue')
    apply_form.place(relx=0.6, rely=0.9, anchor="c")
    locale_select = StringVar(root)
    locale_select.set(list_locale.get(0))
    locale_menu = OptionMenu(create, locale_select, *list_locale.values())
    locale_menu.grid(column=1, row=4)
    locale_menu.config(width=24, height=1, relief=GROOVE, activebackground='light blue')
    create.mainloop()


def apply_global_text():
    global new_form, ip_address, ip_entry_socket, finish, checkpoint, example_text, \
        no_type_string, message, flag_for_save_json
    ip_entry_socket = ip_address.get()
    temp_line = listbox.get(1.0, END)
    try:
        if not ip_entry_socket == '' or not temp_line == '\n':
            listbox2.delete(0, END)
            text_dict = {}
            finish_view = {}
            data_dict = []
            if temp_line.find("null"):
                temp_line = re.sub("null", "None", temp_line)
            text_dict = eval(temp_line)
            new_form = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False)
            core = 10001
            if checkpoint == 1:
                if flag_for_save_json == 0:
                    message = {"id": 107, "data": {"preview": "true", "docPrintTemplate": text_dict}}
                elif flag_for_save_json == 1:
                    message_dict = {}
                    message_dict = ast.literal_eval(message)
                    message = message_dict
                data_dict = message.get('data')
                size_example = len(no_type_string)
                for item in range(size_example):
                    data_dict.update({no_type_string[item]: example_text[item]})
                message.update(data_dict)
            else:
                message = '{"id": 107, "data": {"preview": "true", "docPrintTemplate": %s}}' % new_form
            try:
                global port
                port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port.connect((str(ip_entry_socket), core))
                port.send(str(message).encode())
                data = port.recv(10000).decode()
                data_dict = eval(data)
                finish = data_dict.get('data')
                if finish is None:
                    port.close()
                    listbox2.delete(0, END)
                    errcode = data_dict.get('errCode')
                    errmsg = data_dict.get('errMsg')
                    finish_view = [str(data_dict), 'errCode = ' + str(errcode), 'errMsg = ' + str(errmsg)]
                    for line in finish_view:
                        listbox2.insert(END, line)
                else:
                    finish_view = finish.get('docText')
                    listbox2.delete(0, END)
                    for line in finish_view:
                        listbox2.insert(END, line)
                    port.close()
            except Exception as er:
                messagebox.showwarning('Error', 'Ошибка при подключении \n\n%s' % er)
            finally:
                port.close()
        else:
            messagebox.showwarning('Error', 'Вы не создали шаблон или не ввели адрес в поле: \n"IP для запроса" \n')
    except Exception as er:
        messagebox.showwarning('Error', 'Ошибка !!! \n\n%s' % er)


def settings_change():
    global setting_file, json_insert, json_settings

    try:
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
            text = listbox.get(1.0, END)
            if text is not "\n" or '':
                text_dict = eval(text)
                if type(text_dict) is dict:
                    line_settings = {"settings": settings_parameter}
                    text_dict.update(line_settings)
                    new_json = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False, skipkeys=True)
                    listbox.delete(1.0, END)
                    listbox.insert(1.0, new_json)
                    settings_window.destroy()
                else:
                    messagebox.showwarning('Ошибка при добавлении параметра.', 'Возможно не создан шаблон.')
                    settings_window.destroy()
            else:
                messagebox.showwarning('Ошибка при добавлении параметра.', 'Возможно не создан шаблон.')
                settings_window.destroy()

        settings_window = Toplevel()
        settings_window.title("Выбрать параметры шаблона")
        settings_window.geometry("600x250")
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
        check4 = Checkbutton(settings_window, text='{"pCharSize":"std_size"}', variable=check_var4, onvalue=1,
                             offvalue=0)
        check4.place(relx=0.1, rely=0.4, anchor=W)
        check_var5 = BooleanVar()
        check_var5.set(0)
        check5 = Checkbutton(settings_window, text='{"pCharSize":"dbl_height"}', variable=check_var5, onvalue=1,
                             offvalue=0)
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
        check8 = Checkbutton(settings_window, text='["aCutPaper", "partial"]', variable=check_var8, onvalue=1,
                             offvalue=0)
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
        apply_form = Button(settings_window, text="Применить", width=9, height=1, command=survey_of_choice,
                            font='times 11',
                            relief=GROOVE, activebackground='light blue')
        apply_form.place(relx=0.92, rely=0.93, anchor="c")
    except Exception as err:
        messagebox.showwarning('Ошибка при добавлении', 'str(%s)' % err)


def add_string():
    global tmp_fmt_parameter, var_list, var_line, fmt_list, list_no_standard_type, checkpoint, \
        example_text, no_type_string, flag_add_string
    var_line = ''
    var_list = []
    fmt_list = []
    flag_add_string = 0
    tmp_fmt_parameter = []
    list_option_select = []
    list_no_standard_type = []
    list_type_menu = {0: "Тип не установлен", 1: "Сумма денежных средств", 2: "Количество товара", 3: "Дата/время",
                      4: "Дата", 5: "Время"}
    code_type_menu = {"Тип не установлен": "%ls", "Сумма денежных средств": "t_curr", "Количество товара": "t_qty",
                      "Дата/время": "t_datetime", "Дата": "t_date", "Время": "t_time"}

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

    def new_apply_string():
        global temp_string, fmt_parameter, code_line, flag_add_string
        try:
            flag_add_string = 1
            temp_string = {"var": code_line, "fmt": fmt_parameter}
            text = listbox.get(1.0, END)
            if '"lines"' in text:
                text_dict = eval(text)
                value_lines = text_dict.get("lines")
                value_lines.append(temp_string)
                text_dict.update({"lines": value_lines})
                new_json = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False)
                listbox.delete(0.0, END)
                listbox.insert(1.0, new_json)
                fmt_parameter.clear()
                code_line.clear()
                string_window.destroy()
            else:
                messagebox.showwarning('Ошибка при добавлении параметра.', 'Возможно не создан шаблон.')
                string_window.destroy()
        except Exception as err:
            messagebox.showwarning('Ошибка при добавлении', 'str(%s)' % err)

    def new_add(flag):

        global tmp_code, tmp_fmt_parameter, code_line, fmt_parameter, checkpoint, example_text, no_type_string
        tmp_code = ''
        tmp_fmt_parameter = ''
        select = ''
        parameter_choice = ''

        def date_time_checkbox(form):
            global tmp_fmt_parameter, view
            date_time_parameter = ''
            view = form

            def apply_date_time():
                global date_time_parameter, tmp_fmt_parameter, view, example_text, checkpoint, no_type_string
                tmp_data_time = '2030-01-01 10:10:10'
                tmp_data = '2030-01-01'
                tmp_time = '10:10:10'
                date_parameter_decoding = {0: "%d.%m.%Y", 1: "%Y.%m.%d", 2: "%d-%m-%y",
                                           3: "%y-%m-%d", 4: "%d-%m-%Y", 5: "%Y-%m-%d"}
                time_parameter_decoding = {0: "%H-%M-%S", 1: "%H:%M:%S", 2: "%H-%M", 3: "%H:%M"}
                if view == 'data_time':
                    choice_date = check_var_date.get()
                    choice_time = check_var_time.get()
                    date_parameter = date_parameter_decoding.get(choice_date)
                    time_parameter = time_parameter_decoding.get(choice_time)
                    date_time_parameter = str(date_parameter) + ' ' + str(time_parameter)
                    tmp_fmt_parameter = date_time_parameter
                    example = option_entry.get()
                    example_text.append(tmp_data_time)
                    no_type_string.append(example)
                elif view == 'date':
                    choice_date = check_var_date.get()
                    date_parameter = date_parameter_decoding.get(choice_date)
                    tmp_fmt_parameter = date_parameter
                    example = option_entry.get()
                    example_text.append(tmp_data)
                    no_type_string.append(example)
                elif view == 'time':
                    choice_time = check_var_time.get()
                    time_parameter = time_parameter_decoding.get(choice_time)
                    tmp_fmt_parameter = time_parameter
                    example = option_entry.get()
                    example_text.append(tmp_time)
                    no_type_string.append(example)
                checkpoint = 1
                code_line.append(tmp_code)
                fmt_parameter.append(tmp_fmt_parameter)
                list_option_select.append(select)
                listbox_option_select.delete(0, END)
                option_entry.delete(0, END)
                for line in list_option_select:
                    listbox_option_select.insert(END, line)
                    real_list.append(line)
                data_time_window.destroy()

            if form == 'data_time':
                data_time_window = Toplevel()
                data_time_window.title('Выбор отображения параметра даты и времени')
                data_time_window.geometry("200x400")
                data_time_window.config(bg='#E6E6FA')
                label_date = Label(data_time_window, text="Date Parameter", height=1, width=14, font='times 10',
                                   relief=GROOVE)
                label_date.place(x=10, y=10)
                label_date.config(bg='#7FFFD4')
                check_var_date = IntVar(value=0)
                check_var_date.set(0)
                check1 = Radiobutton(data_time_window, text="dd.mm.yyyy", variable=check_var_date, value=0)
                check1.place(x=10, y=40)
                check2 = Radiobutton(data_time_window, text="yyyy.mm.dd", variable=check_var_date, value=1)
                check2.place(x=10, y=60)
                check3 = Radiobutton(data_time_window, text="dd-mm-yy", variable=check_var_date, value=2)
                check3.place(x=10, y=80)
                check4 = Radiobutton(data_time_window, text="yy-mm-dd", variable=check_var_date, value=3)
                check4.place(x=10, y=100)
                check5 = Radiobutton(data_time_window, text="dd-mm-yyyy", variable=check_var_date, value=4)
                check5.place(x=10, y=120)
                check6 = Radiobutton(data_time_window, text="yyyy-mm-dd", variable=check_var_date, value=5)
                check6.place(x=10, y=120)
                label_time = Label(data_time_window, text="Time Parameter", height=1, width=14, font='times 10',
                                   relief=GROOVE)
                label_time.place(x=10, y=210)
                label_time.config(bg='#7FFFD4')
                check_var_time = IntVar(value=0)
                check_var_time.set(0)
                check9 = Radiobutton(data_time_window, text="HH-MM-SS", variable=check_var_time, value=0)
                check9.place(x=10, y=230)
                check10 = Radiobutton(data_time_window, text="HH:MM:SS", variable=check_var_time, value=1)
                check10.place(x=10, y=250)
                check11 = Radiobutton(data_time_window, text="HH-MM", variable=check_var_time, value=2)
                check11.place(x=10, y=270)
                check12 = Radiobutton(data_time_window, text="HH:MM", variable=check_var_time, value=3)
                check12.place(x=10, y=290)
                button_apply = Button(data_time_window, text="Применить вид дата/время", width=22, font='times 11',
                                      command=apply_date_time, relief=GROOVE, activebackground='light blue')
                button_apply.place(x=100, y=340, anchor="c")
            elif form == 'date':
                data_time_window = Toplevel()
                data_time_window.title('Выбор отображения параметра даты')
                data_time_window.geometry("200x300")
                data_time_window.config(bg='#E6E6FA')
                label_date = Label(data_time_window, text="Date Parameter", height=1, width=14, font='times 10',
                                   relief=GROOVE)
                label_date.place(x=10, y=10)
                label_date.config(bg='#7FFFD4')
                check_var_date = IntVar(value=0)
                check_var_date.set(0)
                check1 = Radiobutton(data_time_window, text="dd.mm.yyyy", variable=check_var_date, value=0)
                check1.place(x=10, y=40)
                check2 = Radiobutton(data_time_window, text="yyyy.mm.dd", variable=check_var_date, value=1)
                check2.place(x=10, y=60)
                check3 = Radiobutton(data_time_window, text="dd.mm.yy", variable=check_var_date, value=2)
                check3.place(x=10, y=80)
                check4 = Radiobutton(data_time_window, text="yy.mm.dd", variable=check_var_date, value=3)
                check4.place(x=10, y=100)
                check5 = Radiobutton(data_time_window, text="dd-mm-yy", variable=check_var_date, value=4)
                check5.place(x=10, y=120)
                check6 = Radiobutton(data_time_window, text="yy-mm-dd", variable=check_var_date, value=5)
                check6.place(x=10, y=140)
                check7 = Radiobutton(data_time_window, text="dd-mm-yyyy", variable=check_var_date, value=6)
                check7.place(x=10, y=160)
                check8 = Radiobutton(data_time_window, text="yyyy-mm-dd", variable=check_var_date, value=7)
                check8.place(x=10, y=180)
                button_apply = Button(data_time_window, text="Применить вид дата/время", width=22, height=1,
                                      command=apply_date_time, font='times 11')
                button_apply.place(x=100, y=240, anchor="c")
            elif form == 'time':
                data_time_window = Toplevel()
                data_time_window.title('Выбор отображения параметра даты и времени')
                data_time_window.geometry("200x250")
                data_time_window.config(bg='#E6E6FA')
                check_var_date = IntVar(value=0)
                check_var_date.set(0)
                label_time = Label(data_time_window, text="Time Parameter", height=1, width=14, font='times 10',
                                   relief=GROOVE)
                label_time.place(x=10, y=10)
                label_time.config(bg='#7FFFD4')
                check_var_time = IntVar(value=0)
                check_var_time.set(0)
                check9 = Radiobutton(data_time_window, text="HH-MM-SS", variable=check_var_time, value=0)
                check9.place(x=10, y=30)
                check10 = Radiobutton(data_time_window, text="HH:MM:SS", variable=check_var_time, value=1)
                check10.place(x=10, y=50)
                check11 = Radiobutton(data_time_window, text="HH-MM", variable=check_var_time, value=2)
                check11.place(x=10, y=70)
                check12 = Radiobutton(data_time_window, text="HH:MM", variable=check_var_time, value=3)
                check12.place(x=10, y=90)
                button_apply = Button(data_time_window, text="Применить вид дата/время", width=22, height=1,
                                      command=apply_date_time, font='times 11')
                button_apply.place(x=100, y=130, anchor="c")
            mainloop()

        def no_std_name(name):
            global no_type_string, example_text, checkpoint

            def exit_setting():
                try:
                    window.destroy()
                except Exception as err:
                    messagebox.showwarning('Ошибка при закрытии окна', '%s' % err)

            def update_parameters():
                global example_text, checkpoint
                checkpoint = 1
                example = message_name_entry.get()
                example_text.append(example)
                window.destroy()

            checkpoint = 0
            no_type_string.append(name)
            message_name_entry = StringVar()
            window = Toplevel()
            window.title("Выбрать параметры шаблона")
            window.geometry("287x200")
            name_entry = Entry(window, textvariable=message_name_entry)
            name_entry.grid(column=1, row=2)
            name_entry.config(width=35)
            label_name = Label(window, text="Введите примерный текст который будет \nотображаться для параметра: %s"
                                            % no_type_string[-1], width=35, height=2, font='times 11', relief=GROOVE)
            label_name.grid(column=1, row=1)
            btn_cancel = Button(window, text="Закрыть", command=exit_setting, width=8, height=1, font='times 11',
                                relief=GROOVE, activebackground='light blue')
            btn_cancel.place(relx=0.85, rely=0.9, anchor="c")
            apply_string = Button(window, text="Применить", width=9, height=1, command=update_parameters,
                                  font='times 11', relief=GROOVE, activebackground='light blue')
            apply_string.place(relx=0.57, rely=0.9, anchor="c")

        def search_parameter_no_standard_string(input_parameter, input_type):
            global tmp_code, tmp_fmt_parameter, parameter_choice
            code_type = code_type_menu.get(input_type)
            if code_type == '%ls':
                tmp_code = input_parameter
                tmp_fmt_parameter = "{%s}" % input_parameter + "%ls"
                no_std_name(input_parameter)
            else:
                tmp_code = input_parameter + '|' + code_type
                if code_type == "t_curr":
                    tmp_fmt_parameter = "{%s}" % input_parameter + "%.2f"
                elif code_type == "t_qty":
                    tmp_fmt_parameter = "{%s}" % input_parameter + "%.3f"
                elif code_type == "t_datetime":
                    date_time_checkbox('data_time')
                elif code_type == "t_date":
                    date_time_checkbox('date')
                elif code_type == "t_time":
                    date_time_checkbox('time')
            option_entry.delete(0, END)

        def search_parameter_standard_string(input_parameter):

            global tmp_code, tmp_fmt_parameter, parameter_choice
            list_fmt_d = ('#002', '#003', '#004', '#005', '#021', '#022')
            list_fmt_parameter_d = {'#002': 'Рег.№ КСА в СКНО:%d', '#003': 'УНП:%d', '#004': '№ Регистрации: %d',
                                    '#005': 'Количество перерег.: %d', '#021': '№ Отчета из БЭП: %d',
                                    '#022': '№ Смены: %d'}
            list_fmt_u = '#001'
            list_fmt_parameter_u = {'#001': 'Серийный № КСА(БУ) :%u'}
            list_fmt_s = '#020'
            list_fmt_parameter_s = {'#020': 'UID СКНО:%s'}
            list_fmt_f = ('#030', '#031', '#032', '#033', '#034', '#035')
            list_fmt_parameter_f = {'#030': 'Итог по док. %f', '#031': 'Пред-итог %f',
                                    '#032': 'Скидка/надб. на пред-итог %f', '#033': 'Сумарная скидка/надб. по поз. %f',
                                    '#034': 'Общая скидка/надб. по док. %f',
                                    '#035': 'Скидка/надб. на поз. в чек прод/возвр. %f'}
            list_fmt_structure_tm = ('#025', '#026', '#027', '#028', '#029')
            tmp_code = code_options.get(input_parameter)
            if tmp_code in list_fmt_d:
                tmp_fmt_parameter = list_fmt_parameter_d.get(tmp_code)
            elif tmp_code in list_fmt_u:
                tmp_fmt_parameter = list_fmt_parameter_u.get(tmp_code)
            elif tmp_code in list_fmt_s:
                tmp_fmt_parameter = list_fmt_parameter_s.get(tmp_code)
            elif tmp_code in list_fmt_f:
                tmp_fmt_parameter = list_fmt_parameter_f.get(tmp_code)
            elif tmp_code in list_fmt_structure_tm:
                date_time_checkbox('data_time')

        if flag == 0:
            select_standard = standard_option_select.get()
            select = select_standard
            search_parameter_standard_string(select_standard)
        elif flag == 1:
            select_entry = entry_selection.get()
            type_select_entry = no_standard_type_select.get()
            select = select_entry
            search_parameter_no_standard_string(select_entry, type_select_entry)
        code_line.append(tmp_code)
        fmt_parameter.append(tmp_fmt_parameter)
        list_option_select.append(select)
        listbox_option_select.delete(0, END)
        for item in list_option_select:
            listbox_option_select.insert(END, item)
            real_list.append(item)

    def new_std_str():
        new_add(0)

    def new_no_std_str():
        new_add(1)

    def del_select():
        global real_list, fmt_parameter, code_line
        select = list(listbox_option_select.curselection())
        select.reverse()
        for i in select:
            listbox_option_select.delete(i)
            del list_option_select[i]
            del fmt_parameter[i]
            del code_line[i]

        real_list = list(listbox_option_select.get(0, END))

    def clear_list():
        global fmt_parameter, code_line
        fmt_parameter.clear()
        code_line.clear()
        listbox_option_select.delete(0, END)
        list_option_select.clear()

    def move_up():
        global fmt_parameter, code_line
        idxs = listbox_option_select.curselection()
        if not idxs:
            return
        for pos in idxs:
            if pos != 0:
                text = listbox_option_select.get(pos)
                listbox_option_select.delete(pos)
                listbox_option_select.insert(pos - 1, text)
                fmt_parameter[pos], fmt_parameter[pos - 1] = fmt_parameter[pos - 1], fmt_parameter[pos]
                code_line[pos], code_line[pos - 1] = code_line[pos - 1], code_line[pos]

    def move_down():
        global fmt_parameter, code_line
        idxs = listbox_option_select.curselection()
        if not idxs:
            return
        for pos in idxs:
            text = listbox_option_select.get(pos)
            listbox_option_select.delete(pos)
            listbox_option_select.insert(pos + 1, text)
            fmt_parameter[pos], fmt_parameter[pos + 1] = fmt_parameter[pos + 1], fmt_parameter[pos]
            code_line[pos], code_line[pos + 1] = code_line[pos + 1], code_line[pos]

    real_list = []
    entry_selection = StringVar()
    string_window = Toplevel()
    string_window.title("Добавление строки в шаблон")
    string_window.geometry("620x550")
    string_window.config(bg='#E6E6FA')
    standard_option_select = StringVar(string_window)
    standard_option_select.set(list_options_menu.get(0))
    label_menu = Label(string_window, text='Стандартные :', height=1, width=18, font='times 11', relief=GROOVE)
    label_menu.grid(column=1, row=1)
    label_menu.config(bg='#e7f236')
    option_menu = OptionMenu(string_window, standard_option_select, *list_options_menu.values())
    option_menu.grid(column=2, row=1)
    option_menu.config(width=50, height=1, relief=GROOVE, activebackground='light blue')
    no_standard_type_select = StringVar(string_window)
    no_standard_type_select.set(list_type_menu.get(0))
    label_menu_type = Label(string_window, text='Типы не стандартных:', height=1, width=18, font='times 11',
                            relief=GROOVE)
    label_menu_type.grid(column=1, row=3)
    label_menu_type.config(bg='#e7f236')
    option_menu_type = OptionMenu(string_window, no_standard_type_select, *list_type_menu.values())
    option_menu_type.grid(column=2, row=3)
    option_menu_type.config(width=50, height=1, relief=GROOVE, activebackground='light blue')
    button_menu = Button(string_window, width=10, height=1, text="Добавить", command=new_std_str,
                         relief=GROOVE, activebackground='light blue')
    button_menu.grid(column=3, row=1)
    label_entry = Label(string_window, text='Не стандартные :', height=1, width=18, font='times 11', relief=GROOVE)
    label_entry.grid(column=1, row=2)
    label_entry.config(bg='#e7f236')
    option_entry = Entry(string_window, textvariable=entry_selection)
    option_entry.grid(column=2, row=2)
    option_entry.config(width=55)
    button_entry = Button(string_window, width=10, height=1, text="Добавить", command=new_no_std_str,
                          relief=GROOVE, activebackground='light blue')
    button_entry.grid(column=3, row=2)
    listbox_option_select = Listbox(string_window, width=55, height=15, font=('times', 12), selectbackground='BLUE')
    listbox_option_select.place(x=50, y=200)
    label_option_select = Label(string_window, text='Список выбранных параметров', height=1, width=25, font='times 11',
                                relief=RIDGE)
    label_option_select.place(x=165, y=175)
    label_option_select.config(bg='#7FFFD4')
    del_element_button = Button(string_window, width=15, height=1, text="Удалить элемент", command=del_select,
                                relief=GROOVE, activebackground='light blue')
    del_element_button.place(x=135, y=510)
    clear_button = Button(string_window, width=15, height=1, text="Очистить список", command=clear_list,
                          relief=GROOVE, activebackground='light blue')
    clear_button.place(x=275, y=510)
    move_up__button = Button(string_window, width=3, height=1, text="▲", command=move_up,
                             relief=GROOVE, activebackground='light blue')
    move_up__button.place(x=505, y=230)
    move_down__button = Button(string_window, width=3, height=1, text="▼", command=move_down,
                               relief=GROOVE, activebackground='light blue')
    move_down__button.place(x=505, y=270)
    apply_form = Button(string_window, text="Применить", width=9, command=new_apply_string, font='times 11',
                        relief=GROOVE, activebackground='light blue')
    apply_form.place(relx=0.91, rely=0.96, anchor="c")

    mainloop()


def save_global_text():
    global message
    temp_line = listbox.get(1.0, END)
    if not temp_line == '\n':
        check = 0
        try:
            if temp_line is not '\n' or None:
                if temp_line.find("null"):
                    temp_line = re.sub("null", "None", temp_line)
                text_dict = eval(temp_line)
                finish_file = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False)
                file = asksaveasfile(defaultextension=".json")
                if file:
                    file.write(message)
                    file.close()
            else:
                check = 1
                raise Exception
        except Exception as err:
            if check == 0:
                messagebox.showwarning('Ошибка при сохранении файла', 'str(%s)' % err)
    else:
        messagebox.showwarning('Error', 'Вы не создали шаблон ! \n')


def send_printer():
    global port, finish, data_100
    temp_line = listbox.get(1.0, END)
    if not temp_line == '\n':
        if temp_line.find("null"):
            temp_line = re.sub("null", "None", temp_line)
        data = ''
        text_dict = eval(temp_line)
        last_form = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False)
        core = 10001
        try:
            message_get_state = '{"id": 100}'
            massage = '{"id": 107, "data": {"preview": false, "docPrintTemplate": %s}}' % last_form
            port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port.connect((str(ip_entry_socket), core))
            port.send(message_get_state.encode())
            data_100 = port.recv(10000).decode()
            port.send(massage.encode())
            data = port.recv(10000).decode()
            if re.search(data_100, '"status":2'):
                raise Exception
        except Exception as er:
            messagebox.showwarning('Error', 'Ошибка при отправке на печать.\nВозможно не включен принтер\n'
                                            '\nОтвет на запрос:\n%s\n%s\n%s' % (er, data, data_100))
        finally:
            port.close()
    else:
        messagebox.showwarning('Error', 'Вы не создали шаблон ! \n')


def get_view_json():
    global new_form, finish, checkpoint, example_text, no_type_string, message, flag_add_string, flag_for_save_json

    def exit_json_view():
        textbox.delete(1.0, END)
        json_window.destroy()

    def save_json():
        global message, flag_for_save_json
        edit_dict = {}
        edit_line = textbox.get(1.0, END)
        edit_dict = eval(edit_line)
        message = {}
        message = json.dumps(edit_dict, sort_keys=False, indent=4, ensure_ascii=False)
        for_data_edit_dict = edit_dict.get('data')
        doc_print_for_data_edit_dict = for_data_edit_dict.get("docPrintTemplate")
        new_json_edit = json.dumps(doc_print_for_data_edit_dict, sort_keys=False, indent=4, ensure_ascii=False)
        listbox.delete(0.0, END)
        listbox.insert(END, new_json_edit)
        flag_for_save_json = 1
        json_window.destroy()

    temp_line = listbox.get(1.0, END)
    if not temp_line == '\n':
        if temp_line.find("null"):
            temp_line = re.sub("null", "None", temp_line)
        text_dict = eval(temp_line)
        new_form = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False)
        if checkpoint == 1:
            if flag_for_save_json == 0:
                message = {"id": 107, "data": {"preview": "true", "docPrintTemplate": text_dict}}
                data_dict = message.get('data')
                size_example = len(no_type_string)
                for item in range(size_example):
                    data_dict.update({no_type_string[item]: example_text[item]})
                message = json.dumps(message, sort_keys=False, indent=4, ensure_ascii=False)
            elif flag_for_save_json == 1:
                if flag_add_string == 1:
                    message_dict = {}
                    message_dict = ast.literal_eval(message)
                    data_dict = message_dict.get('data')
                    doc_print_for_data_dict = data_dict.get("docPrintTemplate")
                    doc_print_for_data_dict.update(text_dict)
                    size_example = len(no_type_string)
                    for item in range(size_example):
                        data_dict.update({no_type_string[item]: example_text[item]})
                    message = json.dumps(message_dict, sort_keys=False, indent=4, ensure_ascii=False)
                elif flag_add_string == 0:
                    message = {"id": 107, "data": {"preview": "true", "docPrintTemplate": text_dict}}
                    data_dict = message.get('data')
                    size_example = len(no_type_string)
                    for item in range(size_example):
                        data_dict.update({no_type_string[item]: example_text[item]})
                    message = json.dumps(message, sort_keys=False, indent=4, ensure_ascii=False)
        else:
            message = '{"id": 107, "data": {"preview": "true", "docPrintTemplate": %s}}' % new_form
        json_window = Toplevel()
        json_window.title("Просмотр Json")
        json_window.geometry("765x420")
        textbox = Text(json_window, width=83, height=21, font=('Courier', 11), selectbackground='light blue')
        textbox.place(x=5, y=10)
        btn_save = Button(json_window, text='Сохранить', command=save_json, relief=GROOVE,
                          activebackground='light blue')
        btn_save.place(x=550, y=390)
        btn_save.config(width=13)
        btn_exit = Button(json_window, text='Закрыть', command=exit_json_view, relief=GROOVE,
                          activebackground='light blue')
        btn_exit.place(x=657, y=390)
        btn_exit.config(width=13)
        textbox.delete(1.0, END)
        textbox.insert(END, message)
        json_window.mainloop()
    else:
        messagebox.showwarning('Ошибка.', 'Вы не создали шаблон.')


def save_text_for_db():
    global listbox

    def exit_setting():
        try:
            save_db_window.destroy()
        except Exception as err:
            messagebox.showwarning('Ошибка при закрытии программы', 'str(%s)' % err)

    def save_parameters():
        global listbox
        try:
            temp_line = listbox.get(1.0, END)
            if not temp_line == '\n':
                if temp_line is not '\n' or None:
                    if temp_line.find("null"):
                        temp_line = re.sub("null", "None", temp_line)
                    text_dict = eval(temp_line)
                    finish_file = json.dumps(text_dict, sort_keys=False, indent=4, ensure_ascii=False)
                    db_json = {"doc_type": doc_type_entry.get(), "index_number": index_entry.get(),
                               "version": version_entry.get(), "template": finish_file,
                               "example": example_text_for_template, "description": description_entry.get()}
                    new_json = json.dumps(db_json, sort_keys=False, indent=4, ensure_ascii=False, skipkeys=True)
                    file = asksaveasfile(defaultextension=".json")
                    if file:
                        file.write(new_json)
                        file.close()
                    save_db_window.destroy()
        except Exception as err:
            messagebox.showwarning('Ошибка при сохранении файла', 'str(%s)' % err)
            save_db_window.destroy()

    try:
        text = listbox.get(1.0, END)
        if text is "\n" or '':
            messagebox.showwarning('Ошибка при добавлении параметра.',
                                   'Возможно не создан шаблон. Либо не сгенерирован.')
        else:
            save_db_window = Toplevel()
            save_db_window.title("Выбрать параметры шаблона для БД")
            save_db_window.geometry("420x200")
            doc_type_entry = IntVar()
            index_entry = IntVar()
            version_symbol = IntVar()
            example_text_for_template = str("{\"id\":107, \"data\":{\n\"preview\":true,\n\"cashierId\":\"Бубыкин В.Б."
                                            "\",\n\"currCode\":\"BYN\",\n\"docNum\":48281002,\n\n\"items\":[\n\t"
                                            "{\"name\":\"Товар 1\", \"codeType\":1, \"code\":\"12345678\","
                                            " \"qty\":2000, \"cost\":370, \"cost2\":400, \"taxes\":[\"в т.ч."
                                            " НДС по ставке 20%: 0.62\"]},\n\t{\"name\":\"Товар 2\","
                                            " \"codeType\":0, \"code\":\"\", \"qty\":33,\"cost\":100,"
                                            " \"cost2\":100}\n]\n}}")
            description_entry = StringVar()
            doc_type = Entry(save_db_window, textvariable=doc_type_entry)
            doc_type.grid(column=2, row=1)
            doc_type.config(width=28)
            label_doc_type = Label(save_db_window, text="Введите тип документа(doc_type(int))", width=30, height=1,
                                   font='times 11', relief=GROOVE)
            label_doc_type.grid(column=1, row=1)
            label_doc_type.config(bg='#e84343')
            label_description = Label(save_db_window, text="Введите description(str)", width=30, height=1,
                                      font='times 11', relief=GROOVE)
            label_description.grid(column=1, row=3)
            label_description.config(bg='#e84343')
            description = Entry(save_db_window, textvariable=description_entry)
            description.grid(column=2, row=3)
            description.config(width=28)
            index = Entry(save_db_window, textvariable=index_entry)
            index.grid(column=2, row=2)
            index.config(width=28)
            label_index = Label(save_db_window, text="Введите индекс(index_number(int))", width=30,
                                height=1, font='times 11', relief=GROOVE)
            label_index.grid(column=1, row=2)
            label_index.config(bg='#e84343')
            label_version = Label(save_db_window, text="Версия", width=30, height=1, font='times 11', relief=GROOVE)
            label_version.grid(column=1, row=4)
            label_version.config(bg='#e84343')
            version_entry = Entry(save_db_window, textvariable=version_symbol)
            version_entry.grid(column=2, row=4)
            version_entry.config(width=28)
            btn_cancel = Button(save_db_window, text="Закрыть", command=exit_setting, width=8, height=1,
                                font='times 11', relief=GROOVE, activebackground='light blue')
            btn_cancel.place(relx=0.85, rely=0.9, anchor="c")
            apply_form = Button(save_db_window, text="Сохранить", width=9, height=1, command=save_parameters,
                                font='times 11', relief=GROOVE, activebackground='light blue')
            apply_form.place(relx=0.6, rely=0.9, anchor="c")
            save_db_window.mainloop()
    except Exception as err:
        messagebox.showwarning('Ошибка при закрытии программы', 'str(%s)' % err)


root = Tk()
root.title("Build Form")
root.wm_geometry("%dx%d+%d+%d" % (1355, 700, 0, 0))
frame = ttk.Frame(root, padding=(7, 7, 11, 11))
frame.grid(column=0, row=0, sticky='news')
ip_label = Label(frame, text='IP для запроса:', width=12, height=1, font='times 11', relief=GROOVE)
ip_label.grid(column=10, row=1)
ip_label.config(bg='#e7f236')
ip_address = StringVar()
ip_entry = Entry(frame, textvariable=ip_address)
ip_entry.grid(column=11, row=1)
btn_info = Button(frame, text="Создать шаблон", command=create_form, relief=GROOVE, activebackground='light blue')
btn_info.grid(column=2, row=1)
btn_info.config(width=13)
btn_trade = Button(frame, text="Добавить строку", command=add_string, relief=GROOVE, activebackground='light blue')
btn_trade.grid(column=5, row=1)
btn_trade.config(width=13)
btn_master = Button(frame, text='Выбор настроек', command=settings_change, relief=GROOVE, activebackground='light blue')
btn_master.grid(column=6, row=1)
btn_master.config(width=13)
btn_close = Button(frame, command=select_close, text='Выход', relief=GROOVE,
                   activeforeground='white', activebackground='#b20101')
btn_close.grid(column=9, row=1)
btn_close.config(width=11)
apply = Button(root, text="Сгенерировать шаблон", command=apply_global_text, activebackground='light blue',
               relief=GROOVE, fg="black", font='times 11')
apply.place(relx=0.07, rely=0.96, anchor="c")
apply.config(width=19)
view_json = Button(root, text="Просмотреть json", command=get_view_json, activebackground='light blue',
                   relief=GROOVE, fg="black", font='times 11')
view_json.place(relx=0.192, rely=0.96, anchor="c")
view_json.config(width=19)
save = Button(root, text="Сохранить шаблон", command=save_global_text, activebackground='light blue', relief=GROOVE,
              fg="black", font='times 11')
save.place(relx=0.94, rely=0.96, anchor="c")
save.config(width=15)
save_db = Button(root, text="Сохранить для БД", command=save_text_for_db,
                 activebackground='light blue', relief=GROOVE, fg="black", font='times 11')
save_db.place(relx=0.84, rely=0.96, anchor="c")
save_db.config(width=15)
printer = Button(root, text="Распечатать", command=send_printer, activebackground='light blue', relief=GROOVE,
                 fg="black", font='times 11')
printer.place(relx=0.75, rely=0.96, anchor="c")
printer.config(width=12)
listbox = Text(root, width=87, height=33, font=('Courier', 11), selectbackground='light blue')
listbox.place(x=5, y=65)
edit_menu = Menu(listbox, tearoff=0)
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: listbox.event_generate('<<Cut>>'))
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: listbox.event_generate('<<Copy>>'))
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: listbox.event_generate('<<Paste>>'))
listbox.bind("<Button-3>", lambda event: edit_menu.post(event.x_root, event.y_root))
listbox2 = Listbox(root, width=61, height=32, font=('Courier', 11), selectbackground='BLUE')
listbox2.place(x=795, y=64)
root.mainloop()
