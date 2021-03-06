import platform
import sys

try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.simpledialog import askstring
    from tkinter.scrolledtext import ScrolledText
except Exception as err:
    print(" ERROR: unable to find required Python module «tkinter» \n", err)
    sys.exit(1)


from vntree import Node, TreeAttr



def vn_uri_to_id(ss):
    _hash = hashlib.md5(ss.encode()).hexdigest()
    return _hash


class tkNode(Node):
    TV = TreeAttr("_treemeta")
    node_count = TreeAttr("_treemeta", initial=0)

    def __init__(self, name=None, parent=None, data=None, treedict=None, TV=None):
        print("NEW NODE parent=", parent)
        super().__init__(name, parent, data, treedict)
        print("self.node_count=",self.node_count)
        self._nodeid="N_"+str(self.node_count)
        self.node_count += 1
        print("self.data=",self.data)
        if TV:
            self.TV = TV
        if parent is None:
            self.add_child(self)



    def add_child(self, node):
        """Add a child node to the current node instance.

        :param node: the child node instance.
        :type node: Node
        :returns: The new child node instance.   
        :rtype: Node 
        """
        if self is node:
            parent_id = ""
            _nodeid="N_"+str(0)
        else:
            if not issubclass(node.__class__, Node):
                raise TypeError("{}.add_child: arg «node»=«{}», type {} not valid.".format(self.__class__.__name__, node, type(node)))
            self.childs.append(node)
            node.parent = self
            parent_id = self.TV.selection()[0]
            _nodeid="N_"+str(self.node_count)
        # parent = self.rootnode.get_node_by_id(parent_id)
        # if parent is None:
        #     return None

        # print("self.TV.insert node._nodeid", node._nodeid)
        # print("self.TV.insert node.data", node.data)
        
        self.TV.insert(parent_id, 'end', _nodeid, text=node.name)

        # parent_id = self.TreeView.selection()[0]
        # node_name = askstring("New Child", prompt="Enter the node name", initialvalue="")
        # if not node_name:
        #     node_name = "no-name-node"
        # # self.TV.insert(item, 'end', 'LC_'+str(self.TVleafref), 
        # #   text='Load case '+str(self.TVleafref))
        # #self.node_count += 1
        
        # self.TreeView.insert(parent_id, 'end', self._nodeid, text=self.name)

        return node  

# class DataEditor(Frame):
#     def __init__(self, parent):
#         Frame.__init__(self, parent)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(0, weight=1)
        
#         canvas = Canvas(self, bg="yellow", bd=10)
#         nrows = 1000
#         ncols = 50
#         wid = 80
#         hei = 20
        
#         ys = 0
#         for ii in range(nrows):
#             xs = 0
#             for jj in range(ncols):
#                 canvas.create_rectangle(xs, ys, xs+wid, ys+hei, 
#                 outline="#fb0", fill="#fff")
#                 xs = xs + wid
#             ys = ys + hei
            
#         canvas.grid(sticky=(N,W,E,S))   # column=0, row=0, 



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PyText(ScrolledText):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=YES, fill=BOTH)

        if platform.system() == 'Windows':
            font = ('Courier New',10)
        else:
            font = 'monospace 10'  # "{Lucida Sans Typewriter} 12"

        # self.cfg = dict(borderwidth=0,
        #     font=font,
        #     foreground="black",
        #     background="green",
        #     insertbackground="yellow", 
        #     selectforeground="blue", 
        #     selectbackground="#008000",
        #     wrap=WORD, 
        #     width=64,
        #     undo=True)
        self.configure(borderwidth=0,
            font=font,
            foreground="black",
            background="green",
            insertbackground="yellow", 
            selectforeground="blue", 
            selectbackground="#008000",
            wrap=WORD, 
            width=64,
            undo=True)

