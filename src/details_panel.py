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
                                   wx.TE_NOHIDESEL|
                                   wx.TE_READONLY)

    def show_details(self, event):
        """
            Description: Called on event when the user selects/deselects
                            a list item in the list panel
            input_param: event - Select/De-Select Event 
            input_type: Event instance
        """
        if event.GetEventType() == wx.EVT_LIST_ITEM_SELECTED.typeId:
            folder_item = self.frame.folder_panel.folders_control.GetFocusedItem()
            folder_data = self.frame.folder_panel.folders_control.GetPyData(folder_item)
            item_index = self.frame.item_panel.list_control.GetFocusedItem()
            if item_index != -1:
                index = self.frame.item_panel.list_control.GetItemData(item_index)
                item_data = folder_data['items'][index]
                self.details.SetValue(item_data.get('notes', ''))
        else:
            self.details.SetValue('')
