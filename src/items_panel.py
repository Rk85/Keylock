import wx
from Crypto.Cipher import AES
import re
import os
from item_pop_menu import ListItemPopUp
import item_pop_menu
import settings
from clip_board_timer import ClipTimer
from item_window import ItemWindow
import settings

class ItemPanel(object):
    """
        Description: List Items Panel to display the Credntial details
    """
    def __init__(self, frame):
        """
            Description: Initialize the class
            
        """
        self.frame = frame
        self.icon_name = 'item.png'
        self.items = []
        self.show_name = False
        self.show_pass = False
        self.list_control = wx.ListCtrl(self.frame.content_splitter,
                                   style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.set_columns()
        #self.list_control.SetItemBackgroundColour(wx.BLACK)
        self.image_list = wx.ImageList(width=10, height=10)
        self.image_list.Add(wx.Bitmap(self.frame.icon_dir+self.icon_name,
                                      type=wx.BITMAP_TYPE_PNG)
                            )
        self.list_control.AssignImageList(self.image_list,
                                          wx.IMAGE_LIST_SMALL
                                          )

        self.pop_up_menu = ListItemPopUp(self.frame)
    
    def set_columns(self):
        """
            Description: Sets the column name for list panel
        """
        self.list_control.InsertColumn(0, 'Title')
        self.list_control.InsertColumn(1, 'User Name')
        self.list_control.InsertColumn(2, 'Password')
        
        self.list_control.SetColumnWidth(0, 100)
        self.list_control.SetColumnWidth(1, 200)
        self.list_control.SetColumnWidth(2, 150)
        
    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.list_window = self.frame.content_splitter.GetWindow2()
        self.list_control.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.show_pop_menu)
        self.list_control.Bind(wx.EVT_LIST_ITEM_SELECTED, self.show_details)
        self.list_control.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.show_details)
        self.list_window.Bind(wx.EVT_KILL_FOCUS, self.show_details)
        self.list_window.Bind(wx.EVT_SET_FOCUS, self.show_details)

    def show_details(self, event):
        """
            Description: Called on event when the user selects/deselects
                            a list item in the list panel
            input_param: event - Select/De-Select Event 
            input_type: Event instance
        """
        self.frame.detail_panel.show_details(event)
        event.Skip()

    def copy_item(self, event):
        """
            Description: Called on event when the user clicks
                            Copy menu item or corresponding Accel Key
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        item_data = self.get_item_details()
        menu_id = event.GetId()
        if wx.TheClipboard.Open() and item_data:
            wx.TheClipboard.Clear()
            if menu_id == settings.ITEM_COPY_USER:
                wx.TheClipboard.SetData(wx.TextDataObject(item_data['name']))
            elif menu_id == settings.ITEM_COPY_PASS:
                wx.TheClipboard.SetData(wx.TextDataObject(item_data['password']))
            else:
                event.Skip()
            wx.TheClipboard.Close()
            self.timer = ClipTimer()
            self.timer.Start(self.frame.expiry, oneShot=True)

    def show_pop_menu(self, event):
        """
            Description: Called on every mouse right click event
                            and displays the Pop-Up menu for the tree item
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        self.pop_up_menu.layout_pop_menu()

    def get_item_details(self):
        """
            Description: Gets the Selected Item's dictionary detail

            return_param: item_data - Details of the currently selected item
            return_type: dict
            
        """
        item_data = {}
        folder_item = self.frame.folder_panel.folders_control.GetFocusedItem()
        folder_data = self.frame.folder_panel.folders_control.GetPyData(folder_item)
        item_count = self.frame.item_panel.list_control.GetSelectedItemCount()
        if item_count:
            item_index = self.frame.item_panel.list_control.GetFocusedItem()
            index = self.frame.item_panel.list_control.GetItemData(item_index)
            item_data = folder_data['items'][index]
        return item_data
    
    def delete_item(self, event):
        """
            Description: Called on event when the user click delete
                            menu in pop or corresponding Accel Key
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        folder_item = self.frame.folder_panel.folders_control.GetFocusedItem()
        folder_data = self.frame.folder_panel.folders_control.GetPyData(folder_item)
        item_index = self.list_control.GetFocusedItem()
        if item_index != -1:
            index = self.list_control.GetItemData(item_index)
            self.list_control.DeleteItem(item_index)
            folder_data['items'][index]['active'] = False
            self.frame.content_saved = False
            self.frame.set_title(self.frame.file_name)
            self.frame.detail_panel.details.SetValue('')
            self.frame.detail_panel.enable = False
            self.frame.detail_panel.set_menu_state()

    def edit_item(self, event):
        """
            Description: Called on event when the user click Edit
                            menu in pop or corresponding Accel Key
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        folder_item = self.frame.folder_panel.folders_control.GetFocusedItem()
        folder_data = self.frame.folder_panel.folders_control.GetPyData(folder_item)
        item_index = self.list_control.GetFocusedItem()
        if item_index != -1:
            index = self.list_control.GetItemData(item_index)
            item_data = folder_data['items'][index]
            edit_item = ItemWindow(self.frame)
            edit_item.title_control.SetValue(item_data.get('title'))
            edit_item.name_control.SetValue(item_data.get('name'))
            edit_item.password_control.SetValue(item_data.get('password'))
            edit_item.notes_control.SetValue(item_data.get('notes'))
            if edit_item.ShowModal() == wx.ID_OK:
                item_data['title'] = edit_item.title
                item_data['name'] = edit_item.name
                item_data['password'] = edit_item.password
                item_data['notes'] = edit_item.notes
                self.frame.content_saved = False
                self.display_items()
                self.frame.detail_panel.details.SetValue('')
                self.frame.set_title(self.frame.file_name)
            edit_item.Destroy()
    def display_items(self):
        """
            Description: Displays the list of credential items on the panel
            
        """
        self.list_control.DeleteAllItems()
        for index, item in enumerate(self.items):
            if item.get('active'):
                row_id = self.list_control.GetItemCount()
                self.list_control.InsertStringItem(row_id, item['title'])
                if self.show_name:
                    self.list_control.SetStringItem(row_id, 1, item['name'])
                else:
                    self.list_control.SetStringItem(row_id, 1, '*'*len(item['name']))
                if self.show_pass:
                    self.list_control.SetStringItem(row_id, 2, item['password'])
                else:
                    self.list_control.SetStringItem(row_id, 2, '*'*len(item['password']))
                self.list_control.SetItemImage(row_id, int(item.get('item_icon_id', 0)))
                self.list_control.SetItemData(row_id, index)
                if (row_id % 2) == 0:
                    self.list_control.SetItemBackgroundColour(row_id, wx.RED)
    
    def assign_new_item_to_folder(self, new_item):
        """
            Description: Assign the new item to the item panel list

            input_param: new_item - Item that need to be added to the list
            input_type: new_item - dict
            
        """
        new_item['active'] = True
        if new_item['folder'] in self.frame.folder_panel.folder_details.keys():
            self.frame.folder_panel.folder_details[new_item['folder']]['items'].append(new_item)
        else:
            new_folder = {
                'icon_id': 0,
                'path': new_item.get('folder', '/'),
                'items': []
            }
            if new_item.get('title'):
                new_folder['items'] = [new_item]
            self.frame.folder_panel.folder_details[new_item['folder']] = new_folder
            
    def set_column_value(self, new_item, line):
        """
            Description: Assign the column value into the new item dictionary
                          from the given line
            input_param: new_item - Details of items to which the column
                          value need to be added
            input_type: new_item - dict
            input_param: line - line read from the stored file
            input_type: line - string
            
        """
        try:
            line = line.strip().split(':')
            if line[0][0] == '[':
                new_item['title'] = line[0][1:-1]
            elif line[0] == 'User Name':
                new_item['name'] = ':'.join(line[1:]).strip()
            elif line[0] == 'Password':
                new_item['password'] = ':'.join(line[1:]).strip()
            elif line[0] == 'Notes':
                new_item['notes'] = ':'.join(line[1:]).strip()
            elif line[0] == 'Group':
                new_item['folder'] = ':'.join(line[1:]).strip()
            elif line[0] == 'Item Icon':
                new_item['item_icon_id'] = ':'.join(line[1:]).strip()
            else:
                new_item['notes'] = new_item.get('notes', '') + "\r\n" + ':'.join(line).strip()
        except IndexError as e:
            pass

    def add_items_from_file(self, ecrypted_file=True):
        """
            Description: Reads the items from already
                         stored file and constructs them into the dict
            input_param: encrypted_file - input file is encrypted or
                            normal text file
            input_type: ecrypted_file - Boolean
            
        """
        new_item = {}
        with open(os.path.join(self.frame.dir_name, self.frame.file_name), 'rb') as pass_file:
            if ecrypted_file:
               aes_obj=AES.new(self.frame.master_password.encode("utf8"),
                               self.frame.mode,
                               IV=self.frame.iv.encode("utf8"))
               file_content = aes_obj.decrypt(pass_file.read())
               file_content = file_content.decode("utf8")
               file_lines = re.split('\r\n|\n', file_content)
               self.frame.credential_valid = file_lines[0][:6]=='RKLOCK'
            else:
                file_content = pass_file.read()
                file_lines = re.split('\r\n|\n', file_content)
                self.frame.credential_valid = file_lines[0][:6]=='RKLOCK'
        if self.frame.credential_valid:
           self.frame.folder_panel.folder_details = {}
           for line in file_lines[1:]:
               line = line.strip('\r\n|\n').strip()
               if not line and new_item.get('folder'):
                   self.assign_new_item_to_folder(new_item)
                   new_item = {}
               elif line:
                   self.set_column_value(new_item, line)
        self.frame.folder_panel.layout_folders()
        self.display_items()

    def add_items_into_file(self, encrypted_file=True):
        """
            Description: Writes the items into file
            input_param: encrypted_file - output file is encrypted or
                            normal text file
            input_type: ecrypted_file - Boolean
            
        """
        try:
            file_content = ''
            secret_key = 'RKLOCK'
            for folder, folder_details in self.frame.folder_panel.folder_details.items():
                if len( folder_details.get('items', [])) > 0:
                    for item in folder_details.get('items', []):
                        if item.get('active'):
                            file_content = file_content + '[' + item['title'] + ']\r\n'
                            file_content = file_content + 'User Name: ' + item['name'] + '\r\n'
                            file_content = file_content + 'Password: ' + item['password'] + '\r\n'
                            file_content = file_content + 'Notes: ' + item['notes'] + '\r\n'
                            file_content = file_content + 'Group: ' + item['folder'] + '\r\n'
                            file_content = file_content + 'Item Icon: ' + str(item.get('item_icon_id', 0)) + '\r\n'
                            file_content = file_content + '\r\n'
                else:
                    file_content = file_content + 'Group: ' + folder + '\r\n\r\n'

            secret_key = secret_key + '\r\n'
            if encrypted_file and self.frame.master_password and file_content:
                aes_obj=AES.new(self.frame.master_password.encode("utf8"),
                               self.frame.mode,
                               IV=self.frame.iv.encode("utf8"))
                with open(os.path.join(self.frame.dir_name, self.frame.file_name), 'wb') as pass_file:
                    total_contet = secret_key+file_content
                    pass_file.write(aes_obj.encrypt(total_contet.encode("utf8")))
        except Exception as e:
            print(e)
            pass
