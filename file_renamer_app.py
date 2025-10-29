import datetime
import os
import re
import shutil

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from file_renamer.file_renamer import FileRenamer


class FileRenamerGUI:

    def __init__(self, window):
        """
        Initialisation of variables and window elements
        """
        self._window = window
        self.fr = FileRenamer()

        # variables
        self._sortchoice_var = tk.IntVar()
        self._sortchoice_var.set(1)
        self._sortchoice_var.trace("w", self._sorting_radio_selected)        
        
        self._timeoffset_identifier_var = tk.StringVar()
        self._timeoffset_identifier_var.trace("w", self._timeoffset_entered)
        
        self._timeoffset_seconds_var = tk.StringVar()
        self._timeoffset_seconds_var.trace("w", self._timeoffset_entered)
        
        self._startnumber_var = tk.StringVar()
        self._startnumber_var.set(self.fr._namepattern["startnum"])
        self._startnumber_var.trace("w", self._startnumber_entered)
        
        self._prefix_var = tk.StringVar()
        self._prefix_var.set(self.fr._namepattern["prefix"])
        self._prefix_var.trace("w", self._prefix_entered)
        
        self._digits_var = tk.StringVar()
        self._digits_var.set(self.fr._namepattern["digits"])
        self._digits_var.trace("w", self._digits_selected)
        
        self._homonymity_var = tk.IntVar()
        self._homonymity_var.set(1 if self.fr._preserve_homonymity is True else 2)
        self._homonymity_var.trace("w", self._homonymity_radio_selected)
        
        self._progress_var = tk.IntVar()
        
        # window elements
        self._make_window_elements()

    def _make_window_elements(self):
        """
        Configure style and location of window elements
        """
        self._window.title('File Renamer')

        top_frame = tk.Frame(self._window)
        browse_button_frame = tk.Frame(top_frame)
        self._browse_button = tk.Button(browse_button_frame, text='browse', command=self._browse_button_clicked)
        self._browse_button.pack(fill=tk.X)
        browse_button_frame.pack(fill=tk.X)
        top_frame.pack(fill=tk.X)
        
        middle_frame = tk.Frame()
        
        original_frame = tk.Frame(middle_frame)
        file_box_frame = tk.Frame(original_frame)
        self._scrollbar_originals = tk.Scrollbar(file_box_frame)
        self._filebox_originals = tk.Listbox(file_box_frame, yscrollcommand=self._scrollbar_originals.set)
        self._scrollbar_originals.config(command=self._filebox_originals.yview)
        self._scrollbar_originals.pack(side='right', fill=tk.Y)
        self._filebox_originals.pack(side='left', fill=tk.BOTH, expand=True)
        file_box_frame.pack(fill=tk.BOTH, expand=True)
        sort_settings_frame = tk.Frame(original_frame)
        sort_settings_frame_1 = tk.Frame(sort_settings_frame)
        sort_settings_frame_2 = tk.Frame(sort_settings_frame)
        sort_settings_frame_3 = tk.Frame(sort_settings_frame)
        self._radio_namesort = tk.Radiobutton(sort_settings_frame_1, text='sort by name', variable=self._sortchoice_var, value=1)
        self._radio_datesort = tk.Radiobutton(sort_settings_frame_1, text='sort by date', variable=self._sortchoice_var, value=2)
        self._radio_namesort.pack(side='left')
        self._radio_datesort.pack(side='right')
        self._radio_homonymdatesort = tk.Radiobutton(sort_settings_frame_2, text='sort by homonymity and date', variable=self._sortchoice_var, value=3)
        self._radio_homonymdatesort.pack()
        self._timeoffset_seconds_label = tk.Label(sort_settings_frame_3, text='time offset')
        self._timeoffset_seconds_entry = tk.Entry(sort_settings_frame_3, textvariable=self._timeoffset_seconds_var)
        self._timeoffset_seconds_label.pack(side='left')
        self._timeoffset_seconds_entry.pack(side='left')
        self._timeoffset_identifier_label = tk.Label(sort_settings_frame_3, text='s, if name contains')
        self._timeoffset_identifier_entry = tk.Entry(sort_settings_frame_3, textvariable=self._timeoffset_identifier_var)
        self._timeoffset_identifier_label.pack(side='left')
        self._timeoffset_identifier_entry.pack(side='left')
        sort_settings_frame_1.pack()
        sort_settings_frame_2.pack()
        sort_settings_frame_3.pack()
        sort_settings_frame.pack()
        original_frame.pack(side='left', fill=tk.BOTH, expand=True)

        preview_frame = tk.Frame(middle_frame)
        preview_box_frame = tk.Frame(preview_frame)
        self._scrollbar_preview = tk.Scrollbar(preview_box_frame)
        self._filebox_preview = tk.Listbox(preview_box_frame, yscrollcommand=self._scrollbar_preview.set)
        self._scrollbar_preview.config(command=self._filebox_preview.yview)
        self._scrollbar_preview.pack(side='right', fill=tk.Y)
        self._filebox_preview.pack(side='left', fill=tk.BOTH, expand=True)
        preview_box_frame.pack(fill=tk.BOTH, expand=True)
        format_settings_frame_1 = tk.Frame(preview_frame)
        format_settings_frame_2 = tk.Frame(preview_frame)
        format_settings_frame_3 = tk.Frame(preview_frame)
        self._prefix_label = tk.Label(format_settings_frame_1, text='Prefix:')
        self._prefix_entry = tk.Entry(format_settings_frame_1, textvariable=self._prefix_var)
        self._prefix_label.pack(side='left')
        self._prefix_entry.pack(side='left')
        self._startnumber_label = tk.Label(format_settings_frame_2, text='Start:')
        self._startnumber_entry = tk.Entry(format_settings_frame_2, textvariable=self._startnumber_var)
        self._startnumber_label.pack(side='left')
        self._startnumber_entry.pack(side='left')
        self._digitnumber_label = tk.Label(format_settings_frame_2, text='Digits:')
        self._digitnumber_spinbox = tk.Spinbox(format_settings_frame_2, textvariable=self._digits_var)
        self._digitnumber_label.pack(side='left')
        self._digitnumber_spinbox.pack(side='left')
        self._radio_homonymity_yes = tk.Radiobutton(format_settings_frame_3, text='preserve homonymity', variable=self._homonymity_var, value=1)
        self._radio_homonymity_no = tk.Radiobutton(format_settings_frame_3, text='strictly increase', variable=self._homonymity_var, value=2)
        self._radio_homonymity_yes.pack(side='left')
        self._radio_homonymity_no.pack(side='left')
        format_settings_frame_1.pack()
        format_settings_frame_2.pack()
        format_settings_frame_3.pack()
        self._progress_bar = ttk.Progressbar(preview_frame, orient="horizontal", mode="determinate")
        self._progress_bar.pack(side='bottom', fill=tk.X)
        preview_frame.pack(side='right', fill=tk.BOTH, expand=True)
        
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        bottom_frame = tk.Frame()
        self._apply_button = tk.Button(bottom_frame, text='apply', command=self._apply_button_clicked)
        self._apply_button.pack(fill=tk.X)
        bottom_frame.pack(side='bottom', fill=tk.X)
        
        self._digitnumber_spinbox.config(from_=self.fr._namepattern["digits"], to=9)


    # -------callback and utility methods-------------------------------

    def _get_folder_directory(self):
        path = filedialog.askdirectory()
        return path

    def _browse_button_clicked(self):
        path = self._get_folder_directory()
        if path:
            self.fr._basepath = path
            self._browse_button.config(text=path)
            self.fr._make_file_list()
            self.fr._sort_by_name()
            self._show_originals()
            self._progress_bar.config(maximum=len(self.fr._file_list))
            self._progress_bar.config(value=0)
            digits = self._get_current_min_digits()
            self.fr._namepattern["digits"] = digits
            self._digitnumber_spinbox.config(from_=digits)
            self._digits_var.set(str(digits))  # callback to _digits_selected

    def _get_current_min_digits(self):
        checked = self._homonymity_var.get()
        if checked == 1:
            amount = len(self.fr._get_homonymity_groups())
        elif checked == 2:
            amount = len(self.fr._file_list)
        else:
            amount = 0
            digits = 1
        start = self._startnumber_var.get()
        start = int(start) if start != '' else 1
        max_num = start + amount - 1
        digits = len(str(max_num))
        return digits

    def _sorting_radio_selected(self, *args):
        if self._sortchoice_var.get() == 1:
            self.fr._sort_by_name()
        elif self._sortchoice_var.get() == 2:
            self.fr._sort_by_date()
        elif self._sortchoice_var.get() == 3:
            self.fr._sort_by_date_and_homonymity()
        self._show_originals()
        self.fr._make_new_names()
        self._show_preview()

    def _timeoffset_entered(self, *args):
        current_entry_seconds = self._timeoffset_seconds_var.get()
        current_entry_identifier = self._timeoffset_identifier_var.get()
        if current_entry_identifier == '':
            current_entry_identifier = None
        if re.match(r"^-?\d+$", current_entry_seconds):  # positive or negative integer
            seconds = int(current_entry_seconds)
        elif current_entry_seconds == '-':  # started typing negative integer
            seconds = 0
        elif current_entry_seconds == "":  # empty means 0
            seconds = 0
        else:  # anything else converts to 0
            seconds = 0
            self._timeoffset_seconds_var.set("0")  # callback to _timeoffset_entered
            return
        self.fr._time_offsets = [{'identifier': current_entry_identifier, 'seconds': seconds}]
        self._sorting_radio_selected()

    def _prefix_entered(self, *args):
        self.fr._namepattern["prefix"] = self._prefix_var.get()
        self.fr._make_new_names()
        self._show_preview()

    def _startnumber_entered(self, *args):
        current_entry = self._startnumber_var.get()
        if re.match(r"^\d+$", current_entry):
            start = int(current_entry)
        elif current_entry == "":  # empty means 1
            # self._startnumber_var.set("1")
            start = 1
        else:  # anything else converts to 1
            self._startnumber_var.set("1")  # callback to _startnumber_entered
            return
        min_digits = self._get_current_min_digits()
        # max_num = start + amount - 1
        # min_digits = len(str(max_num))
        self.fr._namepattern["startnum"] = start
        self._digitnumber_spinbox.config(from_=min_digits)
        self._digits_var.set(str(min_digits))  # callback to _digits_selected

    def _digits_selected(self, *args):
        digits = self._digits_var.get()
        min_digits = self._get_current_min_digits()
        if re.match(r"^\d+$", digits) and int(digits) >= min_digits:
            digits = int(digits)
            self.fr._namepattern["digits"] = digits
            self.fr._make_new_names()
            self._show_preview()
        else:
            digits = self.fr._namepattern["digits"]
            self._digits_var.set(str(digits))

    def _homonymity_radio_selected(self, *args):
        checked = self._homonymity_var.get()
        if checked == 1:
            self.fr._preserve_homonymity = True
        elif checked == 2:
            self.fr._preserve_homonymity = False
        digits= self._get_current_min_digits()
        self._digitnumber_spinbox.config(from_=digits)
        self._digits_var.set(str(digits))  # callback to _digits_selected

    def _show_originals(self):
        self._filebox_originals.delete(0, tk.END)
        for item in self.fr._file_list:
            self._filebox_originals.insert(tk.END, item)

    def _show_preview(self):
        self._filebox_preview.delete(0, tk.END)
        for item in self.fr._new_names:
            self._filebox_preview.insert(tk.END, item)
        self._apply_button.config(text="apply")

    def _set_writechoice(self, *args):
        pass

    def _apply_button_clicked(self):
        self._rename_copy()

    def _rename_copy(self):
        self._progress_var = 0
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_folder = os.path.join(self.fr._basepath, "renamed_files_" + time)
        os.mkdir(new_folder)
        def _copy_next():
            old = self.fr._file_list[self._progress_var]
            new = self.fr._new_names[self._progress_var]
            try:
                old_path = os.path.join(self.fr._basepath, old[0])
                new_path = os.path.join(new_folder, new)
                shutil.copy2(old_path, new_path)
                self._progress_bar.config(value=self._progress_var + 1)
                self._progress_var += 1
            except Exception as err:
                print("An Error occurred:", err)
            if self._progress_var < len(self.fr._file_list):
                self._window.after(1, _copy_next)
            else:
                self._apply_button.config(text="Success! Close window, or continue browsing and renaming.")
        _copy_next()

    def _rename_copy2(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_folder = os.path.join(self.fr._basepath, "renamed_files_" + time)
        os.mkdir(new_folder)
        for i, (old, new) in enumerate(zip(self.fr._file_list, self.fr._new_names)):
            try:
                old_path = os.path.join(self.fr._basepath, old[0])
                new_path = os.path.join(new_folder, new)
                shutil.copy2(old_path, new_path)
                self._progress_bar.config(value=i+1)
            except Exception as err:
                print("An Error occurred:", err)


if __name__ == "__main__":
    root = tk.Tk()
    frg = FileRenamerGUI(root)
    root.mainloop()
