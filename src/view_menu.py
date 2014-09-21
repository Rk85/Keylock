import wx
import menu

class ViewMenu(object):
    """
        Description: ViewMenu class - contains the callback functions
                     for each of submenu found under the View Menu
        
    """
    def __init__(self, frame):
        """
            Description: Initialize the View Menu
            
        """
        self.frame = frame
    
    def view_tool_bar(self, event):
        """
            Description: Toggles the Tool Bar Visiblity
            input_param: event - Menu Event 
            input_type: Event instance

        """
        if self.frame.tool_bar and self.frame.tool_bar.IsShown():
            self.frame.tool_bar.Destroy()
            self.frame.Layout()
        else:
            menu.layout_tool_bar(self.frame)
            item_index = self.frame.item_panel.list_control.GetSelectedItemCount()
            if item_index:
                self.frame.detail_panel.enable = True
                self.frame.detail_panel.set_menu_state()
            root_item = self.frame.folder_panel.folders_control.GetRootItem()
            select_item = self.frame.folder_panel.folders_control.GetFocusedItem()
            if root_item == select_item:
                self.frame.folder_panel.enable = False
            else:
                self.frame.folder_panel.enable = True
            self.frame.folder_panel.set_menu_state()
            self.frame.Layout()
    
    def view_status_bar(self, event):
        """
            Description: Toggles the Status Bar Visiblity
            input_param: event - Menu Event 
            input_type: Event instance

        """
        if self.frame.status_bar and self.frame.status_bar.IsShown():
            self.frame.status_bar.Destroy()
            self.frame.Layout()
        else:
            self.frame.status_bar = self.frame.CreateStatusBar()
            self.frame.Layout()

    def hide_user_name(self, event):
        """
            Description: Toggles the User name string display
            input_param: event - Menu Event 
            input_type: Event instance

        """
        self.frame.item_panel.show_name = not event.IsChecked()
        self.frame.item_panel.display_items()

    def hide_password(self, event):
        """
            Description: Toggles the Password string display
            input_param: event - Menu Event 
            input_type: Event instance

        """
        self.frame.item_panel.show_pass = not event.IsChecked()
        self.frame.item_panel.display_items()
    
    def view_about_info(self, event):
        """
            Description: Display the Application detail window
            input_param: event - Menu Event 
            input_type: Event instance

        """
        info = wx.AboutDialogInfo()
        description = """This application helps the user to store their login
credentials in encrypted file in thier desktop"""
        licence = """Keylock is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License, 
or (at your option) any later version.

Keylock is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details."""
        info.SetIcon(wx.Icon('icons/about.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Keylock')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 - 2014 Radhakrishnan Raji rachandkrishnan@gmail.com')
        info.SetLicence(licence)
        info.AddDeveloper('Radhakrishnan Raji')
        wx.AboutBox(info)
