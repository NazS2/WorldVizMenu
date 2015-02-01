import viz
import vizact
import D3_menu
import vizshape
import vizconnect

viz.setMultiSample(4)
viz.fov(60)
viz.go()

usingPhysics = False

def test():
	print "sending a test function works :)"

vizconnect.go('./vizconnect_config_Desktop_edited.py')
rawTool = vizconnect.getRawToolDict()
rawDisplay = vizconnect.getRawDisplayDict()
rawAvatar = vizconnect.getRawAvatarDict()
menuItems = [ D3_menu.menu_item("T1",action = test),
			  D3_menu.menu_item(viz.add('basketball.osgb')),
			  D3_menu.menu_item("T3",description="thi is the bac"),
			  D3_menu.menu_item("T4",description="thi is the bac"),
			  D3_menu.menu_item("T5"),
			  D3_menu.menu_item("T6") ]

#setParent works. You need to send a smart Opject to be the parent !!
my_menu = D3_menu.menu_system(parent=rawAvatar['head_and_hand'],loc=[0.5,1.5,1], pointer = rawTool['grabber'],itemsList=menuItems,Debug=False)


#linking the hander tpo the call

vizact.onkeydown('n',my_menu.slide)
vizact.onkeydown('p',my_menu.slide,-1)
vizact.onkeydown('c',my_menu.close)
piazza = viz.addChild('piazza.osgb')
