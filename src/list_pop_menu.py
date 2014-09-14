import wx
from menu import (
    create_sub_menus,
    register_menu_call_backs
)
import settings

POP_UP_MENU = [
    {
        'id': settings.ITEM_COPY_USER,
        'name': '&Copy User Name\tCtrl+U',
        'help_text': 'Copies User name into sytem buffer',
        'display': True,
        'call_back': 'copy_item',
        'tool_menu': True,
        'icon_name': 'copy_user.png'
        },
    {
        'id': settings.ITEM_COPY_PASS,
        'name': '&Copy Password\tCtrl+P',
        'help_text': 'Copies Password into sytem buffer',
        'display': True,
        'call_back': 'copy_item',
        'tool_menu': True,
        'icon_name': 'copy_pass.png'
        },
    {
        },
    {
        'id': settings.ITEM_EDIT_ID,
        'name': '&Edit Item\tCtrl+E',
        'help_text': 'Edits Current Item',
        'display': True,
        'call_back': 'edit_item',
        'tool_menu': True,
        'icon_name': 'edit_pass.png'
        },
    {
        'id': settings.ITEM_DELETE_ID,
        'name': '&Delete Item\tCtrl+D',
        'help_text': 'Delete Current Item',
        'display': True,
        'call_back': 'delete_item',
        'tool_menu': True,
        'icon_name': 'delete_pass.png'
        }
    ]

class ListItemPopUp(object):
    """
        Description: Contains details of Item PopUp Menu Details
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
            Description: Renders the Item Pop-up menu in the screen
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
        self.parent.list_control.PopupMenu(self.menu)
