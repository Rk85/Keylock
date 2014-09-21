import wx

class ItemWindow(wx.Dialog):
    """
        Description: Dialog class for the Item Window
    """
    def __init__(self, frame):
        """
            Description: Initialize the Item Window
        """
        super(ItemWindow, self).__init__(None,
                                          -1,
                                          "Item Details",
                                          size=(400, 350)
                                          )
        # Create login Window components
        self.frame = frame
        self.title = ''
        self.name = ''
        self.password = ''
        self.notes = ''
        self.action = 0
        self.title_text = wx.StaticText(self, label="Enter Title: ")
        self.name_text = wx.StaticText(self, label="Enter User Name: ")
        self.password_text = wx.StaticText(self, label="Enter Password: ")
        self.notes_text = wx.StaticText(self, label="Enter Other Details: ")


        self.title_control = wx.TextCtrl(self, size=wx.Size(150, 24))
        self.name_control = wx.TextCtrl(self, size=wx.Size(150, 24))
        self.password_control = wx.TextCtrl(self, style=wx.TE_PASSWORD|
                                    wx.TE_PROCESS_ENTER, size=wx.Size(150, 24))
        self.no_password_control = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                                               size=wx.Size(150, 24))
        self.pass_toggle_check = wx.CheckBox(self, label="Show Text")
        self.notes_control = wx.TextCtrl(self, size=wx.Size(300, 100), style=wx.TE_MULTILINE)
        
        self.ok_button = wx.Button(self, label="OK", id=wx.ID_OK)
        self.cancel_button = wx.Button(self, label="Cancel", id=wx.ID_CANCEL)
        
        self.ok_button.SetDefault()
        
        # Display the components
        self.layout_components()
        self.register_events()
        
        self.no_password_control.Hide()
        self.SetIcon(wx.Icon(self.frame.icon_dir + 'short_icon.ico', 
                             wx.BITMAP_TYPE_ICO)
                    )

    def register_events(self):
        """
            Description: Register the required events for Item Window
            
        """
        self.pass_toggle_check.Bind(wx.EVT_CHECKBOX,
                                    self.change_password_text_type
                                    )
        self.ok_button.Bind(wx.EVT_BUTTON, self.get_item_details)
        self.cancel_button.Bind(wx.EVT_BUTTON,
                                self.get_item_details
                                )

    def get_item_details(self, event):
        """
            Description: Gets the details for the Item
            input_param: event - Button Click Event 
            input_type: Event instance
            
        """
        if event.GetId() == wx.ID_OK:
            if not self.title_control.GetValue():
                error = wx.MessageDialog(self, "Title can not be Empty",
                                     'Item',
                                     wx.OK|wx.CENTRE|
                                     wx.OK_DEFAULT|
                                     wx.ICON_EXCLAMATION
                                     )
                error.ShowModal()
            else:
                self.title = self.title_control.GetValue()
                self.name = self.name_control.GetValue()
                self.password = self.password_control.GetValue() if self.password_control.IsShown() else self.no_password_control.GetValue()
                self.notes = self.notes_control.GetValue()
                self.action = wx.ID_OK
                self.Destroy()
                event.Skip()
        if event.GetId() == wx.ID_CANCEL:
            self.action = wx.ID_CANCEL
            self.Destroy()
            event.Skip()
            
    def layout_components(self):
        """
            Description: Render the components into the Item Frame/Window
            
        """
        # Create the Sizer the Window
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.title_sizer.Add(self.title_text, 0, wx.ALL, 22)
        self.title_sizer.Add(self.title_control, 0, wx.ALL, 22)
        self.main_sizer.Add(self.title_sizer, 0,
                            wx.RIGHT
                            )

        self.name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.name_sizer.Add(self.name_text, 0, wx.ALL, 10)
        self.name_sizer.Add(self.name_control, 0, wx.ALL, 10)
        self.main_sizer.Add(self.name_sizer, 0,
                            wx.RIGHT
                            )
        
        # Insert the components into their sizer
        self.pass_text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pass_text_sizer.Add(self.password_text, 0, wx.ALL, 12)
        self.pass_text_sizer.Add(self.password_control, 0, wx.ALL, 12)
        self.pass_text_sizer.Add(self.no_password_control, 0, wx.ALL, 12)
        self.pass_text_sizer.Add(self.pass_toggle_check, 0, wx.ALL, 12)
        self.main_sizer.Add(self.pass_text_sizer, 0,
                            wx.RIGHT
                            )

        self.notes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notes_sizer.Add(self.notes_text, 0, wx.ALL, 6)
        self.notes_sizer.Add(self.notes_control, 0, wx.ALL, 6)
        self.main_sizer.Add(self.notes_sizer, 0,
                            wx.RIGHT
                            )
        
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.ok_button, 0, wx.ALL, 4)
        self.button_sizer.Add(self.cancel_button, 0, wx.ALL, 4)
        self.main_sizer.Add(self.button_sizer, 0, wx.TOP|wx.ALIGN_CENTER, 6)

        self.SetSizer(self.main_sizer)
        
    def change_password_text_type(self, event):
        """
            Description: Changes the text as * or alphanumeric 
                         based on the checkbox value
            input_param: event - CheckBox change Event 
            input_type: Event instance
        """
        if (self.pass_toggle_check.GetValue()):
            self.no_password_control.SetValue(self.password_control.GetValue())
            self.no_password_control.Show()
            self.password_control.Hide()
        else:
            self.password_control.SetValue(self.no_password_control.GetValue())
            self.password_control.Show()
            self.no_password_control.Hide()
        self.Layout()
