# -*- coding: utf-8 -*-


from build_form import ip_entry_socket, new_form
data = ''


def request_core(form):
    global data
    ip_socket = ip_entry_socket
    core = 10001
    message = '{"id": 107, "data": {"preview": "true", "docPrintTemplate": %s}}' % form
    port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port.connect((ip_socket, core))
    port.send(message.encode())
    data = port.recv(10000).decode()
    print(data)
    port.close()
    return data


request_core(new_form)
