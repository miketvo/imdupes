from _version import __gui_app_name__, __version__
from tkinter import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry(
            f'{int(self.root.winfo_screenwidth() * 0.75)}x'
            f'{int(self.root.winfo_screenheight() * 0.75)}+'
            f'{int(self.root.winfo_screenwidth() * 0.125)}+'
            f'{int(self.root.winfo_screenheight() * 0.1)}'
        )

        main_frame = Frame(self.root)
        main_frame.pack()

        self.toolbar = self.__init_toolbar__()

        console_frame = Frame(self.root)
        console_frame.pack(side=BOTTOM)

        self.root.title(f'{__gui_app_name__} v{__version__}')
        self.root.wm_iconphoto(False, PhotoImage(file='../../icon.png'))

    def main(self):
        self.root.mainloop()

    def __init_toolbar__(self) -> Frame:
        toolbar_frame = Frame(self.root)
        toolbar_frame.pack(side=TOP, fill='x')

        file_menu_bttn = Menubutton(toolbar_frame, text='File')
        file_menu_bttn.pack(side=LEFT)
        file_menu = Menu(file_menu_bttn, tearoff=0)
        file_menu.add_command(label='Open Folder')
        file_menu.add_command(label='Load Dupfile')
        file_menu.add_command(label='Save Dupfile')
        file_menu.add_command(label='Quit', command=lambda: self.root.destroy())
        file_menu_bttn['menu'] = file_menu

        select_menu_bttn = Menubutton(toolbar_frame, text='Select')
        select_menu_bttn.pack(side=LEFT)
        select_menu = Menu(select_menu_bttn, tearoff=0)
        select_menu.add_command(label='Select All')
        select_menu.add_command(label='Select All (Keep 1st Copy)')
        select_menu.add_command(label='Deselect All')
        select_menu.add_command(label='Invert Selection')
        select_menu_bttn['menu'] = select_menu

        scan_menu_bttn = Menubutton(toolbar_frame, text='Scan')
        scan_menu_bttn.pack(side=LEFT)
        scan_menu = Menu(scan_menu_bttn, tearoff=0)
        scan_menu.add_command(label='Scan')
        scan_menu.add_command(label='Recursive Scan')
        scan_menu.add_command(label='Clear')
        scan_menu_bttn['menu'] = scan_menu

        clean_menu_bttn = Menubutton(toolbar_frame, text='Clean')
        clean_menu_bttn.pack(side=LEFT)
        clean_menu = Menu(clean_menu_bttn, tearoff=0)
        clean_menu.add_command(label='Delete Selected')
        clean_menu.add_command(label='Delete All')
        clean_menu_bttn['menu'] = clean_menu

        view_menu_bttn = Menubutton(toolbar_frame, text='View')
        view_menu_bttn.pack(side=LEFT)
        view_menu = Menu(view_menu_bttn, tearoff=0)
        view_menu.add_checkbutton(label='Console')
        view_menu.add_checkbutton(label='Preview Pane')
        view_menu.add_separator()
        view_menu.add_command(label='Help')
        view_menu_bttn['menu'] = view_menu

        return toolbar_frame
