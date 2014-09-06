import wx

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
        self.image_list.Add(wx.Bitmap(self.frame.icon_dir+'new.png', type=wx.BITMAP_TYPE_PNG))
        self.list_control.AssignImageList(self.image_list, wx.IMAGE_LIST_SMALL)
        
        for item in self.items:
            row_id = self.list_control.GetItemCount()
            self.list_control.InsertStringItem(row_id, item['title'])
            self.list_control.SetStringItem(row_id, 1, item['name'])
            self.list_control.SetStringItem(row_id, 2, item['password'])
            self.list_control.SetStringItem(row_id, 3, item['notes'])
            self.list_control.SetItemImage(row_id, item.get('item_icon_id', 0))
            if (row_id % 2) == 0:
                self.list_control.SetItemBackgroundColour(row_id, '#e6f1f5')
        
