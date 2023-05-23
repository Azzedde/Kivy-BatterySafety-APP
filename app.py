from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.behaviors import ButtonBehavior

#instanciate a database to store the battery pourcentage

class BatteryDatabase:

   def __init__(self, pourcentage=0):
       self.pourcentage = pourcentage

   def save_pourcentage(self, pourcentage):
       self.pourcentage = pourcentage

   def get_pourcentage(self):
       return self.pourcentage
   def set_pourcentage(self, pourcentage):

        self.pourcentage = pourcentage
    

   def __str__(self):
       return "Pourcentage: {}".format(self.pourcentage)




class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Set the background color
        with self.canvas.before:
            Color(0.2, 0.2, 0.9, 1)  # Set the color to a light blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50])
        
        self.add_widget(self.layout)

        # Add a title
        title_label = Label(text='Battery and Safety', font_size='24sp')
        self.layout.add_widget(title_label)

        # Add a logo
        logo = Image(source='logo.png', size_hint=(None, None), size=(200, 200))
        self.layout.add_widget(logo)

        # Add input fields
        self.username_input = TextInput(hint_text='Username', size_hint=(None, None), size=(300, 50), multiline=False)
        self.layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text='Password', size_hint=(None, None), size=(300, 50), multiline=False,
                                   password=True)
        self.layout.add_widget(self.password_input)

        # Add a login button
        login_button = Button(text='Login', size_hint=(None, None), size=(200, 50))
        login_button.bind(on_press=self.check_credentials)
        self.layout.add_widget(login_button)

        # Center the layout
        self.layout.center = self.center

    def check_credentials(self, instance):
        # Check the credentials here (e.g., compare with a database)
        username = self.username_input.text
        password = self.password_input.text
        if username == 'user' and password == 'password':
            self.manager.current = 'simple_user'
        elif username == 'admin' and password == 'password':
            self.manager.current = 'admin'

    def on_size(self, *args):
        self.rect.size = self.size
        self.layout.center = self.center


class AdminHome(Screen):
    def __init__(self, **kwargs):
        super(AdminHome, self).__init__(**kwargs)

        # Create a BoxLayout for the admin screen
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[50])

        # Add a title
        title_label = Label(text='Battery and Safety', font_size='24sp')
        layout.add_widget(title_label)

        # Create a MapView
        self.mapview = MapView(zoom=11, lat=35.6971, lon=-0.6308)   # Set initial zoom level and center coordinates
        layout.add_widget(self.mapview)

        # Create the "Add Battery Safe Station" button
        add_button = Button(text='Add Battery Safe Station', size_hint=(None, None), size=(200, 50))
        add_button.bind(on_press=self.add_marker)
        layout.add_widget(add_button)
        # Set the background color
        with self.canvas.before:
            Color(0.2, 0.2, 0.9, 1)  # Set the color to blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Add the layout to the admin screen
        self.add_widget(layout)


    def add_marker(self, instance):
        # Create and add a marker to the map view
        marker = MapMarker(lat=self.mapview.lat, lon=self.mapview.lon)
        self.mapview.add_marker(marker)
        
    def on_size(self, *args):
        self.rect.size = self.size

    



class CustomMapView(MapView, ButtonBehavior):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        return super().on_touch_up(touch)


