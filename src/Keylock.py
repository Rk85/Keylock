import wx
import folders_panel
import items_panel
import details_panel
import login
import menu
import settings
from Crypto.Cipher import AES

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
        self.block_size = 32
        self.iv = 16 * '\x00'
        self.mode = AES.MODE_CBC
        self.dir_name = '.'
        self.file_name = ''
        self.content_saved = True
        self.icon_dir = 'icons/'
 
        # Split the main window into many sub-windows
        self.frame_splitter = wx.SplitterWindow(self, -1,
                                                style=wx.SP_3D
                                                )
        self.content_splitter = wx.SplitterWindow(self.frame_splitter,
                                                  -1,
                                                  style=wx.SP_3D
                                                  )
        
        # Instance for menu items
        self.too_bar = None
        self.file_menu = None
        self.view_menu = None

        # Instance for each panel/windows
        self.folder_panel = folders_panel.Folders(self)
        self.item_panel = items_panel.ItemPanel(self)
        self.detail_panel = details_panel.ItemDetailsPanel(self)

        menu.layout_menus(self)
        menu.layout_tool_bar(self)
        self.layout_windows()
        self.status_bar = self.CreateStatusBar()
        
        # Register the application for required events
        self.register_events()
        
        # Get credentials from the user
        password = login.LoginDialog(self)
        password.Centre()
        if password.ShowModal() == wx.ID_OK and not self.credential_valid:
            error = wx.MessageDialog(self, "Invalid/Wrong Password",
                                     'Keylock',
                                     wx.OK|wx.CENTRE|
                                     wx.OK_DEFAULT|
                                     wx.ICON_EXCLAMATION
                                     )
            error.ShowModal()
        
        self.SetIcon(wx.Icon(self.icon_dir + 'short_icon.ico', 
                             wx.BITMAP_TYPE_ICO)
                    )
        self.set_key_accelarator()
        self.set_title(self.file_name)
        
        # Show the Main Window
        self.Show()

    def layout_windows(self):
        """
            Description: Rebnder the components into the main Frame/Window
            
        """
        # Add components to their respective splitted windows
        self.content_splitter.SplitVertically(
                                self.folder_panel.folders_control,
                                self.item_panel.list_control
                            )
        self.content_splitter.SetMinimumPaneSize(200)
        self.frame_splitter.SetSashGravity(1.0)
        self.frame_splitter.SetMinimumPaneSize(200)
        self.frame_splitter.SplitHorizontally(self.content_splitter,
                                              self.detail_panel.details
                                              )
        
        # Create the sizer and add our Frame/Window into that
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.frame_splitter, 1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(sizer)

    def window_close(self, event):
        """
            Description: Called on event when the user tries
                        to close the window
            input_param: event - Window Close Event 
            input_type: Event instance
        """
        try:
            if not self.content_saved:
                event.Veto(self.confirm_file_save(True))
            else:
                event.Skip()
        except:
            event.Skip()

    def confirm_file_save(self, window_close=False):
        """
            Description: Called on event when the user tries
                        to close the window with changes in 
            input_param: event - Window Close Event 
            input_type: Event instance
        """
        close_dialog = wx.MessageDialog(self, 
                            "Do you want to save before closing?",
                            "Save Check",
                            wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
        return_value = close_dialog.ShowModal()
        window_closed = False
        if return_value == wx.ID_YES:
            self.file_menu.save_file(None)
            window_closed = True
        elif return_value == wx.ID_NO:
            window_closed = True
        elif return_value == wx.ID_CANCEL:
            pass
        if window_close and window_closed:
            self.Destroy()
        return window_closed
        
    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.Bind(wx.EVT_CLOSE, self.window_close)
        self.folder_panel.register_events()
        self.item_panel.register_events()
    
    def set_key_accelarator(self):
        """
            Description: Sets the accelarator/short -cut keys
                        for the POP_UP windows
        """
        accel_tbl = wx.AcceleratorTable(
            [(wx.ACCEL_CTRL,  ord('U'), settings.ITEM_COPY_USER ),
             (wx.ACCEL_CTRL,  ord('P'), settings.ITEM_COPY_PASS ),
             (wx.ACCEL_CTRL,  ord('E'), settings.ITEM_EDIT_ID ),
             (wx.ACCEL_CTRL,  ord('D'), settings.ITEM_DELETE_ID ),
             (wx.ACCEL_CTRL|wx.ACCEL_SHIFT,  ord('N'), settings.FOLDER_ADD_ID ),
             (wx.ACCEL_CTRL|wx.ACCEL_SHIFT,  ord('D'), settings.FOLDER_DELETE_ID ),
             (wx.ACCEL_CTRL,  ord('T'), settings.FOLDER_ADD_ITEM_ID )
             ]
        )
        self.SetAcceleratorTable(accel_tbl)

    def set_title(self, title):
        """
            Description: Sets the Frame's Tile with the give value
            input_param: title - Title string to set on the window
            input_type: title - string
            
        """
        if not self.content_saved:
            title = title + '*'
        self.SetTitle('Keylock - %s'%title)
    
        
if __name__ == '__main__':
    app = wx.App()
    frame = KeyLock()
    app.MainLoop()
