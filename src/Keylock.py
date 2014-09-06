import wx
import folders_panel
import items_panel
import details_panel
import login
import menu

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
        self.dir_name = '.'
        self.file_name = 'keylock.rdb'
        self.content_savd = True
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
        self.edit_menu = None
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
        
        # Show the Main Window
        self.Show()

        # After toolbar overlaps on the content windows
        # and borders are hidder in start-up. to avoid this
        # instantiated the window draw by resizing it
        wind1 = self.content_splitter.GetWindow1()
        wind2 = self.content_splitter.GetWindow2()
        wind1.SetSize(wind1.GetSize()+(-1, -1))
        wind2.SetSize(wind2.GetSize()+(-1, -1))
    
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
        self.frame_splitter.SetMinimumPaneSize(20)
        self.frame_splitter.SplitHorizontally(self.content_splitter,
                                              self.detail_panel.details
                                              )
        
        # Create the sizer and add our Frame/Window into that
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tool_bar, 0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        sizer.Add(self.frame_splitter, 1, flag=wx.EXPAND|wx.BOTTOM)
        self.SetSizer(sizer)
    
    def window_close(self, event):
        try:
            self.item_panel.add_items_into_file()
            event.Skip()
        except:
            event.Skip()
    
    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.Bind(wx.EVT_CLOSE, self.window_close)
        
if __name__ == '__main__':
    app = wx.App()
    frame = KeyLock()
    app.MainLoop()
