import tkinter as tk
from tkinter import filedialog
import os
from file_renamer import FileRenamer


class FileRenamerGUI:

    def __init__(self, window):
        self.fr = FileRenamer()
        # define window
        self._window = window
        self._window.title('File Renamer')
        self._window.config(bg='black')
        self._window.attributes("-alpha", 0.85)
        self._window.geometry('800x510')
        # define elements on window
        # top and bottom
        self._browse_button = tk.Button(window, text='Browse', command=self._browse_folder)
        self._apply_button = tk.Button(window, text='apply')
        # left area
        self._originals_label = tk.Label(window, text='Original')
        self._scrollbar_old = tk.Scrollbar(window)
        self._filebox_old = tk.Listbox(window, yscrollcommand=self._scrollbar_old.set)
        self._scrollbar_old.config(command=self._filebox_old.yview)
        self._radio_namesort = tk.Radiobutton(window, text='sort by name')
        self._radio_datesort = tk.Radiobutton(window, text='sort by date')
        # right area
        self._preview_label = tk.Label(window, text='Preview')
        self._scrollbar_new = tk.Scrollbar(window)
        self._filebox_new = tk.Listbox(window, yscrollcommand=self._scrollbar_new.set)
        self._scrollbar_new.config(command=self._filebox_new.yview)
        self._radio_override = tk.Radiobutton(window, text='override')
        self._radio_copy = tk.Radiobutton(window, text='make copy')
        # middle area
        self._format_label = tk.Label(window, text='Format')
        self._prefix_label = tk.Label(window, text='Prefix:')
        self._prefix_entry = tk.Entry(window)
        self._startnumber_label = tk.Label(window, text='Start with:')
        self._startnumber_entry = tk.Entry(window)
        self._digitnumber_label = tk.Label(window, text='Digits:')
        self._digitnumber_spinbox = tk.Spinbox(window, from_=1, to=10)
        # configure style and place elements on window
        self._make_layout()

    def _make_layout(self):
        """
        Configure style and place elements on window.
        """
        # left area
        self._originals_label.config(font='Helvetica 12 bold', bg='grey', activebackground='grey')
        self._originals_label.place(x=10, y=50, width=220, height=50)
        self._scrollbar_old.place(x=210, y=110, height=310)
        self._filebox_old.place(x=10, y=110, width=200, height=310)
        self._radio_datesort.config(bg='black', activebackground='black', fg='white', relief=tk.RAISED)
        self._radio_namesort.config(bg='black', activebackground='black', fg='white', relief=tk.RAISED)
        self._radio_datesort.place(x=10, y=430, width=110, height=30)
        self._radio_namesort.place(x=120, y=430, width=110, height=30)
        # right area
        self._preview_label.config(font='Helvetica 12 bold', bg='grey', activebackground='grey')
        self._preview_label.place(x=570, y=50, width=220, height=50)
        self._scrollbar_new.place(x=770, y=110, height=310)
        self._filebox_new.place(x=570, y=110, width=200, height=310)
        self._radio_override.config(bg='black', activebackground='black', fg='white', relief=tk.RAISED)
        self._radio_copy.config(bg='black', activebackground='black', fg='white', relief=tk.RAISED)
        self._radio_override.place(x=570, y=430, width=110, height=30)
        self._radio_copy.place(x=680, y=430, width=110, height=30)
        # middle area
        self._format_label.config(font='Helvetica 12 bold', bg='grey', activebackground='grey')
        self._format_label.place(x=300, y=50, width=220, height=50)
        self._prefix_label.config(font='Helvetica 12', bg='black', activebackground='black', fg='white')
        self._prefix_label.place(x=300, y=200)
        self._prefix_entry.config(font='Helvetica 12')
        self._prefix_entry.place(x=375, y=200, width=150, height=20)
        self._startnumber_label.config(font='Helvetica 12', bg='black', activebackground='black', fg='white')
        self._startnumber_label.place(x=300, y=240)
        self._startnumber_entry.config(font='Helvetica 12')
        self._startnumber_entry.place(x=375, y=240, width=150, height=20)
        self._digitnumber_label.config(font='Helvetica 12', bg='black', activebackground='black', fg='white')
        self._digitnumber_label.place(x=300, y=280)
        self._digitnumber_spinbox.config(font='Helvetica 12')
        self._digitnumber_spinbox.place(x=375, y=280, width=150, height=20)
        # top and bottom
        self._browse_button.config(font='Helvetica 11', bg='orange', activebackground='orange')
        self._apply_button.config(font='Helvetica 12 bold', bg='green', activebackground='green')
        self._browse_button.place(x=10, y=10, width=780, height=30)
        self._apply_button.place(x=10, y=470, width=780, height=30)

    def _browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.fr._path = path
            self._browse_button.config(text=path)
            file_list = os.listdir(path)
            self._filebox_old.delete(0, tk.END)
            for item in file_list:
                self._filebox_old.insert(tk.END, item)


if __name__ == "__main__":
    root = tk.Tk()
    fr = FileRenamerGUI(root)
    root.mainloop()