###############################################################################
class TextViewFrame(Frame):

    def __init__(self, parent=None, text='', editfile=None, cfg=None):
        #Frame.__init__(self, parent, wid)
        super().__init__(parent)
        self.parent = parent
        self.pack(expand=YES, fill=BOTH)
        #self.modified = property(self.text.edit_modified, self.text.edit_modified)
        #self.modified = False
        self.editfile = editfile
        #self.editfile= StringVar()
        #self.editfile.trace("w", self.onEditfileChange)
        #self.master_title = self.winfo_toplevel().title()

        self.ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance

        if platform.system() == 'Windows':
            font = ('Courier New',10)
        else:
            font = 'monospace 10'  # "{Lucida Sans Typewriter} 12"

        if cfg:
            self.cfg = cfg
        else:
            self.cfg = dict(borderwidth=0,
                font=font,
                foreground="white",
                background="black",
                insertbackground="yellow", 
                selectforeground="green", 
                selectbackground="#008000",
                wrap=WORD, 
                width=64,
                undo=True)
        #self.makeView()
        self.text = ScrolledText(self, relief=SUNKEN, wrap=WORD)
        
        #self.master.pack(side=LEFT, expand=YES, fill=BOTH)
        #self.pack(side=LEFT, expand=YES, fill=BOTH)
        #self.text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text.pack(expand=YES, fill=BOTH)

        # self.text.grid(column=0, row=0, sticky=(N,W,E,S))
        # self.text.master.grid_columnconfigure(0, weight=1)
        # self.text.master.grid_rowconfigure(0, weight=1)

        self.text.config(**self.cfg)
        if editfile:
            """self.document = TextDocument(editfile)
            self.text.insert('1.0', self.document.fetch())
            self.text.edit_modified(False)
            self.messageDispatch("Editing file {}".format(self.document.filename))"""
            self.onOpen(editfile=editfile)
        else:
            self.document = None
            self.text.insert('1.0', text)
        self.text.focus_set()
        
        ##self.bind("<Control-y>", self.onRedo) 

    def makeView(self):
        vsbar = Scrollbar(self)
        self.text = Text(self, relief=SUNKEN, wrap=WORD)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)
        vsbar['command'] = self.text.yview
        self.text['yscrollcommand'] = vsbar.set
        vsbar.pack(side=RIGHT, fill=Y, before=self.text)   # , expand=YES

    

    def onNew(self, *evt):
        if self.text.edit_modified():
            self.messageDispatch("WARNING Buffer edited: Save or Discard first")
            return
        self.text.delete('1.0', END)
        self.text.edit_modified(False)
        self.text.edit_reset()
        self.editfile = ""
        #self.editfile.set("")

    def onOpen(self, event=None, editfile=None):
        if self.text.edit_modified():
            self.messageDispatch("WARNING Buffer edited: Save or Discard first")
            return
        if not editfile:
            editfile = tkFileDialog.askopenfilename(filetypes=self.ftypes)
        if editfile and os.path.isfile(editfile):
            self.document = TextDocument(editfile)
            self.text.insert('1.0', self.document.fetch())
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.messageDispatch("Editing file {}".format(self.document.filename))
        else:
            self.messageDispatch("WARNING Cannot open file {}".format(editfile))
            

    def onSave(self, *evt):
        if self.document:
            self.document.save( self.text.get('1.0', END) )  # END+'-1c'
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.messageDispatch("INFO Saving file {}".format(self.document.filename))
        else:
            self.onSaveAs()

    def onSaveAs(self):
        editfile = tkFileDialog.asksaveasfilename(filetypes=self.ftypes)
        if editfile:
            self.document = TextDocument(editfile, maycreatenew=True)
            self.onSave()
        else:
            self.messageDispatch("WARNING onSaveAs data not saved".format())

    def messageDispatch(self, message):
        self.parent.messageDispatch(message)

    """def onEditfileChange(self, *event):
        if self.editfile.get():
            new_title = "Editing : " + os.path.basename(self.editfile.get())
        else:
            new_title = self.master_title
        self.winfo_toplevel().title(new_title)"""
    
    #--------------------------------------------------------------------------
    def onUndo(self, event=None):
        try:
            self.text.edit_undo()
        except TclError:
            self.messageDispatch("INFO no edits to undo".format())

    def onRedo(self, event=None):
        try:
            self.text.edit_redo()
        except TclError:
            self.messageDispatch("INFO no edits to redo".format())

    def onCut(self, event=None):
        if not self.text.tag_ranges(SEL):
            self.messageDispatch("WARNING No text selected".format())
        else:
            self.onCopy()
            self.onDelete()

    def onCopy(self, event=None):
        if not self.text.tag_ranges(SEL):
            self.messageDispatch("No text selected".format())
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onPaste(self, event=None):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            self.messageDispatch("Nothing to paste".format())
            return
        self.text.insert(INSERT, text)
        self.text.tag_remove(SEL, '1.0', END)
        self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.text.see(INSERT)                  

    def onDelete(self, event=None):
        if not self.text.tag_ranges(SEL):
            self.messageDispatch("No text selected".format())
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    #--------------------------------------------------------------------------

