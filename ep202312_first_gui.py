#  https://habr.com/ru/articles/133337/

import tkinter as tki
import tkFileDialog as tkFD


root = tki.Tk()

def Hello(event):
    print("Hello world!!!")

def load_file(event):
    print("load")
    fn = tkFD.Open(root, filetypes = [('*.txt files', '.txt')]).show()

def save_file(event):
    print("Save")

def quit_exit(event):
    global root
    root.destroy()
    print("Quit")



# btn = tki.Button(
#     root,  # родительское окно
#     text="Click me",  # Надпись на кнопке
#     width=30, height=5,  # размеры кнопки ширина и высота
#     bg="white", fg="black"  # цвет фона и цвет надписи 
# )
# btn.bind("<Button-1>", Hello)
# btn.pack()
# root.mainloop()

panel_Frame = tki.Frame(root, height=60, bg='gray')
text_Frame = tki.Frame(root, height=340, width=600)

panel_Frame.pack(side='top', fill='x')
text_Frame.pack(side='bottom', fill='both', expand=1)

text_box = tki.Text(text_Frame, font='Arial 14', wrap='word')
scrollbar = tki.Scrollbar(text_Frame)

scrollbar['command'] = text_box.yview
text_box['yscrollcommand'] = scrollbar.set
text_box.pack(side='left', fill='both', expand=1)
scrollbar.pack(side='right', fill='y')

load_btn = tki.Button(panel_Frame, text='Load')
save_btn = tki.Button(panel_Frame, text='Save')
quit_btn = tki.Button(panel_Frame, text='Quit')

load_btn.bind("<Button-1>", load_file)
save_btn.bind("<Button-1>", save_file)
quit_btn.bind("<Button-1>", quit_exit)

load_btn.place(x = 10, y = 10, width = 40, height = 40)
save_btn.place(x = 60, y = 10, width = 40, height = 40)
quit_btn.place(x = 110, y = 10, width = 40, height = 40)

root.mainloop()