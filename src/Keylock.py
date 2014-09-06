import wx
import folders_panel
import items_panel
import details_panel
import login
from Crypto.Cipher import DES
import re

class KeyLock(wx.Frame):
    """
        Description: Base Frame class for the Keylock application
        
    """
    def __init__(self):
        """
            Description: Initialize the Frame class
        """
        super(KeyLock, self).__init__(None, size=(800,400))

        # variables
        self.credential_valid = False
        self.master_password = ''
        self.block_size = 8
        self.icon_dir = 'icons/'
        
        # Split the main window into many sub-windows
        self.frame_splitter = wx.SplitterWindow(self, -1,
                                                style=wx.SP_3D
                                                )
        self.content_splitter = wx.SplitterWindow(self.frame_splitter,
                                                  -1,
                                                  style=wx.SP_3D
                                                  )

        # Creat class instances for each of our windows
        self.folder_panel = folders_panel.Folders(self)
        self.item_panel = items_panel.ItemPanel(self)
        self.detail_panel = details_panel.ItemDetailsPanel(self)
        
        # Get credentials from the user
        password = login.LoginDialog(self)
        password.Centre()
        if password.ShowModal() == wx.ID_OK and not self.credential_valid:
            error = wx.MessageDialog(self, "Invalid/Wrong Password",
                                     'Keylock',
                                     wx.OK|wx.CENTRE|wx.OK_DEFAULT|wx.ICON_EXCLAMATION
                                     )
            error.ShowModal()
                
        
        # Display the components
        self.layout_components()
        self.register_events()

        self.SetIcon(wx.Icon(self.icon_dir + 'short_icon.ico', 
                             wx.BITMAP_TYPE_ICO)
                    )
        
        # Show the Main Window
        self.Show()

    def assign_column(self, new_item, line):
        """
            Description: Assign the column value into the new item
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

    def assign_new_item(self, new_item):
        """
            Description: Assign the new item to the item panel list

            input_param: new_item - Item that need to be added to the list
            input_type: new_item - dict
            
        """
        if new_item['folder'] in self.folder_panel.folder_details.keys():
            self.folder_panel.folder_details[new_item['folder']]['items'].append(new_item)
        else:
            self.folder_panel.folder_details[new_item['folder']] = {
                            'items' : [new_item],
                            'icon_id': 0
            }
    def window_close(self, event):
        """
        """
        try:
            file_content = ''
            secret_key = 'RKLOCK'
            for folder, folder_details in self.folder_panel.folder_details.items():
                for item in folder_details.get('items', []):
                    file_content = file_content + '[' + item['title'] + ']\r\n'
                    file_content = file_content + 'User Name: ' + item['name'] + '\r\n'
                    file_content = file_content + 'Password: ' + item['password'] + '\r\n'
                    file_content = file_content + 'Notes: ' + item['notes'] + '\r\n'
                    file_content = file_content + 'Group: ' + item['folder'] + '\r\n'
                    file_content = file_content + 'Item Icon' + str(item.get('item_icon_id', 0)) + '\r\n'
                    file_content = file_content + '\r\n'

            if len(file_content)%self.block_size != 0:
                padding = ''.zfill(
                             self.block_size-len(file_content)%self.block_size
                        )
                secret_key = secret_key + padding
            secret_key = secret_key + '\r\n'
            if self.master_password and file_content:
                des_obj=DES.new(self.master_password, DES.MODE_ECB)
                with open('keylock.rdb', 'wb') as pass_file:
                    total_contet = secret_key+file_content
                    pass_file.write(des_obj.encrypt(total_contet))
            event.Skip()
        except:
            event.Skip()
    def display_existing_items(self,
                               file_name='keylock.rdb',
                               ecrypted_file=True):
        """
            Description: Reads the credential informatios from already
                         stored file and constructs them into the dict
            
        """
        new_item = {}
        with open(file_name, 'rb') as pass_file:
            if ecrypted_file:
               des_obj=DES.new(self.master_password, DES.MODE_ECB)
               file_content = des_obj.decrypt(pass_file.read())
               file_lines = re.split('\r\n|\n', file_content)
               self.credential_valid = file_lines[0][:6]=='RKLOCK'
            else:
                file_content = pass_file.read()
                file_lines = re.split('\r\n|\n', file_content)
            if self.credential_valid:
                self.folder_panel.folder_details = {}
                for line in file_lines[1:]:
                    line = line.strip('\r\n|\n').strip()
                    if not line and new_item:
                        self.assign_new_item(new_item)
                        new_item = {}
                    elif line:
                        self.assign_column(new_item, line)
        self.folder_panel.get_folders()
        self.item_panel.display_items()
       
    def layout_components(self):
        """
            Description: Rebnder the components into the main Frame/Window
            
        """
        # Add components to their respective splitted windows
        self.content_splitter.SplitVertically(self.folder_panel.folders_control,
                                              self.item_panel.list_control
                                              )
        self.content_splitter.SetMinimumPaneSize(200)
        self.frame_splitter.SetSashGravity(1.0)
        self.frame_splitter.SetMinimumPaneSize(20)
        self.frame_splitter.SplitHorizontally(self.content_splitter,
                                              self.detail_panel.details
                                              )
        
        # Create the sizer and add our Frame/Window into that
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.frame_splitter, 1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(sizer)

    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.Bind(wx.EVT_CLOSE, self.window_close)
        
if __name__ == '__main__':
    app = wx.App()
    frame = KeyLock()
    app.MainLoop()