###############################################################################
###############################################################################
class StatusBarFrame(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(fill=X)   # expand=YES, 
        self.sizegrip = Sizegrip(self)
        self.sizegrip.pack(side=RIGHT, anchor=E)
        self.messagetext = StringVar()   # will vanish when variable goes out of scope, so make it an instance attribute
        self.message = Label(self, relief=SUNKEN, textvariable=self.messagetext, anchor=W)  # 
        self.message.pack(fill=X, side=LEFT, expand=YES)   # , expand=YES
        self.messagetext.set('Starting basic text editor....')
        
    def clear(self):
        self.messagetext.set('')
        

    """def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()"""
################################################################################

class MainApp(Frame):
    def __init__(self, master, name="no-name", add_Sizegrip=True):
        Frame.__init__(self, master, name=name)
        #self.master = master
        
        self.height = 500
        self.width = 700
        master.geometry('%dx%d+300+300' % (self.width, self.height))
        ##self.master.minsize(width, height)
        master.title(name)

        menubar = Menu(self, name="menubar")
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_file.add_command(label='New', command=self.onNew)
        menu_file.add_command(label='Open...', command=self.onNew)
        menu_file.add_command(label='Close', command=self.onNew)
        master.config(menu=menubar)

        # add Panedwindow
        self.PW = Panedwindow(master, orient=HORIZONTAL)
        self.PW.f1 = Frame(self.PW, borderwidth=1, relief="sunken",
                     width=150)
        self.PW.f2 = Frame(self.PW); # second pane    
        self.PW.add(self.PW.f1)
        self.PW.add(self.PW.f2)
        self.PW.grid(column=0, row=0, sticky=(N,W,E,S))
        
        # add Notebook
        self.NB = Notebook(self.PW.f2)
        self.NB.add(TextViewFrame(self.NB, "tree builder"), text='>>>')
        self.NB.add(PyText(self.NB), text='Sheet_2')
        # self.NB.add(DataEditor(self.NB), text='Sheet_3')
        # self.NB.add(DataEditor(self.NB), text='Sheet_4')
        # self.NB.add(DataEditor(self.NB), text='Sheet_5')
        #self.NB.add(ttk.Frame(self.NB), text='Sheet_2')
        # self.NB.grid(column=0, row=0, sticky=(N,W,E,S))
        # self.NB.master.grid_columnconfigure(1, weight=1)
        # self.NB.master.grid_rowconfigure(0, weight=1)
        self.NB.pack(expand=YES, fill=BOTH)
        
        # add Treeview
        self.TV_id_count = 0
        self.TV = Treeview(self.PW.f1)
        self.rootnode = tkNode("root-node", TV=self.TV)
        #self.TV.insert('', 'end', self.rootnode._nodeid, text=self.rootnode.name)
        self.TV.grid(column=0, row=0, sticky='nsew')
        self.TV.master.grid_columnconfigure(0, weight=1)
        self.TV.master.grid_rowconfigure(0, weight=1)
        
        # tree pop-up
        #self.treePopupMenu(self.TV)
        self.TPM = Menu(self.TV, tearoff=0)
        self.TPM.add_command(label="add child", command=self.onAddChild)
        self.TPM.add_command(label="edit name", command=self.onNodeNameEdit)
        self.TPM.add_command(label="close menu", command=lambda *args: None) #, command=self.onTPMClose)
        self.TV.bind("<Button-3>", self.showTreePopupMenu)



        if add_Sizegrip:
            Sizegrip(master).grid(column=0, row=1, sticky=(S,E))

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        print(master.children)

    # def treePopupMenu(self, parent):
    #     self.TPM = Menu(parent, tearoff=0)
    #     self.TPM.add_command(label="add child", command=self.onAddLeaf)
    #     self.TPM.add_command(label="edit name", command=self.onNodeNameEdit)
    #     self.TPM.add_command(label="close menu", command=self.onContextMenuClose)
    #     parent.bind("<Button-3>", self.showTreePopupMenu)
        
    def showTreePopupMenu(self, evt):
        self.TPM.post(evt.x_root, evt.y_root)
        # print(evt, evt.widget)



    def onNodeNameEdit(self):
        item = self.TV.selection()[0]
        node_name = askstring("New Child", prompt="Enter the node name", initialvalue="")
        if not node_name:
            return False
        #self.TV.set(item, column=0, value=node_name)
        # https://stackoverflow.com/questions/18562123/how-to-make-ttk-treeviews-rows-editable
        current_name = self.TV.item(item , option="text")
        print("node ", item, "current_name =", current_name )
        self.TV.item(item , text=node_name)
        #item.text = node_name


    def onAddChild(self):

        parent_id = self.TV.selection()[0]
        parent = self.rootnode.get_node_by_id(parent_id)
        print("parent_id=",parent_id)
        print("self.rootnode.data=",self.rootnode.data)
        print("found parent:", parent.name)
        if parent is None:
            return None
        node_name = askstring("New Child", prompt="Enter the node name", initialvalue="")
        if not node_name:
            node_name = "no-name-node"
        newnode = tkNode(node_name, parent)
        #parent.add_child()
        #self.TV.insert(parent_id, 'end', newnode._nodeid, text=newnode.name)      

    def onTPMClose(self):
        # self.TPM.destroy()
        # self.TPM = None
        # self.TPM.hide()  # AttributeError: 'Menu' object has no attribute 'hide'
        pass

    def onAddSheet(self):
        self.NB.add(Frame(self.NB), text='dummy name')    

    def onExit(self):
        self.quit()  # self needs to be a frame

    def onNew(self, *evt):
        pass





def main():
    root = Tk()
    root.option_add('*tearOff', FALSE) # https://tkdocs.com/tutorial/menus.html
    #print("System: ", root.tk.call('tk', 'windowingsystem') )
    style = Style()
    style.theme_use('clam')
    app = MainApp(root, 'vntree-ui')
    root.mainloop() 

if __name__ == "__main__":
    main()

