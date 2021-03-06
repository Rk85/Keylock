import wx
from menu import (
    create_sub_menus,
    register_menu_call_backs
)
import settings

class FolderPopUp(object):
    """
        Description: Contains details of Side/Folder Panel Information
    """
    def __init__(self, frame):
        """
            Description: Initialize the Folders Display class
            
        """
        self.frame = frame
        self.menu = wx.Menu()
        create_sub_menus(self.frame, self.menu, settings.FOLDER_POP_UP_MENU['sub_menus'])
        register_menu_call_backs(self.frame,
                                 self.menu.GetMenuItems(),
                                 settings.FOLDER_POP_UP_MENU['sub_menus'],
                                 getattr(self.frame, 
                                       settings.FOLDER_POP_UP_MENU['frame_attribute'], 
                                       None
                                     )
                                 )
        self.layout_pop_menu(init=True)
    
    def layout_pop_menu(self, init=False):
        """
            Description: Renders the Folder Pop-up menu in the screen
        """
        if not init:
            self.frame.folder_panel.folders_control.PopupMenu(self.menu)
