import wx

class ClipTimer(wx.Timer):
    """
        Description: Clip Board timer that clears the content
                    copied to clip board
    """

    def Notify(self):
        """
            Description: This function will be called
                    whenever the timer expires
        """
        if wx.TheClipboard.Open():
            wx.TheClipboard.Clear()
            wx.TheClipboard.Close()
