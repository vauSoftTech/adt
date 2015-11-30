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

from datetime import datetime as dttm
from datetime import timedelta as td
import ephem as ep
import configparser as cp
import pathlib as pl

import vauutils

"""
    CONSTANTS DECLARATIONS
"""
TITHI_SIZE = 12
TITHI_SIZE_DEG = ep.degrees(f"{TITHI_SIZE}:00:00")

TITHI_ANGLES_LIST = [(ep.degrees(str(x)), ep.degrees(str(x + TITHI_SIZE)))
                     for x in range(-6, 349, TITHI_SIZE)]
"""
    Main calculations routines
"""


def dates_generator(start_date, end_date=None, delta=td(minutes=1)):
    if end_date is None:
        end_date = start_date + td(days=1)
        end_date = end_date.replace(hour=0, minute=0,
                                    second=0, microsecond=0)

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    value = start_date

    while value < end_date:
        yield value
        value += delta

    return


def str_to_date(dt_as_str):
    try:
        result = dttm.strptime(dt_as_str, "%Y-%m-%d")
    except ValueError as e:
        result = dttm.today().replace(hour=0, minute=0, second=0, microsecond=0)
    return result


def local_datetime_to_utc(local_date_time):
    def offset():
        d1 = dttm.now().replace(second=0, microsecond=0)
        d2 = dttm.utcnow().replace(second=0, microsecond=0)
        r = d1 - d2
        return r

    result = local_date_time - offset()
    return result


def load_config(file_name):
    result = None
    cfg_path = vauutils.RunInfo.get_script_filepath(__file__)
    cfg_name = cfg_path / "config" / file_name
    if cfg_name.is_file():
        result = cp.ConfigParser()
        result.read(cfg_name)
    else:
        print(f"Required file \"{file_name}\" not found.")
        exit()
    return result


def load_config_dot_cfg():
    return load_config("config.cfg")


def load_obs_dot_cfg(obs_file_name):
    return load_config(obs_file_name)


def get_tithi_info_from_right_asc(moon_ra, sun_ra):
    local_copy = TITHI_ANGLES_LIST
    tithi_info = (
            (0, "Amaas", local_copy[0][0], local_copy[0][1]),
            (1, "Sud Padavo", local_copy[1][0], local_copy[1][1]),
            (2, "Sud Beej", local_copy[2][0], local_copy[2][1]),
            (3, "Sud Threej", local_copy[3][0], local_copy[3][1]),
            (4, "Sud Choth", local_copy[4][0], local_copy[4][1]),
            (5, "Sud Pancham", local_copy[5][0], local_copy[5][1]),
            (6, "Sud Chhath", local_copy[6][0], local_copy[6][1]),
            (7, "Sud Satam", local_copy[7][0], local_copy[7][1]),
            (8, "Sud Aatham", local_copy[8][0], local_copy[8][1]),
            (9, "Sud Nom", local_copy[9][0], local_copy[9][1]),
            (10, "Sud Dasam", local_copy[10][0], local_copy[10][1]),
            (11, "Sud Agiyaras", local_copy[11][0], local_copy[11][1]),
            (12, "Sud Baaras", local_copy[12][0], local_copy[12][1]),
            (13, "Sud Teras", local_copy[13][0], local_copy[13][1]),
            (14, "Sud Chaudas", local_copy[14][0], local_copy[14][1]),
            (15, "Poonam", local_copy[15][0], local_copy[15][1]),
            (16, "Vad Padavo", local_copy[16][0], local_copy[16][1]),
            (17, "Vad Beej", local_copy[17][0], local_copy[17][1]),
            (18, "Vad Threej", local_copy[18][0], local_copy[18][1]),
            (19, "Vad Choth", local_copy[19][0], local_copy[19][1]),
            (20, "Vad Pancham", local_copy[20][0], local_copy[20][1]),
            (21, "Vad Chhath", local_copy[21][0], local_copy[21][1]),
            (22, "Vad Satam", local_copy[22][0], local_copy[22][1]),
            (23, "Vad Aatham", local_copy[23][0], local_copy[23][1]),
            (24, "Vad Nom", local_copy[24][0], local_copy[24][1]),
            (25, "Vad Dasam", local_copy[25][0], local_copy[25][1]),
            (26, "Vad Agiyaras", local_copy[26][0], local_copy[26][1]),
            (27, "Vad Baaras", local_copy[27][0], local_copy[27][1]),
            (28, "Vad Teras", local_copy[28][0], local_copy[28][1]),
            (29, "Vad Chaudas", local_copy[29][0], local_copy[29][1]),
            (30, "Amaas", local_copy[0][0], local_copy[0][1]),
    )

    def get_moon_sun_ra_difference(m, s):
        diff = ep.degrees(m - s)
        if ep.degrees("-6:00:00") <= diff < ep.degrees("0:00:00"):
            result = diff
        elif diff < ep.degrees("-6:00:00"):
            result = diff.norm
        else:
            result = diff
        return result

    def calculate_tithi(ra, method_to_use=1):

        def method_one(a):
            return int(a / TITHI_SIZE_DEG) + 1

        def method_two(a):
            i = -1
            for i, j in enumerate(local_copy):
                if j[0] <= a <= j[1]:
                    break
            return i

        if method_to_use == 1:
            t = method_one(ra)
        elif method_to_use == 2:
            t = method_two(ra)
        else:
            t = -1

        return tithi_info[t]

    moon_sun_angle = get_moon_sun_ra_difference(moon_ra, sun_ra)
    q = calculate_tithi(moon_sun_angle, method_to_use=2)
    elapsed = (ep.degrees(ep.degrees(moon_sun_angle) - q[2]) /
               TITHI_SIZE_DEG * 100)
    return q[0], q[1], q[2], q[3], moon_sun_angle


