import psgui as sg

layout = [[sg.Text("Enter Som")]]

window = sg.Window("hej", layout)

while True:
    event, values = window.read()
    if event is None or event == "Exit":
        break

window.close()