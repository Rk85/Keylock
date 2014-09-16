import wx
from menu import (
    create_sub_menus,
    register_menu_call_backs
)
import settings

class ListItemPopUp(object):
    """
        Description: Contains details of Item PopUp Menu Details
    """
    def __init__(self, frame):
        """
            Description: Initialize the Folders Display class
            
        """
        self.frame = frame
        self.menu = None
        self.layout_pop_menu(init=True)
    
    def layout_pop_menu(self, init=False):
        """
            Description: Renders the Item Pop-up menu in the screen
        """
        if self.menu:
            self.menu.Destroy()
        self.menu = wx.Menu()
        create_sub_menus(self.frame, self.menu, settings.ITEM_POP_UP_MENU[0]['sub_menus'])
        register_menu_call_backs(self.frame,
                                 self.menu.GetMenuItems(),
                                 settings.ITEM_POP_UP_MENU[0]['sub_menus'],
                                 getattr(self.frame, 
                                       settings.ITEM_POP_UP_MENU[0]['frame_attribute'], 
                                       None
                                     )
                                 )
        if not init:
            self.frame.item_panel.list_control.PopupMenu(self.menu)
