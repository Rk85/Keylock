import wx
from Crypto.Cipher import DES
import re
import os
from list_pop_menu import ListItemPopUp
import list_pop_menu
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
        self.list_control = wx.ListCtrl(self.frame.content_splitter,
                                   style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.set_columns()
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

    def show_details(self, event):
        """
            Description: Called on event when the user selects/deselects
                            a list item in the list panel
            input_param: event - Select/De-Select Event 
            input_type: Event instance
        """
        self.frame.detail_panel.show_details(event)

    def copy_item(self, event):
        """
            Description: Called on event when the user clicks
                            Copy menu item or corresponding Accel Key
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        item_index = self.list_control.GetFocusedItem()
        menu_id = event.GetId()
        if wx.TheClipboard.Open() and item_index != -1:
            wx.TheClipboard.Clear()
            if menu_id == settings.ITEM_COPY_USER:
                wx.TheClipboard.SetData(wx.TextDataObject(self.list_control.GetItem(item_index, 1).GetText()))
            elif menu_id == settings.ITEM_COPY_PASS:
                wx.TheClipboard.SetData(wx.TextDataObject(self.list_control.GetItem(item_index, 2).GetText()))
            else:
                event.Skip()
            wx.TheClipboard.Close()
    
    def show_pop_menu(self, event):
        """
            Description: Called on every mouse right click event
                            and displays the Pop-Up menu for the tree item
            input_param: event - Context Menu Event 
            input_type: Event instance
        """
        self.pop_up_menu.layout_pop_menu()
    
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
            del folder_data['items'][index]
            self.frame.content_saved = False
            self.frame.set_title(self.frame.file_name)
    
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
            # Todo: Edit Dialog to enter the details
            self.list_control.GetItem(item_index, 1).SetText('poda')
            self.frame.content_saved = False
            self.frame.set_title(self.frame.file_name)
    
    def display_items(self):
        """
            Description: Displays the list of credential items on the panel
            
        """
        self.list_control.DeleteAllItems()
        for index, item in enumerate(self.items):
            row_id = self.list_control.GetItemCount()
            self.list_control.InsertStringItem(row_id, item['title'])
            self.list_control.SetStringItem(row_id, 1, item['name'])
            self.list_control.SetStringItem(row_id, 2, item['password'])
            self.list_control.SetItemImage(row_id, int(item.get('item_icon_id', 0)))
            self.list_control.SetItemData(row_id, index)
            if (row_id % 2) == 0:
                self.list_control.SetItemBackgroundColour(row_id, '#e6f1f5')
    
    def assign_new_item_to_folder(self, new_item):
        """
            Description: Assign the new item to the item panel list

            input_param: new_item - Item that need to be added to the list
            input_type: new_item - dict
            
        """
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
               des_obj=DES.new(self.frame.master_password, DES.MODE_ECB)
               file_content = des_obj.decrypt(pass_file.read())
               file_lines = re.split('\r\n|\n', file_content)
               self.frame.credential_valid = file_lines[0][:6]=='RKLOCK'
            else:
                file_content = pass_file.read()
                file_lines = re.split('\r\n|\n', file_content)
            if self.frame.credential_valid:
                self.frame.folder_panel.folder_details = {}
                for line in file_lines[1:]:
                    line = line.strip('\r\n|\n').strip()
                    if not line and new_item:
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
                        file_content = file_content + '[' + item['title'] + ']\r\n'
                        file_content = file_content + 'User Name: ' + item['name'] + '\r\n'
                        file_content = file_content + 'Password: ' + item['password'] + '\r\n'
                        file_content = file_content + 'Notes: ' + item['notes'] + '\r\n'
                        file_content = file_content + 'Group: ' + item['folder'] + '\r\n'
                        file_content = file_content + 'Item Icon: ' + str(item.get('item_icon_id', 0)) + '\r\n'
                        file_content = file_content + '\r\n'
                else:
                    file_content = file_content + 'Group: ' + folder + '\r\n\r\n'

            if len(file_content)%self.frame.block_size != 0:
                padding = ''.zfill(
                             self.frame.block_size-len(file_content)%self.frame.block_size
                        )
                secret_key = secret_key + padding
            secret_key = secret_key + '\r\n'
            if encrypted_file and self.frame.master_password and file_content:
                des_obj=DES.new(self.frame.master_password, DES.MODE_ECB)
                with open(os.path.join(self.frame.dir_name, self.frame.file_name), 'wb') as pass_file:
                    total_contet = secret_key+file_content
                    pass_file.write(des_obj.encrypt(total_contet))
            event.Skip()
        except Exception as e:
            pass
