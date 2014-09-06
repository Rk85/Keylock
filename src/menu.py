import wx
from file_menu import FileMenu
#from edit_menu import EditMenu
#from view_menu import ViewMenu

VIEW_STATUS_BAR_ID = 30001
VIEW_FONT_ID = 30002
VIEW_ABOUT_ID = 30003
VIEW_TOOL_BAR_ID = 30004

# menu list for the textpad
MENUS = [
        {
            'name': 'File',
            'call_back_class': FileMenu,
            'frame_attribute': 'file_menu', # this is an attribute in TextPad 
            'sub_menus': [
                {
                    'id': wx.ID_NEW,
                    'help_text': 'Creats a DB file',
                    'call_back': 'new_file',
                    'display': True,
                    'name': 'New\tCtrl+N',
                    'tool_menu': True,
                    'icon_name': 'new.png'
                },
                {
                    'id': wx.ID_OPEN,
                    'help_text': 'Open a new file',
                    'call_back': 'open_file',
                    'display': True,
                    'name': 'Open\tCtrl+O',
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
                    'name': 'Save\tCtrl+S',
                    'tool_menu': True,
                    'icon_name': 'save.png'
                },
                {
                    'id': wx.ID_SAVEAS,
                    'help_text': 'Save the file under a different name',
                    'call_back': 'save_as_file',
                    'display_order' : 3,
                    'display': True,
                    'name': 'Save As\tShift+Ctrl+S'
                },
                {},
                {
                    'id': wx.ID_EXIT,
                    'help_text': 'Terminate the program',
                    'call_back': 'exit_program',
                    'display_order' : 5,
                    'display': True,
                    'name': 'Exit\tCtrl+Q'
                }
                ],
            'display_order': 1,
            'display': True
        }
]

def layout_menus(frame):
    """
        Description: Sets the list of menu/submenu items 
                     with the given frame object
        input_param: frame - frame to which menu should be attached
        input_type: frame - wx.Frame instance
        
    """
    menu_bar = wx.MenuBar()
    # traverse through the sorted list of menus
    for menu_group in sorted(
                  MENUS, key=lambda x: x['display_order']
                 ):
        # Create the menu Item and its instance 
        # and assigns the menu instance to one of the
        # Frame class(Textpad) attribute
        menu = wx.Menu()
        menu_object = menu_group['call_back_class'](frame)
        setattr(frame, menu_group['frame_attribute'], menu_object)
        create_sub_menus(menu,
                         menu_group['sub_menus']
        )
        register_menu_call_backs(frame,
                              menu.GetMenuItems(),
                              menu_group['sub_menus'],
                              menu_object
        ) 
        menu_bar.Append(menu, menu_group['name'])
    frame.SetMenuBar(menu_bar)

def create_sub_menus(menu, sub_menu_list):
    """
        Description: Creates all the required submenus under 
                     the given menu item 
        input_param: menu - Main menu to which the new sub-menus
                     need to be attached
        input_type: menu - wx.Menu Instance
        input_param: sub_menu_list - Details of the Sub Menus
                     that need to be created
        input_type: sub_menu_list - list of dictionary
        
    """
    # Traverse the submenu items and append it to main menu
    # Assign event call back funtions for each menu item 
    for sub_menu_item in sub_menu_list:
        if not sub_menu_item:
            menu.AppendSeparator()
        else:
            menu_item = wx.MenuItem(menu,
                          sub_menu_item['id'],
                          sub_menu_item['name'],
                          sub_menu_item['help_text'],
                          sub_menu_item.get('kind_type', wx.ITEM_NORMAL)
                        )
            #menu_item.SetBitmap(wx.Bitmap('exit.png'))
            menu.AppendItem(menu_item)
            if menu_item.IsCheckable():
                menu_item.Check(sub_menu_item.get('kind_value', False))

def register_menu_call_backs(frame,
                             menu_items,
                             sub_menu_details,
                             menu_object, 
                            ):
    """
        Description: Registers the Menu Call back event for  
                     each SubMenu that is created
        input_param: frame - Main Editor frame window
        input_type: frame - wx.Frame
        input_param: menu_items - list of MenuItem to which
                     event call back need to be registered
        input_type: menu_items - list of wx.MenuItem Instance
        input_param: sub_menu_list - Details of the Sub Menus
                     that is being registered for events
        input_type: sub_menu_list - list of dictionary
        input_param: menu_object - Menu class instance which is
                     having call back functions
        input_type: menu_object - Class Instance
        
    """
    for menu_item in menu_items:
        for sub_menu_detail in sub_menu_details:
            if menu_item.GetId() == sub_menu_detail.get('id'):
                frame.Bind(wx.EVT_MENU,
                        getattr(menu_object,
                              sub_menu_detail['call_back'],
                              None
                        ),
                        menu_item
                )

def layout_tool_bar(frame):
    """
        Description: Sets the Toolbar items on the UI 
                     with the given frame object
        input_param: frame - frame to which tool bar should be attached
        input_type: frame - wx.Frame instance
        
    """
    frame.tool_bar = wx.ToolBar(frame, 0, 
                         style=wx.TB_HORIZONTAL | wx.NO_BORDER| wx.TB_NODIVIDER
    )
    frame.tool_bar.Realize()
    
   
