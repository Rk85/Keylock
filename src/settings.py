import wx
from file_menu import FileMenu
from view_menu import ViewMenu

# Folder POP-UP Menu Ids
FOLDER_ADD_ID = 14001
FOLDER_DELETE_ID = 14002
FOLDER_ADD_ITEM_ID = 14003

# Item POP-UP Menu Ids
ITEM_EDIT_ID = 15001
ITEM_DELETE_ID = 15002
ITEM_COPY_USER = 15003
ITEM_COPY_PASS = 15004

VIEW_STATUS_BAR_ID = 30001
VIEW_TOOL_BAR_ID = 30002
VIEW_USER_HIDE = 30003
VIEW_PASS_HIDE = 30004
VIEW_ABOUT_ID = 30005

FOLDER_POP_UP_MENU = {
        'name': 'Folder Pop-Up',
        'frame_attribute': 'folder_panel', # this is an attribute in Keylock Class attribute
        'display_order': 11,
        'display': True,
        'sub_menus': [
            {
                'id': FOLDER_ADD_ID,
                'name': '&Add Folder\tCtrl+Shift+N',
                'help_text': 'Adds New folder',
                'display': True,
                'call_back': 'add_new_folder',
                'tool_menu': True,
                'icon_name': 'add_folder.png'
            },
            {
                'id': FOLDER_DELETE_ID,
                'name': '&Delete Folder\tCtrl+Shift+D',
                'help_text': 'Deletes folder',
                'display': True,
                'call_back': 'delete_folder',
                'tool_menu': True,
                'icon_name': 'delete_folder.png'
            },
            {},
            {
                'id': FOLDER_ADD_ITEM_ID,
                'name': '&New Item\tCtrl+T',
                'help_text': 'New Item',
                'display': True,
                'call_back': 'add_new_item',
                'tool_menu': True,
                'icon_name': 'add_item.png'
            }
        ]
}


ITEM_POP_UP_MENU = {
        'name': 'Item Pop-Up',
        'frame_attribute': 'item_panel', # this is an attribute in Keylock Class
        'display_order': 12,
        'display': True,
        'sub_menus':[
            {
                'id': ITEM_EDIT_ID,
                'name': '&Edit Item\tCtrl+E',
                'help_text': 'Edits Current Item',
                'display': True,
                'enable': False,
                'call_back': 'edit_item',
                'tool_menu': True,
                'icon_name': 'edit_pass.png'
            },
            {
                'id': ITEM_DELETE_ID,
                'name': '&Delete Item\tCtrl+D',
                'help_text': 'Delete Current Item',
                'display': True,
                'enable': False,
                'call_back': 'delete_item',
                'tool_menu': True,
                'icon_name': 'delete_pass.png'
            },
            {},
            {
                'id': ITEM_COPY_USER,
                'name': '&Copy User Name\tCtrl+U',
                'help_text': 'Copies User name into sytem buffer',
                'display': True,
                'enable': False,
                'call_back': 'copy_item',
                'tool_menu': True,
                'icon_name': 'copy_user.png'
                },
            {
                'id': ITEM_COPY_PASS,
                'name': '&Copy Password\tCtrl+P',
                'help_text': 'Copies Password into sytem buffer',
                'display': True,
                'enable': False,
                'call_back': 'copy_item',
                'tool_menu': True,
                'icon_name': 'copy_pass.png'
            }
        ]
}

# menu list for the application
MENUS = [
        {
            'name': 'File',
            'call_back_class': FileMenu,
            'frame_attribute': 'file_menu', # this is an attribute in Keylock Class 
            'sub_menus': [
                {
                    'id': wx.ID_NEW,
                    'help_text': 'Creats a DB file',
                    'call_back': 'new_file',
                    'display': True,
                    'name': '&New\tCtrl+N',
                    'tool_menu': True,
                    'icon_name': 'new_file.png'
                },
                {
                    'id': wx.ID_OPEN,
                    'help_text': 'Open a new file',
                    'call_back': 'open_file',
                    'display': True,
                    'name': '&Open\tCtrl+O',
                    'tool_menu': True,
                    'icon_name': 'open.png'
                },
                {},
                {
                    'id': wx.ID_SAVE,
                    'help_text': 'Save the current file',
                    'call_back': 'save_file',
                    'display_order' : 2,
                    'display': True,
                    'name': '&Save\tCtrl+S',
                    'tool_menu': True,
                    'icon_name': 'save.png'
                },
                {
                    'id': wx.ID_SAVEAS,
                    'help_text': 'Save the file under a different name',
                    'call_back': 'save_as_file',
                    'display_order' : 3,
                    'display': True,
                    'name': '&Save As\tShift+Ctrl+S',
                    'icon_name': 'save_as.png'
                },
                {},
                {
                    'id': wx.ID_EXIT,
                    'help_text': 'Terminate the program',
                    'call_back': 'exit_program',
                    'display_order' : 5,
                    'display': True,
                    'name': '&Exit\tCtrl+Q',
                    'icon_name': 'exit.png'
                    
                }
                ],
            'display_order': 1,
            'display': True
        },
        {
            'name': 'Edit',
            'sub_menus': FOLDER_POP_UP_MENU['sub_menus'] + ITEM_POP_UP_MENU['sub_menus'],
            'display_order': 2,
            'display': True
        },
        {
            'name': 'View',
            'call_back_class': ViewMenu,
            'frame_attribute': 'view_menu',
            'sub_menus': [
                {
                    'id': VIEW_STATUS_BAR_ID,
                    'help_text': 'Shows/Hides the Status Bar in the editor',
                    'call_back': 'view_status_bar',
                    'display': True,
                    'name': 'Show Status Bar',
                    'kind_type': wx.ITEM_CHECK,
                    'kind_value': True
                },
                {
                    'id': VIEW_TOOL_BAR_ID,
                    'help_text': 'Shows/Hides the Tool Bar in the editor',
                    'call_back': 'view_tool_bar',
                    'display': True,
                    'name': 'Show Tool Bar',
                    'kind_type': wx.ITEM_CHECK,
                    'kind_value': True
                },
                {},
                {
                    'id': VIEW_USER_HIDE,
                    'help_text': 'Shows the user name as *** instead of actual name',
                    'call_back': 'hide_user_name',
                    'display': True,
                    'name': 'Show User Name As ***',
                    'kind_type': wx.ITEM_CHECK,
                    'kind_value': True
                },
                {
                    'id': VIEW_PASS_HIDE,
                    'help_text': 'Shows the password name as *** instead of actual name',
                    'call_back': 'hide_password',
                    'display': True,
                    'name': 'Show Password Name As ***',
                    'kind_type': wx.ITEM_CHECK,
                    'kind_value': True
                },  
                {},
                {
                    'id': VIEW_ABOUT_ID,
                    'help_text': 'shows About Window',
                    'call_back': 'view_about_info',
                    'display': True,
                    'name': 'About'
                }
            ],
            'display_order': 3,
            'display': True
      }
]
