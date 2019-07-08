def get_view_json():
    global new_form, finish, checkpoint, example_text, no_type_string, message, flag_add_string

    def exit_json_view():
        textbox.delete(1.0, END)
        json_window.destroy()

    def save_json():
        global message, flag_for_save_json
        edit_line = textbox.get(1.0, END)
        edit_dict = eval(edit_line)
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
                    message_dict = eval(message)
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
    else:
        messagebox.showwarning('Ошибка.', 'Вы не создали шаблон.')

    json_window = Toplevel()
    json_window.title("Просмотр Json")
    json_window.geometry("765x220")
    textbox = Text(json_window, width=83, height=10, font=('Courier', 11), selectbackground='light blue')
    textbox.place(x=5, y=10)
    btn_save = Button(json_window, text='Сохранить', command=save_json, relief=GROOVE,
                      activebackground='light blue')
    btn_save.place(x=550, y=190)
    btn_save.config(width=13)
    btn_exit = Button(json_window, text='Закрыть', command=exit_json_view, relief=GROOVE,
                      activebackground='light blue')
    btn_exit.place(x=657, y=190)
    btn_exit.config(width=13)

    textbox.delete(1.0, END)
    textbox.insert(END, message)

    json_window.mainloop()