#simple GUI

from Tkinter import *

root=Tk()

root.title("Simple GUI")
root.geometry("200x100")

app = Frame(root)
app.grid()

#creating a label
label=Label(app, text="This is a label")
label.grid()

#creating buttons
button1 = Button(app, text="This is a button")
button1.grid()

button2 = Button(app)
button2.grid()
button2.configure(text="This is also a button")

button3 = Button(app)
button3.grid()
button3["text"] = "This will show up as well"

root.mainloop()