def tithi_generator(observer_info, start_date):
    dg = dates_generator(start_date, start_date + td(days=1))
    m = ep.Moon(observer_info)
    s = ep.Sun(observer_info)
    for each_date in dg:
        observer_info.date = each_date
        m.compute(observer_info)
        s.compute(observer_info)
        w = get_tithi_info_from_right_asc(m.ra, s.ra)
        data_row = (each_date, str(ep.degrees(m.ra)), str(ep.degrees(m.alt)),
                    str(ep.degrees(m.az)),
                    str(ep.degrees(s.ra)), str(ep.degrees(s.alt)),
                    str(ep.degrees(s.az)),
                    str(ep.degrees(w[4])))
        yield data_row
    return


def get_list_of_places():
    cfg = load_config_dot_cfg()
    obs_file_name = cfg.get("OBS", "file_name")
    obs = load_obs_dot_cfg(obs_file_name)
    return obs.sections()


def get_details_of_selected_place(selected_place):
    cfg = load_config_dot_cfg()
    obs_file_name = cfg.get("OBS", "file_name")
    obs = load_obs_dot_cfg(obs_file_name)
    a = obs.get(selected_place, "place_name")
    b = obs.get(selected_place, "place_longitude")
    c = obs.get(selected_place, "place_latitude")
    d = obs.getint(selected_place, "place_elevation")
    return [ a, b, c, d]


def another_main( place_name, ):
    pass


def main():
    cfg = load_config_dot_cfg()
    obs_file_name = cfg.get("OBS", "file_name")
    obs = load_obs_dot_cfg(obs_file_name)

    start_chr = ""
    i = 0
    for i, place in enumerate(obs.sections(), start=1):
        ending_char = "\n" if i % 3 == 0 else ""
        print(start_chr, f"{chr(64 + i)}).", f"{place:12.12s}", end=ending_char)
        start_chr = "\t|\t" if i % 3 != 0 else ""

    print("""
Now enter your choice. If you just press enter, place name "A" will be selected. 
    """)
    place = str(input(": ")).upper()
    if place.strip() == "":
        place = obs.sections()[0]

    if place not in obs.sections():
        print("That was not an option!, Bye!")
        exit()

    observer = ep.Observer()
    observer.name = obs.get(place, "place_name")
    observer.lon = obs.get(place, "place_longitude")
    observer.lat = obs.get(place, "place_latitude")
    observer.elevation = obs.getint(place, "place_elevation")

    print("""
Welcome to the program that calculates tithi progression for every five minutes
for the entire date. (starting from 00:00:00 hours to 23:55:00 hours). That
result of that calculation gets saved to a csv file. If you just press enter
Computer's current date will be considered.

The date is expected in ISO format i.e. YYYY-MM-DD :
          """)
    user_entry = input("Enter Date : ")
    user_entry = user_entry.strip()
    if user_entry == "":
        user_entry = "{:%Y-%m-%d}".format(dttm.today())

    ans = tithi_generator(observer, local_datetime_to_utc(str_to_date(user_entry)))
    filename = vauutils.RunInfo.get_script_filepath(__file__) / f"output/{place.lower()}_{user_entry}.csv"
    print("Started writing CSV file ...")
    with open(filename, "w") as out_file:
        txt = "Date & Time (UTC), Moon RA (A), Moon Dec, Moon Az, Sun RA (B), Sun Dec, Sun Az, Difference (A-B)\n"
        out_file.write(txt)
        for ele in ans:
            try:
                txt = f"{ele[0]}, {ele[1]}, {ele[2]}, {ele[3]}, {ele[4]}, {ele[5]}, {ele[6]}, {ele[7]} \n"
            except :
                txt = ""
            out_file.write(txt)
    print("Finished writing CSV file ...")
    print(f"File \"{filename}\" is ready now.")
    return None


if __name__ == '__main__':
    main()
