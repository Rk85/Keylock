import wx
import settings

class ItemDetailsPanel(object):
    """
        Description: Contains Details of an Item
    """
    def __init__(self, frame):
        """
            Description: Initialize the class
        """
        self.frame = frame
        self.enable = False
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
            item_data = self.frame.item_panel.get_item_details()
            if item_data:
                self.details.SetValue(item_data.get('notes', ''))
                self.enable = True
        elif event.GetEventType() == wx.EVT_LIST_ITEM_DESELECTED.typeId:
            self.details.SetValue('')
            self.enable = False
        self.set_menu_state()
            
    def set_menu_state(self):
        """
            Description: Sets the ToolBar menus and Edit Menu enable/disabled
                        based on the given input
        """
        menu_bar = self.frame.GetMenuBar() 
        for sub_menu in settings.ITEM_POP_UP_MENU['sub_menus']:
            if sub_menu.get('id'):
                menu_bar.FindItemById(sub_menu['id']).Enable(self.enable)
                if self.frame.tool_bar:
                    self.frame.tool_bar.EnableTool(sub_menu['id'], self.enable)
