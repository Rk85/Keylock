import wx

class ItemDetailsPanel(wx.Panel):
    """
        Description: Contains Details of an Item
    """
    def __init__(self, frame):
        """
            Description: Initialize the class
        """
        self.frame = frame
        self.details = wx.TextCtrl(self.frame.frame_splitter,
                                   style=wx.TE_MULTILINE|
                                   wx.TE_NOHIDESEL)
