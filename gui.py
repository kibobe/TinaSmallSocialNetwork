from network import Network 
from kivy.app import App
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.adapters.dictadapter import ListAdapter
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.logger import Logger
from random import randint


class MainView(GridLayout):
    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(MainView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.network = Network()
        listUser = self.network.getAllUsers()
	
	
        self.myListAdapter = ListAdapter(data=[str(listUser[i]) for i in range(len(listUser))], 
					cls=ListItemButton, 
					selection_mode='single', 
					sorted_keys=[])
        self.myListAdapter.bind(on_selection_change=self.selectionChange)
        myListView = ListView(adapter=self.myListAdapter)
        
        self.add_widget(myListView)
      
	self.layout = BoxLayout(orientation='vertical')
	lbl = Label(text = 'SELECT USER FROM LIST')
	
	btn1 = Button(text='Friends', background_color = (0.988, 0.53, 0.70, 1.0))
	btn1.bind(on_press=self.clickFriends)
	
	btn2 = Button(text='Friends of friends', background_color = (0.988, 0.53, 0.70, 1.0))
	btn2.bind(on_press=self.clickFriendsOfFriends)
	
	btn3 = Button(text='Suggested friend', background_color = (0.988, 0.53, 0.70, 1.0))
	btn3.bind(on_press=self.clickSuggestedFriends)
	
	self.layout.add_widget(lbl)
	self.layout.add_widget(btn1)
	self.layout.add_widget(btn2)
	self.layout.add_widget(btn3)
	
	people = ""
  
	self.add_widget(self.layout)

    
    def selectionChange(self, adapter, *args):
        if (adapter.selection):
	    self.layout.disabled = False
	    self.people = str(adapter.selection[0].text)
	
    def clickFriends(self, adapter):
	
	listUser1 = self.network.getFriends(self.people)
	lvAdapter = SimpleListAdapter(data=[str(listUser1[i]) for i in range(len(listUser1))],cls=Label)
        lv = ListView(adapter=lvAdapter)
	
	myTitle = str(self.people)
	myTitle += "\nFriends: ";
	
	popup = Popup(title=myTitle, content=lv, size_hint = (None, None), size=(400,400))
	popup.open()


    def clickFriendsOfFriends(self, adapter):

	listUser1 = self.network.getFriendOfFriends(self.people)
	lvAdapter = SimpleListAdapter(data=[str(listUser1[i]) for i in range(len(listUser1))],cls=Label)
        lv = ListView(adapter=lvAdapter)
        
        
	myTitle = str(self.people)
	myTitle += "\nFriends of Friends: ";
	
	popup = Popup(title=myTitle, content=lv, size_hint = (None, None), size=(400,400))
	popup.open()

    def clickSuggestedFriends(self, adapter):
	
	listUser1 = self.network.getSuggestedFriend(self.people)
	lvAdapter = SimpleListAdapter(data=[str(listUser1[i]) for i in range(len(listUser1))],cls=Label)
        lv = ListView(adapter=lvAdapter)
	
	myTitle = str(self.people)
	myTitle += "\nSuggested Friends: ";
	
	popup = Popup(title=myTitle, content=lv, size_hint = (None, None), size=(400,400))
	popup.open()


class MyApp(App):
    def build(self):
	return = MainView()
      

if __name__ == '__main__':
    MyApp().run()
	
