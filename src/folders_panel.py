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
        self.folder_details = self.get_default_folders()
        self.folders_control = wx.TreeCtrl(self.frame.content_splitter,
                                -1,
                                style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|
                                wx.TR_DEFAULT_STYLE
                                )
        self.image_list = wx.ImageList(width=24, height=24)
        self.image_list.Add(wx.Bitmap(self.frame.icon_dir+'folder.png', type=wx.BITMAP_TYPE_PNG))
        self.folders_control.AssignImageList(self.image_list)
        self.path = ''

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
        for key, value in folders_info.items():
            if value:
                self.path = self.path + '/' + key
                new_parent = self.folders_control.AppendItem(parent,
                                key,
                                image=self.folder_details.get(self.path,{}).get('icon_id', 0)
                            )
                if self.folder_details.get(self.path):
                    self.folders_control.SetPyData(new_parent,
                                    self.folder_details[self.path]['items']
                                    )
                self.add_folders_to_tree(new_parent, value)
            else:
                 temp_path = self.path + '/' + key
                 child = self.folders_control.AppendItem(parent,
                            key,
                            image=self.folder_details.get(temp_path, {}).get('icon_id', 0)
                        )
                 if self.folder_details.get(temp_path):
                    self.folders_control.SetPyData(child,
                                    self.folder_details[temp_path]['items']
                                    )
        self.path = '/'.join(self.path.split('/')[:-1])
        
    def get_folders(self):
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
        items = self.folders_control.GetPyData(event.GetItem())
        self.frame.item_panel.items = items if items else []
        self.frame.item_panel.display_items()
        
        
