import wx

class Folders(object):
    """
        Description: Contains details of Side/Folder Panel Information
    """
    def __init__(self, frame):
        """
            Description: Initialize the Folders Display class
            
        """
        self.frame = frame
        self.icon_name = 'folder.png'
        self.folder_details = self.get_default_folders()
        self.folders_control = wx.TreeCtrl(self.frame.content_splitter,
                                -1,
                                style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|
                                wx.TR_DEFAULT_STYLE
                                )
        self.image_list = wx.ImageList(width=24, height=24)
        self.image_list.Add(wx.Bitmap(
                            self.frame.icon_dir+self.icon_name,
                            type=wx.BITMAP_TYPE_PNG)
                        )
        self.folders_control.AssignImageList(self.image_list)
        self.path = ''
        self.pop_up_menu = None

        # Register the application for required events
        self.register_events()

    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.folders_control.Bind(wx.EVT_CONTEXT_MENU, self.show_pop_menu)
        self.folders_control.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.setSelect)

    def setSelect(self, event):
        """
            Description: Called on every mounse right click event
                            and selects the item
            input_param: event - Mouse Right Click Event 
            input_type: Event instance
            
        """
        self.folders_control.SetFocusedItem(event.GetItem())

    def show_pop_menu(self, event):
        """
            Description: Called on every mounse right click event
                            and displays the Pop-Up menu for the tree item
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        if self.pop_up_menu:
            self.pop_up_menu.Destroy()
        self.pop_up_menu = wx.Menu()
        menu_item = wx.MenuItem(self.pop_up_menu,
                          wx.ID_ADD,
                          'Add Folder',
                          'Adds New folder',
                          wx.ITEM_NORMAL
                        )
        self.pop_up_menu.AppendItem(menu_item)
        self.frame.Bind(wx.EVT_MENU, self.show_add, menu_item)
        menu_item = wx.MenuItem(self.pop_up_menu,
                          wx.ID_DELETE,
                          'Delete Folder',
                          'Delets the folder',
                          wx.ITEM_NORMAL
                        )
        self.pop_up_menu.AppendItem(menu_item)
        self.frame.Bind(wx.EVT_MENU, self.show_del, menu_item)
        self.folders_control.PopupMenu(self.pop_up_menu)

    def show_add(self, event):
        """
            Description: Called whenever user clicks the Add folder item in 
                            pop-up menu and and creats new folder
            input_param: event - Menu Click Event 
            input_type: Event instance
        """
        item = self.folders_control.GetSelection()
        data = self.folders_control.GetPyData(item)
        full_path = data['path'] + '/test1'
        if full_path not in self.folder_details.keys():
            self.folder_details[full_path]={
                'items': [],
                'icon_id': 0,
                'path': full_path
            }
            self.path = data['path']
            folder_info = {'test1':{}}
            self.add_folders_to_tree(item, folder_info)
            self.folders_control.Expand(item)

    def show_del(self, event):
        """
            Description: Called whenever user clicks Delete folder item in 
                            pop-up menu and and Delets new folder
            input_param: event - Menu Click Event 
            input_type: Event instance
        """
        item = self.folders_control.GetSelection()
        data = self.folders_control.GetPyData(item)
        path = data['path']
        print path

    def get_default_folders(self):
        """
            Description: returns the default folders to display
                         on the folder tree

            return_param: - returns the details of the folders
            return_type: dict
            
        """
        return {
            '/General/Windows':{},
            '/General/Network':{},
            '/General/Internet':{},
            '/General/EMail':{},
            '/Personal/Banking':{}
        }
    
    def add_folders_to_tree(self, parent, folders_info):
        """
            Description: Recursively adds all the given folders to
                         the tree panel
            
            input_param: parent - parent folder in tree to which the
                         given folders need to be attached
            input_type: TreeCtrlItem instance
            input_param: folders_info - details of the folders that need
                          to be attached.
            input_type: dict
            
        """
        for folder_name, sub_folder in folders_info.items():
            self.path = self.path + '/' + folder_name
            new_parent = self.folders_control.AppendItem(parent,
                                folder_name,
                                image=self.folder_details.get(
                                    self.path,{}
                                ).get('icon_id', 0)
                            )
            if self.folder_details.get(self.path):
                    self.folders_control.SetPyData(new_parent,
                                    self.folder_details[self.path]
                                    )
            if sub_folder:
                self.add_folders_to_tree(new_parent, sub_folder)
            self.path = '/'.join(self.path.split('/')[:-1])
        
    def layout_folders(self):
        """
            Description: Retrievs the details of all the
                         available Folders/Groups
            
        """
        folders_info = {}
        for item in self.folder_details.keys():
            temp_value = folders_info
            for directory in item.split('/'):
                if directory:
                    temp_value = temp_value.setdefault(directory, {})
        root = self.folders_control.AddRoot('Folders')
        self.add_folders_to_tree(root, folders_info)
            
        self.folders_control.Bind(wx.EVT_TREE_SEL_CHANGED,
                                  self.folder_changed
                                  )
        
    def folder_changed(self, event):
        """
            Description: Called on every selected folder change event
            input_param: event - Folder Change Event 
            input_type: Event instance

        """
        self.frame.item_panel.list_control.DeleteAllItems()
        folder_details = self.folders_control.GetPyData(event.GetItem())
        self.frame.item_panel.items = folder_details['items'] if folder_details else []
        self.frame.item_panel.display_items()
        
        
