from kriging import *
from curve_fitting_tool import *

if __name__ == '__main__':
	app = simpleapp_tk(None)
	app.title('Curve Fitting Tool')
	app.mainloop()
	filename = app.window2.labelVariable
	print filename