import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import file_renamer
import datetime
import logging
import os
import re
import shutil


class FileRenamerGUI:

    def __init__(self, window):
        """
        Initialisation of window elements and variables
        """
        self._window = window
        self.fr = file_renamer.FileRenamer()

        # window variables
        self._sortchoice_var = tk.IntVar()
        self._timeoffset_identifier_var = tk.StringVar()
        self._timeoffset_identifier_var.trace("w", self._timeoffset_entered)
        self._timeoffset_seconds_var = tk.StringVar()
        self._timeoffset_seconds_var.trace("w", self._timeoffset_entered)
        self._writechoice_var = tk.IntVar()
        self._writechoice_var.trace("w", self._set_writechoice)
        self._startnumber_var = tk.StringVar()
        self._startnumber_var.set(self.fr._namepattern["startnum"])
        self._startnumber_var.trace("w", self._startnumber_entered)
        self._prefix_var = tk.StringVar()
        self._prefix_var.set(self.fr._namepattern["prefix"])
        self._prefix_var.trace("w", self._prefix_entered)
        self._digits_var = tk.StringVar()
        self._digits_var.set(self.fr._namepattern["digits"])
        self._digits_var.trace("w", self._digits_selected)
        self._progress_var = tk.IntVar()

        # define elements on window
        # top and bottom
        self._browse_button = tk.Button(window, text='browse', command=self._browse_button_clicked)
        self._apply_button = tk.Button(window, text='apply', command=self._apply_button_clicked)
        # left area
        self._label_originals = tk.Label(window, text='original')
        self._scrollbar_originals = tk.Scrollbar(window)
        self._filebox_originals = tk.Listbox(window, yscrollcommand=self._scrollbar_originals.set)
        self._scrollbar_originals.config(command=self._filebox_originals.yview)
        self._radio_namesort = tk.Radiobutton(window, text='sort by name',
                                              variable=self._sortchoice_var,
                                              value=1, command=self._sorting_radio_selected)
        self._radio_namesort.select()
        self._radio_datesort = tk.Radiobutton(window, text='sort by date',
                                              variable=self._sortchoice_var,
                                              value=2, command=self._sorting_radio_selected)
        self._timeoffset_identifier_label = tk.Label(window, text='offset tag')
        self._timeoffset_identifier_entry = tk.Entry(window, textvariable=self._timeoffset_identifier_var)
        self._timeoffset_seconds_label = tk.Label(window, text='offset seconds')
        self._timeoffset_seconds_entry = tk.Entry(window, textvariable=self._timeoffset_seconds_var)
        # right area
        self._label_preview = tk.Label(window, text='Preview')
        self._scrollbar_preview = tk.Scrollbar(window)
        self._filebox_preview = tk.Listbox(window, yscrollcommand=self._scrollbar_preview.set)
        self._scrollbar_preview.config(command=self._filebox_preview.yview)
        self._radio_override = tk.Radiobutton(window, text='override', variable=self._writechoice_var, value=1)
        self._radio_copy = tk.Radiobutton(window, text='make copy', variable=self._writechoice_var, value=2)
        self._radio_copy.select()
        # middle area
        self._format_label = tk.Label(window, text='Format')
        self._prefix_label = tk.Label(window, text='Prefix:')
        self._prefix_entry = tk.Entry(window, textvariable=self._prefix_var)
        self._startnumber_label = tk.Label(window, text='Start:')
        self._startnumber_entry = tk.Entry(window, textvariable=self._startnumber_var)
        self._digitnumber_label = tk.Label(window, text='Digits:')
        self._digitnumber_spinbox = tk.Spinbox(window, from_=self.fr._namepattern["digits"], to=9,
                                               textvariable=self._digits_var)
        self._progress_bar = ttk.Progressbar(window, orient="horizontal", mode="determinate")

        # configure style and place elements on window
        self._make_layout()

    def _make_layout(self):
        """
        Configure style and location of window elements
        """
        self._window.title('File Renamer')
        self._window.config(bg='black')
        # self._window.attributes("-alpha", 0.85)
        self._window.geometry('760x510')
        # left area
        self._label_originals.config(font='Helvetica 12 bold', bg='grey')
        self._label_originals.place(x=10, y=50, width=220, height=50)
        self._scrollbar_originals.place(x=210, y=110, height=310)
        self._filebox_originals.place(x=10, y=110, width=200, height=310)
        self._radio_datesort.config(font='Calibri 10', bg='black', fg='white',
                                    selectcolor='black', relief=tk.RAISED)
        self._radio_namesort.config(font='Calibri 10', bg='black', fg='white',
                                    selectcolor='black', relief=tk.RAISED)
        self._radio_namesort.place(x=10, y=430, width=110, height=30)
        self._radio_datesort.place(x=120, y=430, width=110, height=30)
        self._timeoffset_identifier_label.config(font='Calibri 10', bg='black', fg='white')
        self._timeoffset_identifier_label.place(x=230, y=430, width=60, height=30)
        self._timeoffset_identifier_entry.place(x=290, y=430, width=30, height=30)
        self._timeoffset_seconds_label.config(font='Calibri 10', bg='black', fg='white')
        self._timeoffset_seconds_label.place(x=320, y=430, width=85, height=30)
        self._timeoffset_seconds_entry.place(x=405, y=430, width=20, height=30)
        # right area
        x0 = 530
        self._label_preview.config(font='Helvetica 12 bold', bg='grey')
        self._label_preview.place(x=x0, y=50, width=220, height=50)
        self._scrollbar_preview.place(x=x0 + 200, y=110, height=310)
        self._filebox_preview.place(x=x0, y=110, width=200, height=310)
        self._radio_override.config(font='Calibri 10', bg='black', fg='white', selectcolor='black', relief=tk.RAISED)
        self._radio_copy.config(font='Calibri 10', bg='black', fg='white', selectcolor='black', relief=tk.RAISED)
        self._radio_override.place(x=x0 + 110, y=430, width=110, height=30)
        self._radio_copy.place(x=x0, y=430, width=110, height=30)
        # middle area
        x0 = 270
        y1 = 160
        self._format_label.config(font='Helvetica 12 bold', bg='grey')
        self._format_label.place(x=x0, y=50, width=220, height=50)
        self._prefix_label.config(font='Helvetica 12', bg='black', fg='white')
        self._prefix_label.place(x=x0, y=y1)
        self._prefix_entry.config(font='Helvetica 12')
        self._prefix_entry.place(x=x0 + 75, y=y1, width=140, height=20)
        self._startnumber_label.config(font='Helvetica 12', bg='black', fg='white')
        self._startnumber_label.place(x=x0, y=y1 + 40)
        self._startnumber_entry.config(font='Helvetica 12')
        self._startnumber_entry.place(x=x0 + 75, y=y1 + 40, width=140, height=20)
        self._digitnumber_label.config(font='Helvetica 12', bg='black', fg='white')
        self._digitnumber_label.place(x=x0, y=y1 + 2 * 40)
        self._digitnumber_spinbox.config(font='Helvetica 12')
        self._digitnumber_spinbox.place(x=x0 + 75, y=y1 + 2 * 40, width=140, height=20)
        self._progress_bar.place(x=x0 + 75, y=y1 + 120, width=140)
        # top and bottom
        self._browse_button.config(font='Helvetica 11', bg='orange', activebackground='orange')
        self._apply_button.config(font='Helvetica 12 bold', bg='green', activebackground='green')
        self._browse_button.place(x=10, y=10, width=740, height=30)
        self._apply_button.place(x=10, y=470, width=740, height=30)

    # -------methods invoked by GUI actions------------------------------------

    def _browse_button_clicked(self):
        """
        Let user select a folder and display file content in list box.
        """
        self._apply_button.config(text="apply")
        path = filedialog.askdirectory()
        if path:
            self.fr._basepath = path
            self._browse_button.config(text=path)
            self.fr._file_list = self.fr._make_list_of_files()

            self._progress_bar.config(maximum=len(self.fr._file_list))

            # default_prefix = self.fr._get_default_prefix()
            # self.fr._namepattern["prefix"] = default_prefix
            # self._prefix_var.set(default_prefix)

            # self.fr._namepattern["startnum"] = "1"
            # self._startnumber_var.set("1")

            digits = len(str(len(self.fr._file_list)))
            self.fr._namepattern["digits"] = digits
            self._digits_var.set(digits)
            self._digitnumber_spinbox.config(from_=digits)

            self._show_originals()

            self.fr._new_names = self.fr._make_new_names()
            self._show_preview()

    def _sorting_radio_selected(self):
        """
        Sort internal file list according to choice and update display.
        """
        if self._sortchoice_var.get() == 1:
            self.fr._sort_by_name()
        else:
            self.fr._sort_by_date()
        self._show_originals()
        self.fr._new_names = self.fr._make_new_names()
        self._show_preview()

    def _show_originals(self):
        """
        Show or update list of original file names with dates in list box.
        """
        self._filebox_originals.delete(0, tk.END)
        for item in self.fr._file_list:
            self._filebox_originals.insert(tk.END, item)

    def _show_preview(self):
        self._filebox_preview.delete(0, tk.END)
        for item in self.fr._new_names:
            self._filebox_preview.insert(tk.END, item)
        self._apply_button.config(text="apply")

    def _startnumber_entered(self, *args):
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

        self.fr._new_names = self.fr._make_new_names()
        self._show_preview()

    def _timeoffset_entered(self, *args):
        current_entry_seconds = self._timeoffset_seconds_var.get()
        current_entry_identifier = self._timeoffset_identifier_var.get()
        if current_entry_identifier == '':
            current_entry_identifier = None
        if re.match(r"^-?\d+$", current_entry_seconds):
            seconds = int(current_entry_seconds)
        elif current_entry_seconds == '-':
            seconds = 0
        elif current_entry_seconds == "":
            seconds = 0
        else:
            seconds = 0
            self._timeoffset_seconds_var.set("0")
        self.fr._time_offsets = [{'identifier': current_entry_identifier, 'seconds': seconds}]
        self._sorting_radio_selected()

    def _prefix_entered(self, *args):
        self.fr._namepattern["prefix"] = self._prefix_var.get()
        self.fr._new_names = self.fr._make_new_names()
        self._show_preview()

    def _digits_selected(self, *args):
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
        self.fr._new_names = self.fr._make_new_names()
        self._show_preview()

    def _set_writechoice(self, *args):
        self._apply_button.config(text="apply")

    def _apply_button_clicked(self):
        if self._writechoice_var.get() == 1:
            self.fr._rename_override()
            self.fr._file_list = self.fr._make_list_of_files()
            self._show_originals()
        else:
            self._rename_copy()
        self._apply_button.config(text="Success! Close window, or continue browsing and renaming.")

    def _rename_copy(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_folder = os.path.join(self.fr._basepath, "renamed_files_" + time)
        os.mkdir(new_folder)
        for i, (old, new) in enumerate(zip(self.fr._file_list, self.fr._new_names)):
            try:
                old_path = os.path.join(self.fr._basepath, old[0])
                new_path = os.path.join(new_folder, new)
                shutil.copy2(old_path, new_path)
            except Exception as err:
                print("An Error occurred:", err)


if __name__ == "__main__":
    root = tk.Tk()
    frg = FileRenamerGUI(root)
    root.mainloop()
