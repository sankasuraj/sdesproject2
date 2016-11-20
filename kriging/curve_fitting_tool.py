import Tkinter
from Tkinter import *
from tkFileDialog import askopenfilename
from kriging import *

#For running multiple commands using one click
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func        
    
class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent=parent
        self.filename = None
        self.initialize()
    
    def initialize(self):
        self.grid()        
        Label(self, text="To Train a model out of a csv file click Train Model").grid(row=0, sticky=W)
        create = Tkinter.Button(self,text="Create Model",command = self.Window2, height = 1, width = 10)
        create.grid(row=1, column=0, sticky='W', padx=5, pady=5)
        Label(self, text="To get the values using a model click Use Model").grid(row=2, sticky=W)
        use = Tkinter.Button(self,text="Use Model",command = self.OpenFile, height = 1, width = 10)
        use.grid(row=3, column=0, sticky='W', padx=5, pady=5)
        
        quit = Tkinter.Button(self,text="Quit",command = self.destroy)
        quit.grid(row=4, column=1, sticky='E', padx=5, pady=5)
        self.grid_columnconfigure(0,weight=1)
        #self.resizable(True,False)

    #For Opening a file
    def OpenFile(self):
        self.filename = askopenfilename()
        if self.filename:
            self.window2.labelVariable.set(self.filename)

    #def Quit(self):
	#result = messagebox.askyesno("Continue?", "Do you want to quit?")
    def Window2(self):
        self.window2 = Toplevel()
        self.window2.title("Window 2")
        self.window2.transient(self)

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self.window2,textvariable=self.entryVariable)
        self.entry.grid(row=0,column=0, sticky='NSEW',columnspan=3, pady=5, padx=5)
        self.entryVariable.set("Please choose a file using import button")
        
        import_data = Button(self.window2,text="Import Data",command=self.OpenFile)
        import_data.grid(row=1,column=2, rowspan=2, sticky='NSEW')

        back = Button(self.window2, text="Back",command = self.window2.destroy, height = 1, width = 10)
        back.grid(row=1, column=0, sticky='E',pady=5, padx=5)

        next = Button(self.window2,text="Next",command=combine_funcs(self.Window3,
            self.window2.destroy), height = 1, width = 10)
        next.grid(row=1, column=1, sticky='E',pady=5, padx=5)
        self.window2.labelVariable = Tkinter.StringVar()
        label2 = Label(self.window2,textvariable=self.window2.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label2.grid(row=2,column=0,columnspan=2,sticky='EW')
        self.window2.labelVariable.set("Hello !")

    def Window3(self):
        self.window3 = Toplevel()
        self.window3.title("Progress Bar")
        self.window3.transient(self)
        next = Button(self.window3,text="Next",command=combine_funcs(self.Window4,self.window3.destroy))
        next.grid(row=0, column=1, sticky='E',pady=5, padx=5)
        back = Button(self.window3,text="Back",command = combine_funcs(self.window3.destroy,self.Window2))
        back.grid(row=0, column=0, sticky='E',pady=5, padx=5)
        self.window3.labelVariable = Tkinter.StringVar()
        label3 = Label(self.window3,textvariable=self.window3.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label3.grid(row=2,column=0,columnspan=2,sticky='EW')
        self.window3.labelVariable.set("Hello !")
        self.Progress()
        #self.topButton.pack()

    def Progress(self):
        model_name = '../../model.csv'
        training_data_file = self.filename
        start = time()
        x, y = read_data(training_data_file)
        x1, y1, x2, y2 = divide_data(x, y)
        self.window3.labelVariable.set('Preliminary model initialising...')
        prelim_model = Solve(x1, y1)
        self.window3.labelVariable.set('Preliminary model initialised')
        self.window3.labelVariable.set('Preliminary model training started')
        prelim_model.train()
        self.window3.labelVariable.set('Preliminary model trained')

        self.window3.labelVariable.set('Estimating error using preliminary model')
        error = estimate_error(prelim_model, x2, y2)
        self.window3.labelVariable.set('Error estimation done')

        self.window3.labelVariable.set('Final model initialising...')
        final_model = Solve(x, y)
        self.window3.labelVariable.set('Final model initialised')
        self.window3.labelVariable.set('Final model training started') 
        self.window3.labelVariable.set('Esimated time remaining is approximately ' 
            + str(int(1.45 * (time()-start))) + ' seconds' )
        final_model.train()
        self.window3.labelVariable.set('Final model trained')

        end = time()
        self.window3.labelVariable.set('Total time taken = ' + str(int(end-start)) + ' seconds')
        self.window3.labelVariable.set('L2 error for the given data = ' + str(round(error, 2)))

        f = open(model_name, 'wb')
        writer = csv.writer(f, delimiter = ',')
        writer.writerow(np.concatenate([final_model.max_x, final_model.max_y]))
        writer.writerow(np.concatenate([final_model.min_x, final_model.min_y]))
        for i in range(final_model.n):
            writer.writerow(x[i])
        f.close()



    def Window4(self):
        self.window4 = Toplevel()
        self.window4.title("Model")
        save = Button(self.window4,text="Next",command = combine_funcs(self.window4.destroy,self.Window3))
        save.grid(row=0,column=1,sticky='E', pady=5, padx=5)
        back = Button(self.window4,text="Back",command = combine_funcs(self.window4.destroy,self.Window3))
        back.grid(row=0, column=0, sticky='E',pady=5, padx=5)
    def Usemodel(self):
        self.window5 = Toplevel()
        self.window5.title("New Model")

if __name__ == '__main__':
    app = simpleapp_tk(None)
    app.title('Curve Fitting Tool')
    # app.geometry("200x200")
    app.mainloop()
