#!/usr/bin/env python3
# -*- coding: utf_8 -*-
#
"""

    Copyright    : 2015 November. A. R. Bhatt.
    Organization : VAU SoftTech
    Project      : adt - Tithi progression log for a given date
    Script Name  : header-template.py
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
from datetime import datetime
import ephem as ep

"""
    CONSTANTS DECLARATIONS
"""
RAASHI_SIZE = 30
RAASHI_SIZE_DEG = ep.degrees(f"{RAASHI_SIZE}:00:00")
TITHI_SIZE = 12
TITHI_SIZE_DEG = ep.degrees(f"{TITHI_SIZE}:00:00")

RAASHI_ANGLES_LIST = [(ep.degrees(str(x)), ep.degrees(str(x + RAASHI_SIZE))) for x in range(0, 331, RAASHI_SIZE)]
TITHI_ANGLES_LIST = [(ep.degrees(str(x)), ep.degrees(str(x + TITHI_SIZE))) for x in range(-6, 349, TITHI_SIZE)]
"""
    Main calculations routines
"""


def get_raashi_info_from_right_asc(right_asc):
    l = RAASHI_ANGLES_LIST

    raashi_info = (
            (1, 'Mesh', 'Aries', l[0][0], l[0][1]),
            (2, 'Vrishabh', 'Taurus', l[1][0], l[1][1]),
            (3, 'Mithun', 'Gemini', l[2][0], l[2][1]),
            (4, 'Kark', 'Cancer', l[3][0], l[3][1]),
            (5, 'Sinh', 'Leo', l[4][0], l[4][1]),
            (6, 'Kanya', 'Virgo', l[5][0], l[5][1]),
            (7, 'Tula', 'Libra', l[6][0], l[6][1]),
            (8, 'Vrishchik', 'Scorpio', l[7][0], l[7][1]),
            (9, 'Dhanu', 'Sagittarius', l[8][0], l[8][1]),
            (10, 'Makar', 'Capricorn', l[9][0], l[9][1]),
            (11, 'Kumbh', 'Aquarius', l[10][0], l[10][1]),
            (12, 'Min', 'Pisces', l[11][0], l[11][1]),
    )

    def convert_right_asc_to_raashi_index(ra):
        return int(ep.degrees(ra) / RAASHI_SIZE_DEG)

    result = raashi_info[convert_right_asc_to_raashi_index(right_asc)]
    elapsed = ((right_asc - ep.degrees(result[3])) / RAASHI_SIZE_DEG) * 100
    remains = 100 - elapsed
    return result[0], result[1], result[2], result[3], result[4], elapsed, remains


def get_tithi_info_from_right_asc(moon_ra, sun_ra):
    l = TITHI_ANGLES_LIST
    tithi_info = (
            (0, "Amaas", l[0][0], l[0][1]),
            (1, "Sud Padavo", l[1][0], l[1][1]),
            (2, "Sud Beej", l[2][0], l[2][1]),
            (3, "Sud Threej", l[3][0], l[3][1]),
            (4, "Sud Choth", l[4][0], l[4][1]),
            (5, "Sud Pancham", l[5][0], l[5][1]),
            (6, "Sud Chhath", l[6][0], l[6][1]),
            (7, "Sud Satam", l[7][0], l[7][1]),
            (8, "Sud Aatham", l[8][0], l[8][1]),
            (9, "Sud Nom", l[9][0], l[9][1]),
            (10, "Sud Dasam", l[10][0], l[10][1]),
            (11, "Sud Agiyaras", l[11][0], l[11][1]),
            (12, "Sud Baaras", l[12][0], l[12][1]),
            (13, "Sud Teras", l[13][0], l[13][1]),
            (14, "Sud Chaudas", l[14][0], l[14][1]),
            (15, "Poonam", l[15][0], l[15][1]),
            (16, "Vad Padavo", l[16][0], l[16][1]),
            (17, "Vad Beej", l[17][0], l[17][1]),
            (18, "Vad Threej", l[18][0], l[18][1]),
            (19, "Vad Choth", l[19][0], l[19][1]),
            (20, "Vad Pancham", l[20][0], l[20][1]),
            (21, "Vad Chhath", l[21][0], l[21][1]),
            (22, "Vad Satam", l[22][0], l[22][1]),
            (23, "Vad Aatham", l[23][0], l[23][1]),
            (24, "Vad Nom", l[24][0], l[24][1]),
            (25, "Vad Dasam", l[25][0], l[25][1]),
            (26, "Vad Agiyaras", l[26][0], l[26][1]),
            (27, "Vad Baaras", l[27][0], l[27][1]),
            (28, "Vad Teras", l[28][0], l[28][1]),
            (29, "Vad Chaudas", l[29][0], l[29][1]),
            (30, "Amaas", l[0][0], l[0][1]),
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

            for i, j in enumerate(l):
                if j[0] <= a <= j[1]:
                    break
            return i

        if method_to_use == 1:
            t = method_one(ra)
        elif method_to_use == 2:
            t = method_two(ra)

        return tithi_info[t]

    moon_sun_angle = get_moon_sun_ra_difference(moon_ra, sun_ra)
    q = calculate_tithi(moon_sun_angle, method_to_use=2)
    elapsed = (ep.degrees(ep.degrees(moon_sun_angle) - q[2]) / TITHI_SIZE_DEG * 100)
    return q[0], q[1], q[2], moon_sun_angle, q[3], elapsed, 100 - elapsed


def calculate_tithi_for_a_given_date_time(array_of_given_datetime_in_utc):
    place = ep.Observer()
    place.name = "Amdavad"
    place.lat = "22"
    place.lon = "73"

    result = []
    for each_date in array_of_given_datetime_in_utc:
        place.date = each_date
        s = ep.Sun(place)
        m = ep.Moon(place)
        w = get_tithi_info_from_right_asc(m.ra, s.ra)
        data_row = (each_date, w[1], w[2], w[3], w[4], w[5], w[6])
        result.append( data_row )

    return result


def main():
    user_entry = input("Enter Date : ")
    dts = []
    for i in range(0, 24):
        for j in range(0, 56, 5):
            dts.append(f"{user_entry} {i:>02}:{j:>02}:00")

    ans = calculate_tithi_for_a_given_date_time(dts)
    flnm = f"output/output{user_entry}.csv"
    with open(flnm, "w") as out_file:
        txt = f"Given dateTime(UTC), Tithi Name, current, Elapsed, Remains\n"
        out_file.write(txt)
        for ele in ans:
            txt = f"{ele[0]}, {ele[1]}, {ele[3]}, {ele[5]}\n"
            out_file.write(txt)

    return


if __name__ == '__main__':
    main()
