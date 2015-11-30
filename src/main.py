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
from tkinter.ttk import *
from tkinter import messagebox

from datetime import datetime as dttm
from datetime import timedelta as td

from time import sleep
import adt


class AdtMain(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.master = parent
        self.master.title("VAU - ADT")
        self.master.protocol("WM_DELETE_WINDOW", self.client_exit)
        self.master.resizable(False, False)
        self.pack(fill=BOTH, expand=1)
        self['borderwidth'] = 2
        self['relief'] = 'sunken'

        self.place_list = sorted(adt.get_list_of_places())

        self.place_entered = StringVar()
        self.place_lat = StringVar()
        self.place_lon = StringVar()
        self.place_ele = StringVar()
        self.interval_var = DoubleVar()

        self.date_entered = StringVar()
        self.text_to_display = StringVar()

        self.text_to_display.set("")
        self.place_entered.set('Choose...')
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

    # noinspection PyAttributeOutsideInit
    def make_widgets(self):
        # Create MainMenu
        main_menu = Menu(self.master, tearoff=0)
        self.master.config(menu=main_menu)

        # Create FileMenu
        fl = Menu(main_menu, tearoff=0)
        fl.add_command(label=" Exit ", command=self.client_exit)
        main_menu.add_cascade(label=" File ", menu=fl)

        # Create HelpMenu
        hm = Menu(main_menu, tearoff=0)
        hm.add_command(label="Help", command=None)
        hm.add_command(label="About", command=self.show_about_dialog)
        main_menu.add_cascade(label="Help", menu=hm)

        self.style = Style()
        self.style.configure('.', background='#202020')
        self.style.configure('.', foreground='#1E90FF')
        self.style.configure('.', font="TkDefaultFont")

        s = Style()
        s.configure('my.TLabel', foreground='#1E90FF', font=('Ubuntu', 50))

        self.app_title = Label(self, text=" Tithi Progression for a Date ",
                               style='my.TLabel')
        self.app_title.grid(row=0, column=0, pady=2, columnspan=11)

        self.l0 = Label(self, text="Place ")
        self.l0.grid(row=1, column=0, columnspan=1, pady=2, sticky=E)

        self.place = OptionMenu(self, self.place_entered, self.place_list[0], *self.place_list,
                                command=self.get_place_info)
        self.place.grid(row=1, column=2, pady=2, columnspan=1, sticky='NESW')

        self.l1 = Label(self, text="Latitude : ")
        self.l1.grid(row=1, column=3, pady=2, columnspan=1, sticky=E)

        self.lat_label = Label(self, textvariable=self.place_lat)
        self.lat_label.grid(row=1, column=4, pady=2, columnspan=1, sticky=W)

        self.l2 = Label(self, text=" | ")
        self.l2.grid(row=1, column=5, pady=2, columnspan=1, sticky='NESW')

        self.l3 = Label(self, text="Longitude : ")
        self.l3.grid(row=1, column=6, pady=2, columnspan=1, sticky=E)

        self.lon_label = Label(self, textvariable=self.place_lon)
        self.lon_label.grid(row=1, column=7, pady=2, columnspan=1, sticky=W)

        self.l4 = Label(self, text=" | ")
        self.l4.grid(row=1, column=8, pady=2, columnspan=1, sticky='NESW')

        self.l5 = Label(self, text="Elevation : ")
        self.l5.grid(row=1, column=9, pady=2, columnspan=1, sticky=E)

        self.ele_label = Label(self, textvariable=self.place_ele)
        self.ele_label.grid(row=1, column=10, pady=2, columnspan=1, sticky=W)

        self.date_entry_label = Label(self, text="Enter a date ")
        self.date_entry_label.grid(row=2, column=0, pady=2, columnspan=1,
                                   sticky=E)

        self.date_entry = Entry(self, textvariable=self.date_entered)
        self.date_entry.grid(row=2, column=2, pady=2, columnspan=1, sticky='NESW')

        self.interval_label = Label(self, text="Interval (in Seconds)")
        self.interval_label.grid(row=3, column=0, pady=2, columnspan=1,
                                 sticky=E)

        self.interval_sb = Spinbox(self, from_=1.0, to=3600.0, increment=15,
                                   textvariable=self.interval_var,
                                   format='%5.0f', justify=RIGHT,
                                   wrap=True)
        self.interval_var.set("60")
        self.interval_sb.grid(row=3, column=2, pady=2, columnspan=1, sticky='NESW')

        self.calc_btn = Button(self, text="Calculate",
                               command=self.calculate_callback)
        self.calc_btn.grid(row=4, column=0, pady=2, sticky='NESW', columnspan=8)

        self.exit_btn = Button(self, text="Exit",
                               command=self.client_exit)
        self.exit_btn.grid(row=4, column=8, pady=2, sticky='NESW', columnspan=3)

        self.msg = Label(self, textvariable=self.text_to_display)
        self.msg.grid(row=5, column=0, pady=2, columnspan=9)

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

    def show_about_dialog(self):
        import about
        ad = Toplevel()
        big_frame = Frame(ad)
        big_frame.pack(fill='both', expand=True)

        l0 = Label(big_frame, text="ADT by VAU SoftTech")
        l0.place(relx=0.5, rely=0.3, anchor='center')
        l1 = Label(big_frame, text="www.vausofttech.com")
        l1.place(relx=0.5, rely=0.4, anchor='center')
        b0 = Button(big_frame, text="Close", command=ad.destroy)
        b0.place(relx=0.5, rely=0.7, anchor='center')
        ad.transient(self)
        ad.geometry('300x150')
        ad.wait_window()

    def calculate_callback(self):
        try:
            x = self.date_entered.get()
            dttm.strptime(x, "%Y-%m-%d")
            plc = self.place_entered.get()
            fl_nm = f"output/{plc.lower()}_{x}.csv"
            self.text_to_display.set("Calculation has begun.")
            self.disable_ui()
            print("Calculating for ...")
            print("Start date", x)
            print("Interval", td(seconds=self.interval_var.get()))
            adt.another_main(plc, x, x, td(seconds=self.interval_var.get()), fl_nm)
            self.enable_ui()
            self.text_to_display.set(f"Result saved to file \"{fl_nm}\".")
        except ValueError as e:
            messagebox.showinfo("Invalid Date", f"{x} is not a valid date!")
        return

    def get_place_info(self, event):
        print("User selected ", event)
        if event is None:
            x = adt.get_details_of_selected_place("AHMEDABAD")
            self.place_lat.set(f"{str(x[1]):<15s}")
            self.place_lon.set(f"{str(x[2]):<15s}")
            self.place_ele.set(f"{str(x[3]):<15s}")
        else:
            try:
                x = adt.get_details_of_selected_place(event)
                self.place_lat.set(f"{str(x[1]):<15s}")
                self.place_lon.set(f"{str(x[2]):<15s}")
                self.place_ele.set(f"{str(x[3]):<15s}")
            except:
                self.place_lat.set("")
                self.place_lon.set("")
                self.place_ele.set("")
        return


def main():
    main_win = Tk()
    # main_win.geometry('400x300')
    app = AdtMain(main_win)
    app.mainloop()
    return


if __name__ == '__main__':
   main()
