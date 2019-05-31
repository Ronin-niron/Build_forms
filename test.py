var_line = ''
var_list = []
fmt_list = []
tmp_fmt_parameter = []
list_option_select = []
list_no_standard_type = []
list_fmt_d = ('#002', '#003', '#004', '#005', '#021', '#022')
list_fmt_u = '#001'
list_fmt_s = '#020'
list_fmt_f = ('#030', '#031', '#032', '#033', '#034', '#035')
list_fmt_struct_tm = ('#025', '#026', '#027', '#028', '#029')
list_type_menu = {0: "Тип не установлен", 1: "Сумма денежных средств", 2: "Количество товара", 3: "Дата/время",
                  4: "Дата"}
code_type_menu = {"Тип не установлен": "%ls", "Сумма денежных средств": "t_curr", "Количество товара": "t_qty",
                  "Дата/время": "t_datetime", "Дата": "t_date"}

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



def add():
    global tmp_fmt_parameter, fmt_list, var_line, list_no_standard_type
    flag = 0
    real_list.clear()
    if type(fmt_parameter) is list:
        fmt_parameter.clear()
    select = standard_option_select.get()
    list_option_select.append(select)
    listbox_option_select.delete(0, END)
    for item in list_option_select:
        listbox_option_select.insert(END, item)
        real_list.append(item)
        if item in code_options:
            code = code_options.get(item)
            if code in list_fmt_d:
                if code == '#002':
                    fmt_parameter.append('№ КСА в СКНО:%d')
                elif code == '#003':
                    fmt_parameter.append('УНП:%d')
                elif code == '#004':
                    fmt_parameter.append('№ Регистрации: %d')
                elif code == '#005':
                    fmt_parameter.append('Количество перерег.: %d')
                elif code == '#021':
                    fmt_parameter.append('№ Отчета из БЭП: %d')
                elif code == '#022':
                    fmt_parameter.append('№ Смены: %d')
            elif code in list_fmt_u:
                fmt_parameter.append('Рег.№ КСА:%u')
            elif code in list_fmt_s:
                fmt_parameter.append('UID СКНО:%s')
            elif code in list_fmt_f:
                if code == '#030':
                    fmt_parameter.append('Итог по док. %f')
                elif code == '#031':
                    fmt_parameter.append('Пред-итог %f')
                elif code == '#032':
                    fmt_parameter.append('Скидка/надб. на пред-итог %f')
                elif code == '#033':
                    fmt_parameter.append('Сумарная скидка/надб. по поз. %f')
                elif code == '#034':
                    fmt_parameter.append('Общая скидка/надб. по док. %f')
                elif code == '#035':
                    fmt_parameter.append('Скидка/надб. на поз. в чек прод/возвр. %f')
            elif code in list_fmt_struct_tm:
                date_time_checkbox()
        else:
            add_entry_type = list_no_standard_type[flag]
            fmt_parameter.append(add_entry_type)
            flag += 1
            # fmt_list = [fmt_parameter]
            # fmt_parameter = fmt_list


def add_entry():
    global tmp_fmt_parameter, var_line, var_list, list_no_standard_type
    fmt_line = ''
    fmt_parameter_list = []
    real_list.clear()
    select = nonstandard_option_selection.get()
    type_select = no_standard_type_select.get()
    list_option_select.append(select)
    listbox_option_select.delete(0, END)
    for item in list_option_select:
        if len(list_option_select) == 1:
            listbox_option_select.insert(END, item)
            real_list.append(item)
            code_type = code_type_menu.get(type_select)
            if code_type == '%ls':
                var_line = select
                fmt_line = "{%s}" % item + "%ls"
                var_list.append(var_line)
            else:
                var_line = select + '|' + code_type
                var_list.append(var_line)
                if code_type == "t_curr":
                    fmt_line = "{%s}" % item + "%.2f"
                elif code_type == "t_qty":
                    fmt_line = "{%s}" % item + "%.3f"
            list_no_standard_type.append(var_line)
        else:
            listbox_option_select.insert(END, item)
            real_list.append(item)
            code_type = code_type_menu.get(type_select)
            if item not in code_options:
                if code_type == '%ls':
                    var_line = select
                    fmt_line = "{%s}" % item + "%ls"
                else:
                    var_line = select + '|' + code_type
                    if code_type == "t_curr":
                        fmt_line = "{%s}" % select + "%.2f"
                    elif code_type == "t_qty":
                        fmt_line = "{%s}" % select + "%.3f"
                if var_line not in var_list:
                    var_list.append(var_line)
                if var_line not in list_no_standard_type:
                    list_no_standard_type.append(var_line)
    if len(list_option_select) == 1:
        fmt_parameter = fmt_line
    elif len(list_option_select) == 2:
        if type(fmt_parameter) is list:
            fmt_parameter.append(fmt_line)
        else:
            fmt_parameter_list.append(fmt_parameter)
            fmt_parameter_list.append(fmt_line)
            fmt_parameter = fmt_parameter_list
    elif len(list_option_select) > 2:
        fmt_parameter.append(fmt_line)