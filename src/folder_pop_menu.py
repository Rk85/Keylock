import wx
from menu import (
    create_sub_menus,
    register_menu_call_backs
)

FOLDER_ADD_ID = 14001
FOLDER_DELETE_ID = 14002
FOLDER_ADD_ITEM_ID = 14003

POP_UP_MENU = [
    {
        'id': FOLDER_ADD_ID,
        'name': 'Add Folder',
        'help_text': 'Adds New folder',
        'display': True,
        'call_back': 'add_new_folder'
        },
    {
        },
    {
        'id': FOLDER_DELETE_ID,
        'name': 'Delete Folder',
        'help_text': 'Deletes folder',
        'display': True,
        'call_back': 'delete_folder'
        },
    {
        'id': FOLDER_ADD_ITEM_ID,
        'name': 'New Item',
        'help_text': 'New Item',
        'display': True,
        'call_back': 'add_new_item'
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
