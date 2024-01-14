from tkinter import (
    Tk,
    StringVar,
    Listbox)
from tkinter.ttk import (
    Label,
    LabelFrame,
    Treeview,
    Button)
from tkinter import filedialog
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations
from filecmp import dircmp
from subprocess import run



def select(f):
    run(f"explorer.exe /select,\"{f}\"")

class App(Tk):
    def __init__(self):
        super().__init__()
        self.paths = set()
        self.paths_v = StringVar()
        self.left_label_v = StringVar()
        self.right_label_v = StringVar()
        self.add_path_btn = Button(self,text="Add Path",command=self.add_path_cmd)
        self.add_path_btn.pack()
        self.paths_listbox = Listbox(self,listvariable=self.paths_v)
        self.paths_listbox.pack(fill="both",expand=True)
        self.pairs_tree = Treeview(self,show="",columns=("left","right"),
                                   displaycolumns=("left","right"))
        self.pairs_tree.pack(fill="both",expand=True)
        self.pairs_tree.bind("<<TreeviewSelect>>",self.pairs_tree_select)
        self.list_tree = Treeview(self,show="",columns=("left","right"),
                                  displaycolumns=("left","right"))
        self.list_tree.pack(fill="both",expand=True)
        self.list_tree.bind("<<TreeviewSelect>>",self.list_tree_select)
        self.left_label = Label(self,textvariable=self.left_label_v)
        self.right_label = Label(self,textvariable=self.right_label_v)
        self.left_label.pack(fill="both",expand=True)
        self.right_label.pack(fill="both",expand=True)
        self.list_tree.bind("<Double-1>",self.list_tree_doubleclick)

    def add_path_cmd(self):
        p = filedialog.askdirectory(mustexist=True)
        if p:
            self.paths.add(p)
        self.paths_listbox_update()

    def paths_listbox_update(self):
        self.paths_v.set(sorted(list(self.paths)))
        if len(self.paths) > 1:
            self.pairs_tree_update()

    def pairs_tree_update(self):
        self.pairs_tree.delete(*self.pairs_tree.get_children())
        for a,b in combinations(self.paths,r=2):
            print("a,b:",a,b)
            self.pairs_tree.insert("","end",values=(a,b))

    def pairs_tree_select(self,event):
        print("self,event:",self,event)
        print(event.widget.item(event.widget.focus(),"values"))
        a,b = event.widget.item(event.widget.focus(),"values")
        print("a,b:",a,b)
        self.left_label_v.set(a)
        self.right_label_v.set(b)
        self.list_tree_update()

    def list_tree_update(self):
        self.list_tree.delete(*self.list_tree.get_children())
        left = self.left_label_v.get()
        right = self.right_label_v.get()
        print("left,right:",left,right)
        dc = dircmp(left,right)
        res = set()
        # for o in dc.common:
            # res.add((o,o))
        for o in dc.left_only:
            res.add((o,""))
        for o in dc.right_only:
            res.add(("",o))
        for a,b in sorted(list(res)):
            self.list_tree.insert("","end",values=(a,b))

    def list_tree_select(self,event):
        print("self,event:",self,event)
        print(event.widget.item(event.widget.focus(),"values"))

    def list_tree_doubleclick(self,event):
        left = self.left_label_v.get()
        right = self.right_label_v.get()
        path_l = Path(left)
        path_r = Path(right)
        a,b = event.widget.item(event.widget.focus(),"values")
        print("a,b:",a,b)
        if a:
            select(path_l/a)
        if b:
            select(path_r/b)




def main():
    app = App()
    args = ArgumentParser()
    args.add_argument("--path",action="append")
    ns = args.parse_args()
    if ns.path:
        for p in ns.path:
            print("p:",p)
            path = Path(p).resolve()
            print("path:",path)
            if path.is_dir():
                print(path,"exists")
                app.paths.add(str(path))
        app.paths_listbox_update()
    app.mainloop()
    
if __name__ == "__main__":
    main()

