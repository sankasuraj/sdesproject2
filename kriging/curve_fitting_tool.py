import Tkinter
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfile
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
        self.savefile = None
        self.loadmodel = None
        self.xdata = None
        self.output = None
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
            self.window2.labelVariable.set("Now save the model using Save button")
            #window2.save_model.config(state="normal")

    def OpenFile1(self):
        self.filename = askopenfilename()
        if self.filename:
            self.window4.labelVariable.set("Now load the X data for which Y-values should be determined")

    def OpenFile2(self):
        self.filename = askopenfilename()
        if self.filename:
            self.window4.labelVariable.set("Now save the data using the Output button")

    def file_save(self):
        self.savefile = asksaveasfile(mode='w', defaultextension=".csv")
        if self.savefile is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        if self.savefile:
            self.window2.localVariable.set("Now press Next to start Training the data")

    def file_save1(self):
        self.savefile = asksaveasfile(mode='w', defaultextension=".csv")
        if self.savefile is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        if self.savefile:
            self.window4.localVariable.set("Now press Next to start the model")

    #def Quit(self):
	#result = messagebox.askyesno("Continue?", "Do you want to quit?")
    def Window2(self):
        self.window2 = Toplevel()
        self.window2.title("Window 2")
        self.window2.transient(self)
        
        import_data = Button(self.window2,text="Import Data",command=self.OpenFile)
        import_data.grid(row=1,column=0, rowspan=2, sticky='NSEW')

        save_model = Button(self.window2,text="Save Model",command=self.file_save)
        save_model.grid(row=1,column=1, rowspan=2, sticky='NSEW')

        back = Button(self.window2, text="Back",command = self.window2.destroy, height = 1, width = 10)
        back.grid(row=3, column=1, sticky='E',pady=5, padx=5)

        next = Button(self.window2,text="Next",command=combine_funcs(self.Progress,
            self.window2.destroy), height = 1, width = 10)
        next.grid(row=3, column=2, sticky='E',pady=5, padx=5)
        self.window2.labelVariable = Tkinter.StringVar()
        label2 = Label(self.window2,textvariable=self.window2.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label2.grid(row=0,column=0,columnspan=2,sticky='EW')
        self.window2.labelVariable.set("Hello! Import a CSV file using Import Button")



    def Window3(self):
        self.window3 = Toplevel()
        self.window3.title("Progress Bar")
        self.window3.transient(self)
        self.window3.labelVariable = Tkinter.StringVar()
        label3 = Label(self.window3,textvariable=self.window3.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label3.grid(row=0,column=0,columnspan=2,sticky='EW')
        self.window3.labelVariable.set("Hello !")
        next = Button(self.window3,text="Next",command=combine_funcs(self.Window4,self.window3.destroy))
        next.grid(row=1, column=1, sticky='E',pady=5, padx=5)
        #self.topButton.pack()

    def Progress(self):
        self.Window3()
        model_name = '../../model.csv'
        training_data_file = self.filename
        start = time()
        x, y = read_data(training_data_file)
        x1, y1, x2, y2 = divide_data(x, y)
        show = 'Preliminary model initialising...\n'
        self.window3.labelVariable.set(show)
        prelim_model = Solve(x1, y1)
        show += 'Preliminary model initialised\n'
        self.window3.labelVariable.set(show)
        show +='Preliminary model training started\n'
        self.window3.labelVariable.set(show)
        prelim_model.train()
        show +='Preliminary model trained\n'
        self.window3.labelVariable.set(show)
        show +='Estimating error using preliminary model\n'
        self.window3.labelVariable.set(show)
        error = estimate_error(prelim_model, x2, y2)
        show +='Error estimation done\n'
        self.window3.labelVariable.set(show)
        show +='Final model initialising...\n'
        self.window3.labelVariable.set(show)
        final_model = Solve(x, y)
        show +='Final model initialised\n'
        self.window3.labelVariable.set(show)
        show +='Final model training started\n'
        self.window3.labelVariable.set(show)
        show +='Esimated time remaining is approximately '+(str(int(1.45 * (time()-start)))) + ' seconds\n'
        self.window3.labelVariable.set(show)
        final_model.train()
        show +='Final model trained\n'
        self.window3.labelVariable.set(show)
        
        end = time()
        show +='Total time taken = ' + str(int(end-start)) + ' seconds\n'
        self.window3.labelVariable.set(show)
        show +='L2 error for the given data = ' + str(round(error, 2))+'\n'
        self.window3.labelVariable.set(show)
        
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
        self.window4.labelVariable = Tkinter.StringVar()
        label4 = Label(self.window4,textvariable=self.window4.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label4.grid(row=0,column=0,columnspan=2,sticky='EW')
        self.window4.labelVariable.set("Import the Loaded model Using 'Load Model' button")
        self.loadmodel = Button(self.window4,text="Load Model",command = self.OpenFile1)
        self.loadmodel.grid(row=1,column=0,rowspan=2, pady=5, padx=5)
        self.xdata = Button(self.window4,text="X Data",command = self.OpenFile2)
        self.xdata.grid(row=1, column=1, rowspan=2,pady=5, padx=5)
        self.output = Button(self.window4,text="Output",command = self.file_save1)
        self.output.grid(row=1, column=2, sticky='E',pady=5, padx=5)
        next = Button(self.window4,text="Next",command = Run_Model)
        next.grid(row=1, column=2, sticky='E',pady=5, padx=5)

    def Run_Model(self):
        None

if __name__ == '__main__':
    app = simpleapp_tk(None)
    app.title('Curve Fitting Tool')
    # app.geometry("200x200")
    app.mainloop()
