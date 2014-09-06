import wx

class LoginDialog(wx.Dialog):
    """
        Description: Dialog class for the Login Window
    """
    def __init__(self, frame):
        """
            Description: Initialize the Login Window
        """
        super(LoginDialog, self).__init__(None,
                                          -1,
                                          "Enter Master Key",
                                          size=(300, 150)
                                          )
        # Create login Window components
        self.text = wx.StaticText(self, label="Enter Master Key: ")
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.no_password = wx.TextCtrl(self)
        self.ok_button = wx.Button(self, label="OK", id=wx.ID_OK)
        self.cancel_button = wx.Button(self, label="Cancel", id=wx.ID_CANCEL)
        self.pass_toggle_check = wx.CheckBox(self, label="Show Normal Text")
        self.frame = frame

        # Display the components
        self.layout_components()
        self.register_events()
        
        self.no_password.Hide()
        self.SetIcon(wx.Icon(self.frame.icon_dir + 'short_icon.ico', 
                             wx.BITMAP_TYPE_ICO)
                    )

    def register_events(self):
        """
            Description: Register the required events for this Window
        """
        self.pass_toggle_check.Bind(wx.EVT_CHECKBOX,
                                    self.change_password_text_type
                                    )
        self.ok_button.Bind(wx.EVT_BUTTON, self.verify_credentials)
        self.cancel_button.Bind(wx.EVT_BUTTON,
                                self.verify_credentials
                                )

    def verify_credentials(self, event):
        """
        """
        if event.GetId() == wx.ID_OK:
            self.frame.master_password = self.password.GetValue() if self.password.IsShown() else self.no_password.GetValue()
            if len(self.frame.master_password)%self.frame.block_size !=0:
                self.frame.master_password = self.frame.master_password.zfill(len(self.frame.master_password)+len(self.frame.master_password)%self.frame.block_size)
            try:
                self.frame.display_existing_items()
            except ValueError as e:
                print e
                self.frame.folder_panel.folder_details = self.frame.folder_panel.get_default_folders()
                self.frame.item_panel.items = []
                self.frame.folder_panel.get_folders()
            event.Skip()
        if event.GetId() == wx.ID_CANCEL:
            self.frame.folder_panel.get_folders()
            event.Skip()
            
    def layout_components(self):
        """
            Description: Rebnder the components into the main Frame/Window
        """
        # Create the Sizer the Window
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Insert the components into their sizer
        self.pass_text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pass_text_sizer.Add(self.text, 0, wx.ALL, 4)
        self.pass_text_sizer.Add(self.password, 1, wx.ALL, 4)
        self.pass_text_sizer.Add(self.no_password, 1, wx.ALL, 4)
        self.main_sizer.Add(self.pass_text_sizer, 1,
                            wx.EXPAND|wx.TOP|wx.RIGHT, 8
                            )

        self.pass_check_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pass_check_sizer.Add(self.pass_toggle_check, 0, wx.ALL, 4)
        self.main_sizer.Add(self.pass_check_sizer, 1,
                            wx.EXPAND|wx.TOP|wx.BOTTOM, 2
                            )
        
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.ok_button, 0, wx.ALL, 8)
        self.button_sizer.Add(self.cancel_button, 0, wx.ALL, 8)
        self.main_sizer.Add(self.button_sizer, 0, wx.ALL|wx.ALIGN_CENTER, 8)

        self.SetSizer(self.main_sizer)
        
    def change_password_text_type(self, event):
        """
            Description: Changes the text as * or alphanumeric 
                         based on the checkbox value
            input_param: event - CheckBox change Event 
            input_type: Event instance
        """
        if (self.pass_toggle_check.GetValue()):
            self.no_password.SetValue(self.password.GetValue())
            self.no_password.Show()
            self.password.Hide()
        else:
            self.password.SetValue(self.no_password.GetValue())
            self.password.Show()
            self.no_password.Hide()
        self.Layout()
        
        