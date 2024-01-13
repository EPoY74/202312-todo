from tkinter import *
from tkinter import ttk

root = Tk()

def Hello(event):
    print("Hello world!!!")

btn = Button(
    root,  # родительское окно
    text="Click me",  # Надпись на кнопке
    width=30, height=5,  # размеры кнопки ширина и высота
    bg="white", fg="black"  # цвет фона и цвет надписи 
)
btn.pack()
root.mainloop()