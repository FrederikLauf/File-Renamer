import tkinter as tk
from tkinter import filedialog
import os
import re
from file_renamer import FileRenamer


class FileRenamerGUI:

    def __init__(self, window):

        self._window = window
        self.fr = FileRenamer()
        # entry and selection states
        self._sortchoice_var = tk.IntVar()
        self._writechoice_var = tk.IntVar()
        self._startnumber_var = tk.StringVar()
        self._startnumber_var.set(self.fr._namepattern["startnum"])
        self._startnumber_var.trace("w", self._set_startnumber)
        self._prefix_var = tk.StringVar()
        self._prefix_var.set(self.fr._namepattern["prefix"])
        self._prefix_var.trace("w", self._set_prefix)
        self._digits_var = tk.StringVar()
        self._digits_var.set(self.fr._namepattern["digits"])
        self._digits_var.trace("w", self._set_digits)
        # define elements on window
        # top and bottom
        self._browse_button = tk.Button(window, text='Browse', command=self._browse_folder)
        self._apply_button = tk.Button(window, text='apply')
        # left area
        self._originals_label = tk.Label(window, text='Original')
        self._scrollbar_old = tk.Scrollbar(window)
        self._filebox_old = tk.Listbox(window, yscrollcommand=self._scrollbar_old.set)
        self._scrollbar_old.config(command=self._filebox_old.yview)
        self._radio_namesort = tk.Radiobutton(window, text='sort by name',
                                              variable=self._sortchoice_var,
                                              value=1, command=self._choose_sorting)
        self._radio_namesort.select()
        self._radio_datesort = tk.Radiobutton(window, text='sort by date',
                                              variable=self._sortchoice_var,
                                              value=2, command=self._choose_sorting)
        # right area
        self._preview_label = tk.Label(window, text='Preview')
        self._scrollbar_new = tk.Scrollbar(window)
        self._filebox_new = tk.Listbox(window, yscrollcommand=self._scrollbar_new.set)
        self._scrollbar_new.config(command=self._filebox_new.yview)
        self._radio_override = tk.Radiobutton(window, text='override', variable=self._writechoice_var, value=1)
        self._radio_override.select()
        self._radio_copy = tk.Radiobutton(window, text='make copy', variable=self._writechoice_var, value=2)
        # middle area
        self._format_label = tk.Label(window, text='Format')
        self._prefix_label = tk.Label(window, text='Prefix:')
        self._prefix_entry = tk.Entry(window, textvariable=self._prefix_var)
        self._startnumber_label = tk.Label(window, text='Start with:')
        self._startnumber_entry = tk.Entry(window, textvariable=self._startnumber_var)
        self._digitnumber_label = tk.Label(window, text='Digits:')
        self._digitnumber_spinbox = tk.Spinbox(window, from_=self.fr._namepattern["digits"], to=9,
                                               textvariable=self._digits_var)
        # configure style and place elements on window
        self._make_layout()

    def _make_layout(self):
        """
        Configure style and place elements on window.
        """
        self._window.title('File Renamer')
        self._window.config(bg='black')
        self._window.attributes("-alpha", 0.85)
        self._window.geometry('800x510')
        # left area
        self._originals_label.config(font='Helvetica 12 bold', bg='grey', activebackground='grey')
        self._originals_label.place(x=10, y=50, width=220, height=50)
        self._scrollbar_old.place(x=210, y=110, height=310)
        self._filebox_old.place(x=10, y=110, width=200, height=310)
        self._radio_datesort.config(bg='black', activebackground='black',
                                    fg='white', selectcolor='black', relief=tk.RAISED)
        self._radio_namesort.config(bg='black', activebackground='black',
                                    fg='white', selectcolor='black', relief=tk.RAISED)
        self._radio_namesort.place(x=10, y=430, width=110, height=30)
        self._radio_datesort.place(x=120, y=430, width=110, height=30)
        # right area
        self._preview_label.config(font='Helvetica 12 bold', bg='grey', activebackground='grey')
        self._preview_label.place(x=570, y=50, width=220, height=50)
        self._scrollbar_new.place(x=770, y=110, height=310)
        self._filebox_new.place(x=570, y=110, width=200, height=310)
        self._radio_override.config(bg='black', activebackground='black',
                                    fg='white', selectcolor='black', relief=tk.RAISED)
        self._radio_copy.config(bg='black', activebackground='black',
                                fg='white', selectcolor='black', relief=tk.RAISED)
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

    # -------methods invoked by GUI actions------------------------------------

    def _browse_folder(self):
        """
        Let user select a folder and display file content in list box.
        """
        path = filedialog.askdirectory()
        if path:
            self.fr._basepath = path
            self._browse_button.config(text=path)
            self.fr._file_list = self.fr._make_list_of_files()

            default_prefix = self.fr._get_default_prefix()
            self.fr._namepattern["prefix"] = default_prefix
            self._prefix_var.set(default_prefix)

            self.fr._namepattern["startnum"] = "1"
            self._startnumber_var.set("1")

            digits = len(str(len(self.fr._file_list)))
            self.fr._namepattern["digits"] = digits
            self._digits_var.set(digits)
            self._digitnumber_spinbox.config(from_=digits)

            self._show_originals()

    def _choose_sorting(self):
        """
        Sort internal file list according to choice and update display.
        """
        if self._sortchoice_var.get() == 1:
            self.fr._sort_by_name()
            print("sorted by name")
        else:
            self.fr._sort_by_date()
            print("sorted by date")
        self._show_originals()

    def _show_originals(self):
        """
        Show or update list of original file names with dates in list box.
        """
        print("Updating")
        self._filebox_old.delete(0, tk.END)
        for item in self.fr._file_list:
            self._filebox_old.insert(tk.END, item)

    def _set_startnumber(self, *args):
        current_entry = self._startnumber_var.get()
        if re.match(r"^\d+$", current_entry):
            start = str(int(current_entry))
            max_num = int(current_entry) + len(self.fr._file_list) - 1
            min_digits = len(str(max_num))
        elif current_entry == "":
            start = "1"
            min_digits = len(str(len(self.fr._file_list)))
        else:
            start = "1"
            self._startnumber_var.set("1")
            min_digits = len(str(len(self.fr._file_list)))
        self.fr._namepattern["startnum"] = start
        self._digitnumber_spinbox.config(from_=min_digits)
        self._digits_var.set(str(min_digits))

    def _set_prefix(self, *args):
        self.fr._namepattern["prefix"] = self._prefix_var.get()

    def _set_digits(self, *args):
        digits = self._digits_var.get()
        max_num = int(self.fr._namepattern["startnum"]) + len(self.fr._file_list) - 1
        min_digits = len(str(max_num))
        if re.match(r"^\d+$", digits) and int(digits) >= min_digits:
            digits = str(int(digits))
        else:
            digits = str(min_digits)
            self._digits_var.set(digits)
            self._digitnumber_spinbox.config(from_=min_digits)
        self.fr._namepattern["digits"] = digits


if __name__ == "__main__":
    root = tk.Tk()
    frg = FileRenamerGUI(root)
    root.mainloop()
