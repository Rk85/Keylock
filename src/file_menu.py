import wx
import os.path
import login

class FileMenu(object):
    """
        Description: FileMenu class - contains the callback functions
                     for each of submenu found under the File Menu
        
    """
    def __init__(self, frame):
        """
            Description: Initialize the File Menu
            
        """
        self.frame = frame
        self.default_file_dialog_options = {
            'message': 'Choose a file', 
            'defaultDir': self.frame.dir_name,
            'wildcard': '*.*'
        }
    
    def is_file_name_given(self):
        """
            Description: Find whether the user has provided the 
                         file name to access on 
            return_param: userProvidedFilename - user selected the file ot not
            return_type: Boolean
            
        """
        # show the file dialog
        dialog = wx.FileDialog(self.frame, **self.default_file_dialog_options)
        
        # user has selected a file name
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.frame.file_name = dialog.GetFilename()
            self.frame.dir_name = dialog.GetDirectory()
            self.frame.SetTitle(self.frame.file_name) # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

    def new_file(self, event):
        """
            Description: Clears previous content from editor 
                         and creats new file
            input_param: event - Create Event 
            input_type: Event instance

        """
        if not self.frame.content_saved:
            self.frame.confirm_file_save()
        self.frame.file_name = ''
        
        self.frame.folder_panel.folders_control.DeleteAllItems()
        self.frame.item_panel.list_control.DeleteAllItems()
        self.frame.folder_panel.folder_details = self.frame.folder_panel.get_default_folders()
        self.frame.folder_panel.layout_folders()
        self.frame.item_panel.display_items()
        item = self.frame.folder_panel.folders_control.GetFirstVisibleItem()
        self.frame.folder_panel.folders_control.SelectItem(item)
        
        self.frame.set_title(self.frame.file_name)
        self.frame.content_saved = True
    
    def open_file(self, event):
        """
            Description: Open the selected file
            input_param: event - Open Event 
            input_type: Event instance
            
        """
        self.default_file_dialog_options.update(
            {
                'defaultDir': self.frame.dir_name,
                'style': wx.FD_OPEN
            }
        )
        if self.is_file_name_given():
            self.frame.folder_panel.folders_control.DeleteAllItems()
            self.frame.item_panel.list_control.DeleteAllItems()
            password = login.LoginDialog(self.frame)
            if password.ShowModal() == wx.ID_OK and not self.frame.credential_valid:
                self.frame.file_name = ''
            self.frame.content_saved = True
        self.frame.set_title(self.frame.file_name)
    
    def save_file(self, event):
        """
            Description: Save the text content into a file
            input_param: event - Save Event 
            input_type: Event instance
            
        """
        if not self.frame.file_name:
            self.save_as_file(event)
        else:
            self.frame.item_panel.add_items_into_file()
            self.frame.content_saved = True
            self.frame.set_title(self.frame.file_name) 
    
    def save_as_file(self, event):
        """
            Description: Save the file into different name
            input_param: event - save Event 
            input_type: Event instance
            
        """
        self.default_file_dialog_options.update(
            {
            'message': 'Choose a file',
            'defaultDir': self.frame.dir_name,
            'wildcard': '*.*',
            'style': wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT,
            'defaultFile': self.frame.file_name
            }
        )
        if self.is_file_name_given():
            self.save_file(event)
            self.frame.set_title(self.frame.file_name) 
            self.frame.content_saved = True
       
    def exit_program(self, event):
        """
            Description: Exit from TextPad application
            input_param: event - Exit Event 
            input_type: Event instance
            
        """
        self.frame.Close()