class UserHome(Screen):


    def __init__(self,battery, **kwargs):
        super(UserHome, self).__init__(**kwargs)

        self.battery = battery

        # #Create a Navbar for the user screen that have 'set home position' and 'battery pourcentage' 
        # navbar = BoxLayout(orientation='horizontal', spacing=10, padding=[50])
        # set_home_button = Button(text='Set Home Position', size_hint=(None, None), size=(200, 50))
        # navbar.add_widget(set_home_button)
        # battery_button = Button(text='Battery Pourcentage', size_hint=(None, None), size=(200, 50))
        
        # navbar.add_widget(battery_button)
        # self.add_widget(navbar)

        # # Create a BoxLayout for the user screen
        # layout = BoxLayout(orientation='vertical', spacing=10, padding=[50])

        # # Add a title
        # title_label = Label(text='Battery and Safety', font_size='24sp')
        # layout.add_widget(title_label)
        # battery = BatteryDatabase()
        # # Create an input field for the user's to enter a pourcentage threshold of battery with placeholder text
        # self.pourcentage_input = TextInput(hint_text='Battery Pourcentage', size_hint=(None, None), size=(300, 50), multiline=False)
        # layout.add_widget(self.pourcentage_input)

        # # when saving the input value, write an announce that the input value is saved
        # save_button = Button(text='Save', size_hint=(None, None), size=(200, 50))
        # save_button.bind(on_press=lambda instance: self.save_pourcentage(instance, battery))
        # layout.add_widget(save_button)


        # # Set the background color
        # with self.canvas.before:
        #     Color(0.2, 0.2, 0.9, 1)  # Set the color to blue
        #     self.rect = Rectangle(size=self.size, pos=self.pos)

        # # Add the layout to the user screen
        # self.add_widget(layout)

        battery = BatteryDatabase()

        # Create a BoxLayout for the user home screen
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[50])

        # Create the navigation bar
        navbar = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        set_pourcentage_button = Button(text='Battery Pourcentage', size_hint=(0.5, 1))
        set_pourcentage_button.bind(on_press=self.go_to_set_pourcentage)
        navbar.add_widget(set_pourcentage_button)
        set_localization_button = Button(text='Home Localization', size_hint=(0.5, 1))
        set_localization_button.bind(on_press=self.go_to_set_localization)
        navbar.add_widget(set_localization_button)
        layout.add_widget(navbar)

        # Create a welcome message
        welcome_label = Label(text='Welcome!', font_size='24sp')
        layout.add_widget(welcome_label)

        # Create a label to display the battery percentage
        battery_label = Label(text='Battery Pourcentage: {}%'.format(battery.get_pourcentage()))
        layout.add_widget(battery_label)

        # Set the background color
        with self.canvas.before:
            Color(0.2, 0.2, 0.9, 1)  # Set the color to light gray
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # with self.canvas.before:
        #     Color(0.2, 0.2, 0.9, 1)  # Set the color to blue
        #     self.rect = Rectangle(size=self.size, pos=self.pos)

        # Add the layout to the user home screen
        self.add_widget(layout)
    def go_to_set_pourcentage(self, instance):
        self.manager.current = 'set_pourcentage'

    def go_to_set_localization(self, instance):
        self.manager.current = 'set_localization'

    def on_size(self, *args):
        self.rect.size = self.size

    def on_pos(self, *args):
        self.rect.pos = self.pos

class SetPourcentage(Screen):
    def save_pourcentage(self,battery):
        # Save the input value to the database
        battery.set_pourcentage(self.pourcentage_input.text)
        # Write an announce that the input value is saved
        self.pourcentage_input.text = 'Saved!'
        #disable the save button
        self.pourcentage_input = True


    def __init__(self, battery, **kwargs):
        super(SetPourcentage, self).__init__(**kwargs)
        self.battery = battery

        layout = BoxLayout(orientation='vertical', spacing=10, padding=[50])

        # Add a title
        title_label = Label(text='Battery and Safety', font_size='24sp')
        layout.add_widget(title_label)
        battery = BatteryDatabase()
        # Create an input field for the user's to enter a pourcentage threshold of battery with placeholder text
        self.pourcentage_input = TextInput(hint_text='Battery Pourcentage', size_hint=(None, None), size=(300, 50), multiline=False)
        layout.add_widget(self.pourcentage_input)

        # when saving the input value, write an announce that the input value is saved
        save_button = Button(text='Save', size_hint=(None, None), size=(200, 50))
        # save the input value to the database using the save_pourcentage method
        save_button.bind(on_press=lambda instance: self.save_pourcentage(battery))



        layout.add_widget(save_button)


        # Set the background color
        with self.canvas.before:
            Color(0.2, 0.2, 0.9, 1)  # Set the color to blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Add the layout to the user screen


        self.add_widget(layout)

    def on_size(self, *args):
        self.rect.size = self.size

    def on_pos(self, *args):
        self.rect.pos = self.pos

    

class SetLocalization(Screen):
    def __init__(self, **kwargs):
        super(SetLocalization, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=[50])

        # Add a title
        title_label = Label(text='Battery and Safety', font_size='24sp')
        layout.add_widget(title_label)

        #Create a MapView where the user can select his home localization or automatically get it through the GPS
        mapview = MapView(zoom=11, lat=50.6394, lon=3.057)
        layout.add_widget(mapview)

        # Create a button to get the user's localization through the GPS
        get_localization_button = Button(text='Get my localization', size_hint=(None, None), size=(200, 50))
        layout.add_widget(get_localization_button)

        # Create a button to save the user's localization


        self.add_widget(layout)
        # Set the background color
        with self.canvas.before:
            Color(0.2, 0.2, 0.9, 1)  # Set the color to blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def on_size(self, *args):
        self.rect.size = self.size

    def on_pos(self, *args):
        self.rect.pos = self.pos



class MyScreenManager(ScreenManager):
    def __init__(self,battery, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(LoginScreen(name='login'))
        self.add_widget(AdminHome(name='admin'))
        self.add_widget(UserHome(name='simple_user', battery=battery))
        self.add_widget(SetPourcentage(name='set_pourcentage', battery=battery))
        self.add_widget(SetLocalization(name='set_localization'))


class MyApp(App):
    def build(self):
        Window.size = (400, 600)
        Window.clearcolor = (1, 1, 1, 1)
        Window.set_title('Battery and Safety')
        Window.set_icon('logo.png')
        Window.size_hint = (None, None)
        battery = BatteryDatabase()
        return MyScreenManager(battery=battery)


if __name__ == '__main__':
    MyApp().run()
