#!/usr/bin/env python3
import wx, os

APP_TITLE = "TextEditer"



class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetSize(815, 658)
        
        self.SetBackgroundColour("#ffd700")

        self.filename = ""
        self.dirname = ""
        
        self.panel = wx.Panel(self)      
        
        self.MenuMaker()

        self.INTextCrtl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE |
                                      wx.HSCROLL, pos=(0,0), size=(800, 600))
        self.INTextCrtl.SetBackgroundColour(wx.Colour(224,224,255))
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.INTextCrtl, proportion = 1, flag = wx.EXPAND,
                       border = 10)
        self.panel.SetSizer(self.sizer)
        
    def StatusBarMaker(self):
        self.CreateStatusBar()
        self.SetStatusText("TextEditer[simpled]")
        
    def MenuMaker(self):
        menubar = wx.MenuBar()
        ##       File Menu
        FileMenu = wx.Menu()

        OpenItem = FileMenu.Append(-1, "&Open\tCtrl-O",
        "Open a file and edit it")
        #NewItem = 
        FileMenu.AppendSeparator()

        SaveItem = FileMenu.Append(-1, "&Save\tCtrl-S",     
        "Save a file make it can't be lost")
        SaveAsItem = FileMenu.Append(-1,"&Save As\tShift-S",
        "Sava a copy")                             
        FileMenu.AppendSeparator()

        ExitItem = FileMenu.Append(wx.ID_EXIT)
        
        ##        About Menu
        helpMenu = wx.Menu()
        BoardItem = helpMenu.Append(-1,"FastCopyBoard\tCtrl-F1",
        "a FastCopyBoard")
        AboutItem = helpMenu.Append(wx.ID_ABOUT)
        
        menubar.Append(FileMenu, "&File")
        menubar.Append(helpMenu, "&Help")
        
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnOpen, OpenItem)
        self.Bind(wx.EVT_MENU, self.OnExit, ExitItem)
        self.Bind(wx.EVT_MENU, self.OnSave, SaveItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, AboutItem)
        self.Bind(wx.EVT_MENU, self.OnOpenBroad, BoardItem)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, SaveAsItem)

    def OnExit(self, event):
        self.Close(True)

    def OnOpen(self, event):
        dlg = wx.FileDialog(self,"Choose a file",self.dirname,"","", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname,self.filename),'r')
            try:
                self.INTextCrtl.SetValue(f.read())
            except UnicodeDecodeError:
                wx.MessageBox("TextEiditer can't read it, maybe it's a binary file",
                      "TextEditer Can't Read",
                      wx.OK|wx.ICON_WARNING)
                self.filename = ""
            else:
                filename = os.path.join(self.dirname,self.filename)
                self.SetTitle("[edit]"+filename)
            f.close()
        dlg.Destroy()
        
    def OnSave(self, event):
        try:
            file = open(self.filename,'w')
        except FileNotFoundError:
            wx.MessageBox("File Not found!",
                      "Save In Undefine File",
                      wx.OK|wx.ICON_WARNING)
        else:
            file.write(self.INTextCrtl.GetValue())
            file.close()

    def OnAbout(self, event):
        wx.MessageBox("This is a TextEditer you can edit your file",
                      "About TextEditer",
                      wx.OK|wx.ICON_INFORMATION)
    
    def OnSaveAs(self, event):
        dlg = wx.DirDialog(None, "Choose a folder", style=wx.DD_DEFAULT_STYLE |
                            wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            if bool(self.filename):
                try:
                    path = os.path.join(self.dirname,self.filename)
                except OSError:
                    wx.MessageBox("No Source!",
                        "Please Open First",
                        wx.OK|wx.ICON_WARNING)
                else:
                    file = open(path, "w")
                    file.write(self.INTextCrtl.GetValue())
                    file.close()
            else:
                wx.MessageBox("No Source!",
                      "Please Open First",
                      wx.OK|wx.ICON_WARNING)
        
    def OnOpenBroad(self, event):
        win = wx.Frame(self, title = "Paste board", size = (410,335))
        
        bkg = wx.Panel(win)
        hbox = wx.BoxSizer()
        
        contents = wx.TextCtrl(bkg, style = wx.TE_MULTILINE | wx.HSCROLL, size = (410,335))
        
        hbox.Add(contents,proportion = 1,
                flag = wx.EXPAND)
        
        bkg.SetSizer(hbox)
        win.Show()
        
class Application(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainWindow()
        self.Frame.Show()
        return True

if __name__ == "__main__":
    app = Application(True, "Debug.log")
    app.MainLoop()
