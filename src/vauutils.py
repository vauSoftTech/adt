#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""

    Copyright    : 2015 November. A. R. Bhatt.
    Organization : VAU SoftTech
    Project      : adt
    Script Name  : vauutils.py
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
from pathlib import *


class RunInfo:

    def __init__(self):
        return

    @classmethod
    def get_user_home(cls):
        return str(Path.home())

    @classmethod
    def get_cwd(cls):
        return str(Path.cwd())

    @classmethod
    def is_running_from_home_folder(cls):
        return cls.get_user_home() == cls.get_cwd()

    @classmethod
    def get_script_filename(cls, script_path_and_name):
        if script_path_and_name is not None:
            result = Path(script_path_and_name).resolve().name
        else:
            result = None
        return result

    @classmethod
    def get_script_filepath(cls, script_path_and_name):
        if script_path_and_name is not None:
            result = Path(script_path_and_name).resolve().parent
        else:
            result = None
        return result
