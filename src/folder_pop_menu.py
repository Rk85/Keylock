import wx
from menu import (
    create_sub_menus,
    register_menu_call_backs
)
import settings

POP_UP_MENU = [
    {
        'id': settings.FOLDER_ADD_ID,
        'name': '&Add Folder\tCtrl+Shift+N',
        'help_text': 'Adds New folder',
        'display': True,
        'call_back': 'add_new_folder',
        'tool_menu': True,
        'icon_name': 'add_folder.png'
        },
    {
        },
    {
        'id': settings.FOLDER_DELETE_ID,
        'name': '&Delete Folder\tCtrl+Shift+D',
        'help_text': 'Deletes folder',
        'display': True,
        'call_back': 'delete_folder',
        'tool_menu': True,
        'icon_name': 'delete_folder.png'
        },
    {
        'id': settings.FOLDER_ADD_ITEM_ID,
        'name': '&New Item\tCtrl+T',
        'help_text': 'New Item',
        'display': True,
        'call_back': 'add_new_item',
        'tool_menu': True,
        'icon_name': 'add_item.png'
        }
    ]

class FolderPopUp(object):
    """
        Description: Contains details of Side/Folder Panel Information
    """
    def __init__(self, frame, parent):
        """
            Description: Initialize the Folders Display class
            
        """
        self.frame = frame
        self.parent = parent
        self.menu = None

    def layout_pop_menu(self):
        """
            Description: Renders the Folder Pop-up menu in the screen
        """
        if self.menu:
            self.menu.Destroy()
        self.menu = wx.Menu()
        create_sub_menus(self.frame, self.menu, POP_UP_MENU)
        register_menu_call_backs(self.frame,
                                 self.menu.GetMenuItems(),
                                 POP_UP_MENU,
                                 self.parent
                                 )
        self.parent.folders_control.PopupMenu(self.menu)
