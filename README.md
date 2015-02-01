World Viz 3d Menu
==================================
<h2> The aim of this repository</h2>
<p>This class is made to provide a 3d menu that is fairly customizable in term of menu items actions and behaviours.
The menu should be available in two style. one of them that follows the users avatar all the time. and the other one works like a box that is click-able so options pops up.
</p>



<h2>classes</h2>
<ul>
	<li><b>menuSystem</b>: is the main class that receives the modules & menu_itmes</li>
	<li><b>menu_item</b>: is the menu items class is used to configure each menu-items behaviour. </li>
	</ul>
	
<h2>usage</h2>
main.py is used for testing the system.
```python
menuItems = [ D3_menu.menu_item("T1",action = test),
			  D3_menu.menu_item(viz.add('basketball.osgb')),
			  D3_menu.menu_item("T3",description="thi is the bac"),
			  D3_menu.menu_item("T4",description="thi is the bac"),
			  D3_menu.menu_item("T5"),
			  D3_menu.menu_item("T6") ]

#setParent works. You need to send a smart Opject to be the parent !!
my_menu = D3_menu.menu_system(parent=rawAvatar['head_and_hand'],loc=[0.5,1.5,1], pointer = rawTool['grabber'],itemsList=menuItems,Debug=False)
```
