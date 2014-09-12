import wx
from Crypto.Cipher import DES
import re
import os

class ItemPanel(object):
    """
        Description: List Items Panel to display the Credntial details
    """
    def __init__(self, frame):
        """
            Description: Initialize the class
            
        """
        self.frame = frame
        self.items = []
        self.list_control = wx.ListCtrl(self.frame.content_splitter,
                                   style=wx.LC_REPORT)
        self.list_control.InsertColumn(0, 'Title')
        self.list_control.InsertColumn(1, 'User Name')
        self.list_control.InsertColumn(2, 'Password')
        self.list_control.InsertColumn(3, 'Notes')

        self.list_control.SetColumnWidth(0, 100)
        self.list_control.SetColumnWidth(1, 200)
        self.list_control.SetColumnWidth(2, 150)
        self.list_control.SetColumnWidth(3, 420)

    def display_items(self):
        """
            Description: Displays the list of credential items on the panel
            
        """
        self.image_list = wx.ImageList(width=10, height=10)
        self.image_list.Add(wx.Bitmap(self.frame.icon_dir+'new.png',
                                      type=wx.BITMAP_TYPE_PNG)
                            )
        self.list_control.AssignImageList(self.image_list,
                                          wx.IMAGE_LIST_SMALL
                                          )
        
        for item in self.items:
            row_id = self.list_control.GetItemCount()
            self.list_control.InsertStringItem(row_id, item['title'])
            self.list_control.SetStringItem(row_id, 1, item['name'])
            self.list_control.SetStringItem(row_id, 2, item['password'])
            self.list_control.SetStringItem(row_id, 3, item['notes'])
            self.list_control.SetItemImage(row_id, item.get('item_icon_id', 0))
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
            self.frame.folder_panel.folder_details[new_item['folder']] = {
                            'items' : [new_item],
                            'icon_id': 0,
                            'path': new_item.get('folder', '/')
            }

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
                for item in folder_details.get('items', []):
                    file_content = file_content + '[' + item['title'] + ']\r\n'
                    file_content = file_content + 'User Name: ' + item['name'] + '\r\n'
                    file_content = file_content + 'Password: ' + item['password'] + '\r\n'
                    file_content = file_content + 'Notes: ' + item['notes'] + '\r\n'
                    file_content = file_content + 'Group: ' + item['folder'] + '\r\n'
                    file_content = file_content + 'Item Icon' + str(item.get('item_icon_id', 0)) + '\r\n'
                    file_content = file_content + '\r\n'

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
        except:
            event.Skip()
