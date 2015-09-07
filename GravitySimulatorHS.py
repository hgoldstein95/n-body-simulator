## Harry Goldstein and Shalin Patel
## Customizable Gravitation Model
## Provdes tools on-the-fly setup of
## gravitating systems.

# Requires vPython

from visual import *
from visual.controls import *
import wx
import os
import nbody2

planet_list = []
loaded_planet_list = []

mass = 6.0E27
radius = 1.0E9
position = vector(0,0,0)
velocity = vector(0,0,0)
c = [1,0,0]

def getColor (col):
	"""
	Returns an appropriate color tuple based on a given string
	"""
	if col == 'Red':
		return color.red
	elif col == 'Blue':
		return color.blue
	elif col == 'Green':
		return color.green
	elif col == 'Cyan':
		return color.cyan
	elif col == 'Yellow':
		return color.yellow
	elif col == 'Magenta':
		return color.magenta
	elif col == 'Orange':
		return color.orange
	elif col == 'White':
		return color.white
	else:
		return color.black
		
def is_num (s):
	"""
	Returns True if input can be casted to float
	"""
	try:
		float(s)
		return True
	except ValueError:
		return False

class Wrapper(wx.Frame):
	def __init__ (self, parent, title):
		wx.Frame.__init__(self,parent,title=title,size=(600,400))
		
		# Setting up the menu.
		filemenu= wx.Menu()
		
		# Add about and save buttons
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		filemenu.AppendSeparator()
		menuSave = filemenu.Append(wx.ID_SAVE,"S&ave"," Save current configuration")
		menuLoad = filemenu.Append(wx.ID_OPEN,"L&oad"," Load saved configuration")
		
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
		self.Show(True)
		
		self.Bind(wx.EVT_MENU, self.onSave, menuSave)
		self.Bind(wx.EVT_MENU, self.onLoad, menuLoad)
		self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
		
	def onAbout (self, e):
		os.system('notepad.exe readme.txt')
	
	def onSave (self, e):
		dlg = wx.TextEntryDialog(self, "File Name:", "Save", "", wx.OK)
		dlg.SetValue('save')
		if dlg.ShowModal() == wx.ID_OK:
			name = dlg.GetValue()
			dlg.Destroy()
		nbody2.saveState(planet_list, name)
		
	def onLoad (self, e):
		""" Open a file"""
		dlg = wx.FileDialog(self, "Choose a file", os.getcwd() + "\\saves\\", "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
		dlg.Destroy()
		loaded_planet_list = nbody2.createList(os.getcwd() + '\\saves\\' + self.filename)
		for p in loaded_planet_list:
			planet_list.append(nbody2.makePlanet(vector(p[0],p[1],p[2]), p[3], (p[4],p[5],p[6]), vector(p[7],p[8],p[9]), p[10]))

class Controls(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
	
		# Sizer setup
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		grid = wx.GridBagSizer(hgap=5, vgap=5)
		hSizer = wx.BoxSizer(wx.VERTICAL)
		
		# Text display
		self.logger = wx.TextCtrl(self, size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)
	
		# Radius field
		self.radlbl = wx.StaticText(self, label="Radius of planet, suggested ~E9:")
		self.radedit = wx.TextCtrl(self, size=(95, -1))
		self.radedit.SetValue('1.0E9')
		grid.Add(self.radlbl, pos=(0,0))
		grid.Add(self.radedit, pos=(0,1))
		self.Bind(wx.EVT_TEXT, self.radEvent, self.radedit)
	
		# Mass field
		self.masslbl = wx.StaticText(self, label="Mass of planet, suggested ~E27:")
		self.massedit = wx.TextCtrl(self, size=(95, -1))
		self.massedit.SetValue('6.0E27')
		grid.Add(self.masslbl, pos=(1,0))
		grid.Add(self.massedit, pos=(1,1))
		self.Bind(wx.EVT_TEXT, self.massEvent, self.massedit)
		
		# Position fields
		self.poslbl = wx.StaticText(self, label="Position of planet (x,y,z), suggested ~E10:")
		self.poseditx = wx.TextCtrl(self, size=(95, -1))
		self.posedity = wx.TextCtrl(self, size=(95, -1))
		self.poseditz = wx.TextCtrl(self, size=(95, -1))
		self.poseditx.SetValue('0')
		self.posedity.SetValue('0')
		self.poseditz.SetValue('0')
		grid.Add(self.poslbl, pos=(2,0))
		grid.Add(self.poseditx, pos=(2,1))
		grid.Add(self.posedity, pos=(2,2))
		grid.Add(self.poseditz, pos=(2,3))
		self.Bind(wx.EVT_TEXT, self.posxEvent, self.poseditx)
		self.Bind(wx.EVT_TEXT, self.posyEvent, self.posedity)
		self.Bind(wx.EVT_TEXT, self.poszEvent, self.poseditz)
		
		# Velocity fields
		self.vellbl = wx.StaticText(self, label="Velocity of planet (x,y,z), suggested ~E3:")
		self.veleditx = wx.TextCtrl(self, size=(95, -1))
		self.veledity = wx.TextCtrl(self, size=(95, -1))
		self.veleditz = wx.TextCtrl(self, size=(95, -1))
		self.veleditx.SetValue('0')
		self.veledity.SetValue('0')
		self.veleditz.SetValue('0')
		grid.Add(self.vellbl, pos=(3,0))
		grid.Add(self.veleditx, pos=(3,1))
		grid.Add(self.veledity, pos=(3,2))
		grid.Add(self.veleditz, pos=(3,3))
		self.Bind(wx.EVT_TEXT, self.velxEvent, self.veleditx)
		self.Bind(wx.EVT_TEXT, self.velyEvent, self.veledity)
		self.Bind(wx.EVT_TEXT, self.velzEvent, self.veleditz)
		
		# Color dropdown
		self.colorList = ['Red', 'Blue', 'Green', 'Cyan', 'Yellow', 'Magenta', 'Orange', 'White' , 'Black']
		self.colorlbl = wx.StaticText(self, label="Color of planet:")
		self.coloredit = wx.ComboBox(self, size=(95, -1), choices=self.colorList, style=wx.CB_DROPDOWN)
		self.coloredit.SetValue('Red')
		grid.Add(self.colorlbl, pos=(4,0))
		grid.Add(self.coloredit, pos=(4,1))
		self.Bind(wx.EVT_COMBOBOX, self.colorEvent, self.coloredit)
		
		# Buttons
		self.button =wx.Button(self, label="Run")
		self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
		grid.Add(self.button, pos=(6,2))
		
		self.button2 =wx.Button(self, label="Exit")
		self.Bind(wx.EVT_BUTTON, self.OnClick2,self.button2)
		grid.Add(self.button2,  pos=(6,3))
		
		self.button3 =wx.Button(self, label="Add Planet")
		self.Bind(wx.EVT_BUTTON, self.OnClick3,self.button3)
		grid.Add(self.button3,  pos=(6,0))
		
		self.button4 =wx.Button(self, label="Undo")
		self.Bind(wx.EVT_BUTTON, self.OnClick4,self.button4)
		grid.Add(self.button4,  pos=(6,1))
				
		# Sizing
		hSizer.Add(grid, 0, wx.ALL, 5)
		mainSizer.Add(hSizer, 0, wx.ALL, 5)
		mainSizer.Add(self.logger, wx.RIGHT)
		self.SetSizerAndFit(mainSizer)
	
	# Events
	def OnClick (self, e):
		self.logger.AppendText('Animating\n')
		dlg = wx.TextEntryDialog(self, "Timestep:", "Speed", "", wx.OK)
		dlg.SetValue('8.64E3')
		if dlg.ShowModal() == wx.ID_OK:
			dt = float(dlg.GetValue())
			dlg.Destroy()
		nbody2.animate(planet_list, dt)
	def OnClick2 (self, e):
		os._exit(0)
	def OnClick3 (self, e):
		present = False
		for p in planet_list:
			if position == p.pos:
				present = True
				break
		if not present:
			pnew = vector(position.x, position.y, position.z)
			rnew = float(radius)
			cnew = (c[0], c[1], c[2])
			vnew = vector(velocity.x, velocity.y, velocity.z)
			mnew = float(mass)
			planet_list.append(nbody2.makePlanet(pnew, rnew, cnew, vnew, mnew))
			self.logger.AppendText('Planet Added Successfully:\n')
			self.logger.AppendText('Radius: ' + str(radius) + '\n')
			self.logger.AppendText('Mass: ' + str(mass) + '\n')
			self.logger.AppendText('Position: ' + str(position) + '\n')
			self.logger.AppendText('Velocity: ' + str(velocity) + '\n')
			self.logger.AppendText('\n')
		else:
			self.logger.AppendText('Failed to Add Planet\n')
			dlg = wx.MessageDialog( self,"You cannot put two planets at the same position.","Error",  wx.OK)
			dlg.ShowModal() # Show it
			dlg.Destroy()
	def OnClick4 (self, e):
		if len(planet_list) > 0:
			p = planet_list.pop()
			p.visible = False
			p.trail_object.visible = False
			del p
			self.logger.AppendText('Undone\n')
	def radEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			radius = float(input)
	def massEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			mass = float(input)
	def posxEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			position.x = float(input)
	def posyEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			position.y = float(input)
	def poszEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			position.z = float(input)
	def velxEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			velocity.x = float(input)
	def velyEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			velocity.y = float(input)
	def velzEvent (self, e):
		input = e.GetString()
		if (is_num(input)):
			velocity.z = float(input)
	def colorEvent (self, e):
		col = e.GetString()
		temp = getColor(col)
		c[0] = temp[0]
		c[1] = temp[1]
		c[2] = temp[2]
		
app = wx.App(False)
frame = Wrapper(None,'Gravity Simulator')
panel = Controls(frame)
frame.Show()
app.MainLoop()