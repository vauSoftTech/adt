#!/usr/bin/env python3
# -*- coding: utf_8 -*-
#
"""

    Copyright    : 2015 November. A. R. Bhatt.
    Organization : VAU SoftTech
    Project      : adt - Tithi progression log for a given date
    Script Name  : adt.py
    License      : GNU General Public License v3.0


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from tkinter import *
from tkinter import messagebox

from datetime import datetime as dttm

from time import sleep
import adt


class AdtMain(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.master = parent
        self.master.title("VAU - Any Date Tithi")
        self.master.protocol("WM_DELETE_WINDOW", self.client_exit)
        self.master.resizable(False, False)
        self.pack(fill=BOTH, expand=1)
        self['borderwidth'] = 2
        self['relief'] = 'sunken'

        self.place_list = sorted(adt.get_list_of_places())

        self.place_entered = StringVar()
        self.place_lat = StringVar()
        self.place_lon = StringVar()

        self.date_entered = StringVar()
        self.text_to_display = StringVar()

        self.text_to_display.set("")
        self.place_entered.set(self.place_list[0])
        self.date_entered.set(f"{dttm.today():%Y-%m-%d}")
        self.date_entered.set("2015-11-30")

        self.make_widgets()
        return

    def client_exit(self):
        if messagebox.askquestion("Decide", "Are you sure to exit?") == 'yes':
            self.master.destroy()
        else:
            messagebox.showinfo('Return', 'OK then, you will now return to the'
                                          ' application screen')
        return

    def make_widgets(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)
        fl = Menu(menu)
        fl.add_command(label=" Exit ", command=self.client_exit)
        menu.add_cascade(label=" File ", menu=fl)

        self.place = OptionMenu(self, self.place_entered, *self.place_list,
                                command=self.get_place_info)
        self.place.pack(padx=20, pady=5)

        self.lat_label = Label(self, textvariable=self.place_lat)
        self.lat_label.pack(padx=20, pady=2)

        self.lon_label = Label(self, textvariable=self.place_lon)
        self.lon_label.pack(padx=20, pady=2)

        self.date_entry_label = Label(self, text="Please enter a date")
        self.date_entry_label.pack(padx=20, pady=5)

        self.date_entry = Entry(self, textvariable=self.date_entered)
        self.date_entry.pack(padx=20, pady=5)


        self.calc_btn = Button(self, text="Calculate",
                               command=self.calculate_callback)
        self.calc_btn.pack(padx=20, pady=5)

        self.msg = Label(self, textvariable=self.text_to_display)
        self.msg.pack(padx=0, pady=20)

        self.get_place_info(None)
        return

    def disable_ui(self):
        self.place.config(state="disabled")
        self.date_entry.config(state="disabled")
        self.calc_btn.config(state="disabled")
        self.update()
        return

    def enable_ui(self):
        self.place.config(state="normal")
        self.date_entry.config(state="normal")
        self.calc_btn.config(state="normal")
        self.update()
        return

    def calculate_callback(self):
        try:
            x = self.date_entered.get()
            dttm.strptime(x, "%Y-%m-%d")
            self.text_to_display.set("Calculation has begun.")
            self.disable_ui()
            sleep(5)
            self.enable_ui()
            self.text_to_display.set("Calculation finished. Result has been "
                                     "saved to a file.")
        except ValueError as e:
            messagebox.showinfo("Invalid Date", f"{x} is not a valid date!")
        return

    def get_place_info(self, event):
        print(event)
        y = self.place_entered.get()
        x = adt.get_details_of_selected_place(y)
        self.place_lat.set(x[1])
        self.place_lon.set(x[2])
        return


def main():
    main_win = Tk()
    main_win.geometry('400x300')
    app = AdtMain(main_win)
    app.mainloop()
    return


if __name__ == '__main__':
   main()
