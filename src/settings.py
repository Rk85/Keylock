import wx
from file_menu import FileMenu

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
VIEW_FONT_ID = 30002
VIEW_ABOUT_ID = 30003
VIEW_TOOL_BAR_ID = 30004

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
        }
]

FOLDER_POP_UP_MENU = [
    {
        'name': 'Folder Pop-Up',
        'frame_attribute': 'folder_panel', # this is an attribute in Keylock Class
        'display_order': 2,
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
            {},
            {
                'id': FOLDER_DELETE_ID,
                'name': '&Delete Folder\tCtrl+Shift+D',
                'help_text': 'Deletes folder',
                'display': True,
                'call_back': 'delete_folder',
                'tool_menu': True,
                'icon_name': 'delete_folder.png'
            },
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
]

ITEM_POP_UP_MENU = [
    {
        'name': 'Item Pop-Up',
        'frame_attribute': 'folder_panel', # this is an attribute in Keylock Class
        'display_order': 3,
        'display': True,
        'sub_menus':[
            {
                'id': ITEM_COPY_USER,
                'name': '&Copy User Name\tCtrl+U',
                'help_text': 'Copies User name into sytem buffer',
                'display': True,
                'call_back': 'copy_item',
                'tool_menu': True,
                'icon_name': 'copy_user.png'
                },
            {
                'id': ITEM_COPY_PASS,
                'name': '&Copy Password\tCtrl+P',
                'help_text': 'Copies Password into sytem buffer',
                'display': True,
                'call_back': 'copy_item',
                'tool_menu': True,
                'icon_name': 'copy_pass.png'
            },
            {},
            {
                'id': ITEM_EDIT_ID,
                'name': '&Edit Item\tCtrl+E',
                'help_text': 'Edits Current Item',
                'display': True,
                'call_back': 'edit_item',
                'tool_menu': True,
                'icon_name': 'edit_pass.png'
            },
            {
                'id': ITEM_DELETE_ID,
                'name': '&Delete Item\tCtrl+D',
                'help_text': 'Delete Current Item',
                'display': True,
                'call_back': 'delete_item',
                'tool_menu': True,
                'icon_name': 'delete_pass.png'
            }
        ]
    }
]
