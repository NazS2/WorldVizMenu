import viz
import vizact
import vizshape
from threading import Timer #used to force deley on the grap item handeler
from tools import grabber

def sayClicked():
	print ("--> sayClicked was called ;)");

class GrabHandler(viz.EventClass):
	"""
	Class to handle events for grabbing, holds a reference to the objects with on grab functions
	"""
	def __init__(self, onGrabbed=None, onReleased=None, onIntersection=None):
		viz.EventClass.__init__(self)
		if onGrabbed:
			self.callback(grabber.GRAB_EVENT, onGrabbed)
		if onReleased:
			self.callback(grabber.RELEASE_EVENT, onReleased)
		if onIntersection:
			self.callback(grabber.UPDATE_INTERSECTION_EVENT, onIntersection)

class menu_system:
	"""a simple menu system class"""

	def __init__(self,loc=[0.5,-0.5,1],parent=None,pointer=None,itemsList=None,openModel='basketball.osgb',onScreen=False,Debug=False):
		"""the constructor"""
		self.isOpen = False
		self.lastCloseTick = 0
		self.lastOpenTick = 0
		self.notRepeted = True
		self.focusedItem = 0
		self.itemList = []
		self.Debug = Debug
		
		self.audio = {}
		self.audio['open']  = viz.addAudio('art/sound/open.wav')
		self.audio['click'] = viz.addAudio('art/sound/click.wav')
		self.audio['error'] = viz.addAudio('art/sound/error.wav')
		self.audio['slide'] = viz.addAudio('art/sound/slide.wav')
		self.audio['close'] = viz.addAudio('art/sound/close.wav')
		
		if  itemsList == None:
			self.entries = []		# list of menu items
		else:
			self.entries = itemsList
		
		self.slider = vizshape.addQuad(size=(1,0.5),axis=-vizshape.AXIS_Z,cullFace=False,  cornerRadius=0.0)
		self.slider.alpha(0.5)
		self.descriptionText = viz.addText3D("",pos=[0,0.1,-0.3],color=[0.3,0.3,0.3],parent = self.slider,scale=[0.05,0.05,0.05],align=viz.ALIGN_CENTER_BOTTOM)
			
		self.arage()
		#the OpenModel is the one to open the menu
		if isinstance(openModel, basestring):
			self.menuOpenOpject = viz.add(openModel);
		else:
			self.menuOpenOpject = openModel;
		
		#in case its linked to the head for example..
		if not (parent == None):
			self.menuOpenOpject.setParent(parent)
			self.slider.setPosition([0,1.5,1])
			self.slider.setParent(parent)
		
		self.menuOpenOpject.setPosition(loc)
		
		self._grabHandler = GrabHandler(onGrabbed=self.onGrabbed,onIntersection=self.onIntersection)
		self._grabHandler.setEnabled(True)
		
		if not (pointer == None):
			self.graber = pointer# list of menu items
			self.graber.setItems([self.menuOpenOpject])
			self.graber.setUpdateFunction(self.updateGrabber)
		
	
	def add_entry(self, key, Desciption=None, pos=None, sub=None):
		return True	# happy

	# update code for grabber
	def updateGrabber(self,tool):
		state = viz.mouse.getState()
		if state & viz.MOUSEBUTTON_LEFT:
			tool.grab();
			#tool.grabAndHold() # create a link..

	def show(self):
		"""runs the menu system, returns selected letter"""
		
	def open(self):
		"""runs the menu system, returns selected letter"""
		if self.Debug: print ("__code for opening the menu__")
		print viz.tick(), " ", self.lastCloseTick+1 , " ", self.lastCloseTick+1 < viz.tick()
		self.graber.removeItems([self.menuOpenOpject]) ## removing the Oppning object !!
		self.itemList = []
		for item in self.entries: self.itemList.append(item.model),item.model.visible(True)
		self.graber.setItems(self.itemList)
		self.audio['open'].play()
		self.lastOpenTick = viz.tick();
		
	def close(self):
		if self.isOpen and self.lastOpenTick+1 < viz.tick() :
			self.lastCloseTick = viz.tick()
			for item in self.entries: self.itemList.append(item.model),item.model.visible(False)
			self.graber.setItems([self.menuOpenOpject])
			self.descriptionText.visible(False)
			self.audio['close'].play()
			self.isOpen = False
		"""ment to close the opened menu"""
		
	def arage(self):
		i = self.focusedItem*-1
		for item in self.entries:
			item.model.setParent(self.slider)
			item.model.setPosition([i/2.0,0,-0.1])
			i=i+1		
		
	def slide(self,amount=1):
		"""ment to slide through the items the opened menu"""
		if self.isOpen:
			if self.Debug: print amount, "f: ",self.focusedItem
			try:
				self.focusedItem = (self.focusedItem+amount)%len(self.entries)
				self.audio['slide'].play()
				self.arage()
			except TypeError:
				print "an intiger is expected in the amount"
			
	def onGrabbed(self, e):
		# this is the function that is been called when ever an Object id been clicked on aka " Grabbed "
		# it will be divided into checking a ( its the Opining object { inventory box } ) or b (one of the menu itmes)
		if e.grabbed == self.menuOpenOpject and ( self.lastCloseTick+1 < viz.tick() and not(self.isOpen)):
			self.isOpen = True
			self.open()
		elif e.grabbed in self.itemList and self.notRepeted:
			self.notRepeted = False
			Timer(0.1, self._clearItemMenu).start() 
			index = self.itemList.index(e.grabbed)
			self.entries[index].action()
			self.audio['click'].play()
			if self.entries[index].data.cau:
				self.close()
		e.grabber.release()
						
	def onIntersection(self, e):
		#similer to hover in the html prespective
		if self.isOpen and e.new in self.itemList:
			index = self.itemList.index(e.new)
			self.entries[index].intersection()
			
			self.descriptionText.message(self.entries[index].data.description)
			self.descriptionText.visible(True)
			
			
		if self.isOpen and e.old in self.itemList:
			index = self.itemList.index(e.old)
			self.descriptionText.visible(False)
			self.entries[index].afterIntersection()
			
	def onReleased(self, e):
		print e.grabbed,self.menuOpenOpject

	def _clearItemMenu(self):
		self.notRepeted = True
		
class menu_item:
	
	def __init__(self, model, description = "" , action=None,intersection=None,afterIntersection=None,subMenu=None,scale= [0.2,0.2,0.2], closeAfterUse = True ):
		self.data = viz.Data(
				#name=name,
				action=action,
				description=description,
				cau=closeAfterUse)
		
		if isinstance(model, basestring):
			self.model =  viz.addText3D(model,pos=[0,0,0],align=viz.ALIGN_CENTER_BOTTOM)
			self.model.setScale(scale)
		else:
			self.model =  model
				
		self.action 			= self.defultAction 			if action 			 == None else action
		self.intersection 		= self.defultIntersection		if intersection 	 == None else intersection
		self.afterIntersection 	= self.defultAfterIntersection	if afterIntersection == None else afterIntersection
		
		self.visible(False)

	def visible (self,value):
		self.model.visible(value)
		
	def defultAction (self):
		print "testing still... ?"
		
	def defultIntersection (self):
		self.model.addAction(vizact.spin(0,1,0,90))
		
	def defultAfterIntersection (self):
		self.model.setEuler([0,0,0])
		self.model.clearActions()
		