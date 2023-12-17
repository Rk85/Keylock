import wx
import os
import settings
import random

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
                  settings.MENUS, key=lambda x: x['display_order']
                 ):
        # Create the menu Item and its instance 
        # and assigns the menu instance to one of the
        # Frame class(Textpad) attribute
        menu = wx.Menu()
        create_sub_menus(frame,
                         menu,
                         menu_group['sub_menus']
        )
        if menu_group.get('call_back_class'):
            menu_object = menu_group['call_back_class'](frame)
            setattr(frame, menu_group['frame_attribute'], menu_object)
            register_menu_call_backs(frame,
                              menu.GetMenuItems(),
                              menu_group['sub_menus'],
                              menu_object
            ) 
        menu_bar.Append(menu, menu_group['name'])
    frame.SetMenuBar(menu_bar)

def create_sub_menus(frame,
                     menu,
                     sub_menu_list):
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
    for index, sub_menu_item in enumerate(sub_menu_list):
        if not sub_menu_item:
            menu.AppendSeparator()
        else:
            #sub_menu_item['id'] = index + random.randint(0, 32765)
            menu_item = wx.MenuItem(menu,
                          sub_menu_item['id'],
                          sub_menu_item['name'],
                          sub_menu_item['help_text'],
                          sub_menu_item.get('kind_type', wx.ITEM_NORMAL)
                        )
            if sub_menu_item.get('icon_name'):
                menu_item.SetBitmap(wx.Image(
                                os.path.join(frame.icon_dir, sub_menu_item['icon_name']),
                                wx.BITMAP_TYPE_PNG
                                ).ConvertToBitmap())
            menu.AppendItem(menu_item)
            if menu_item.IsCheckable():
                menu_item.Check(sub_menu_item.get('kind_value', False))
            menu_item.Enable(sub_menu_item.get('enable', True))

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
    frame.tool_bar = frame.CreateToolBar()
    tool_bar_menus = [settings.MENUS[0]] + [
                     settings.FOLDER_POP_UP_MENU] + [
                     settings.ITEM_POP_UP_MENU]
    for menu_group in sorted(
                  tool_bar_menus, key=lambda x: x['display_order']
                 ):
        handler_instance = getattr(frame, 
                                   menu_group['frame_attribute'], 
                                   None
                           )
        if handler_instance:
            for sub_menu in menu_group.get('sub_menus', []):
                if sub_menu.get('tool_menu'):
                    frame.tool_bar.AddSimpleTool(sub_menu['id'],
                                       wx.Bitmap(frame.icon_dir + sub_menu['icon_name'], 
                                                   wx.BITMAP_TYPE_PNG),
                                                 sub_menu['name'],)
                    frame.Bind(wx.EVT_TOOL, 
                               getattr(handler_instance, 
                                        sub_menu['call_back'], 
                                        None),
                               id=sub_menu['id'])
        frame.tool_bar.AddSeparator()
    for sub_menu in settings.ITEM_POP_UP_MENU['sub_menus']:
        if sub_menu:
            frame.tool_bar.EnableTool(sub_menu['id'], False)
    frame.tool_bar.Realize()
    
   
