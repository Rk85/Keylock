import wx
from folder_pop_menu import FolderPopUp
import copy

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
                                style=wx.TR_HAS_BUTTONS|
                                wx.TR_DEFAULT_STYLE
                                )
        self.image_list = wx.ImageList(width=22, height=22)
        self.image_list.Add(wx.Bitmap(
                            self.frame.icon_dir+self.icon_name,
                            type=wx.BITMAP_TYPE_PNG)
                        )
        self.folders_control.AssignImageList(self.image_list)
        self.path = ''
        self.pop_up_menu = FolderPopUp(self.frame)

    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.folders_control.Bind(wx.EVT_CONTEXT_MENU, self.show_pop_menu)
        self.folders_control.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.setSelect)
        self.folders_control.Bind(wx.EVT_TREE_SEL_CHANGED, self.folder_changed)

    def setSelect(self, event):
        """
            Description: Called on every mounse right click event
                            and selects the item
            input_param: event - Mouse Right Click Event 
            input_type: Event instance
            
        """
        self.frame.item_panel.list_control.DeleteAllItems()
        folder_item = event.GetItem()
        data = self.folders_control.GetPyData(folder_item)
        self.folders_control.SelectItem(folder_item)
        if data:
            self.frame.item_panel.items = data['items']
            self.frame.item_panel.display_items()
            self.pop_up_menu.layout_pop_menu()
    
    def show_pop_menu(self, event):
        """
            Description: Called on every mounse right click event
                            and displays the Pop-Up menu for the tree item
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        self.pop_up_menu.layout_pop_menu()
    
    def add_new_folder(self, event):
        """
            Description: Called whenever user clicks the Add folder item in 
                            pop-up menu and and creats new folder
            input_param: event - Menu Click Event 
            input_type: Event instance
        """
        item = self.folders_control.GetSelection()
        data = self.folders_control.GetPyData(item)
        # TODO: Dialog for Folder add 
        full_path = data['path'] + '/test1' if data else '/test1'
        if full_path not in self.folder_details.keys():
            self.folder_details[full_path]={
                'items': [],
                'icon_id': 0,
                'path': full_path
            }
            self.path = data['path'] if data else ''
            folder_info = {'test1':{}}
            self.add_folders_to_tree(item, folder_info)
            self.folders_control.Expand(item)
            self.frame.content_saved = False
            self.frame.set_title(self.frame.file_name)
    
    def delete_folder(self, event):
        """
            Description: Called whenever user clicks Delete folder item in 
                            pop-up menu and and Delets new folder
            input_param: event - Menu Click Event 
            input_type: Event instance
        """
        # TODO: Confirmation dialog on delete
        item = self.folders_control.GetSelection()
        root_item = self.folders_control.GetRootItem()
        data = self.folders_control.GetPyData(item)
        if item != root_item and data['path'] in self.folder_details.keys():
            del self.folder_details[data['path']]
            self.folders_control.Delete(item)
            self.frame.content_saved = False
            self.frame.set_title(self.frame.file_name)
        
    def add_new_item(self, event):
        """
            Description: Called whenever user clicks the Add New item in 
                            pop-up menu and and creats new credential item
            input_param: event - Menu Click Event 
            input_type: Event instance
        """
        folder_item = self.folders_control.GetSelection()
        data = self.folders_control.GetPyData(folder_item)
        if data:
            list_items = data['items']
            # TODO: Attributes Dialog for New credential item
            new_item = {
                    'title': 'test',
                    'name': 'name',
                    'password': 'password',
                    'notes': 'notes',
                    'folder': data['path']
                }
            list_items.append(new_item)
            self.frame.item_panel.items = list_items
            self.frame.item_panel.display_items()
            self.frame.content_saved = False
            self.frame.set_title(self.frame.file_name)
    
    def get_default_folders(self):
        """
            Description: returns the default folders to display
                         on the folder tree

            return_param: - returns the details of the folders
            return_type: dict
            
        """
        item = {
                'items': [],
                'icon_id': 0,
            }
        return {
            '/General':dict(path='/General',
                                    **copy.deepcopy(item)
                                ),
            '/General/Windows':dict(path='/General/Windows',
                                    **copy.deepcopy(item)
                                ),
            '/General/Network':dict(path='/General/Network',
                                    **copy.deepcopy(item)
                                ),
            '/General/Internet':dict(path='/General/Internet',
                                    **copy.deepcopy(item)
                                ),
            '/General/EMail':dict(path='/General/EMail',
                                    **copy.deepcopy(item)
                                ),
            '/Personal':dict(path='/Personal',
                                    **copy.deepcopy(item)
                                ),
            '/Personal/Banking':dict(path='/Personal/Banking',
                                    **copy.deepcopy(item)
                                ),
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
        
