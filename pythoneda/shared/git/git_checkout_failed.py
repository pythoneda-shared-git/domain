"""
pythoneda/shared/git/git_checkout_failed.py

This file defines the GitCheckoutFailed exception class.

Copyright (C) 2023-today rydnr's pythoneda-shared-git/shared

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
from pythoneda import BaseObject


class GitCheckoutFailed(Exception, BaseObject):
    """
    Running git checkout [rev] failed.

    Class name: GitCheckoutFailed

    Responsibilities:
        - Represent the error when running git checkout.

    Collaborators:
        - None
    """

    def __init__(self, url: str, rev: str, folder: str):
        """
        Creates a new instance.
        :param url: The url of the repository.
        :type url: str
        :param rev: The revision.
        :type rev: str
        :param folder: The folder with the cloned repository.
        :type folder: str
        """
        super().__init__(f'"git checkout {rev}" from {url} in folder {folder} failed')
