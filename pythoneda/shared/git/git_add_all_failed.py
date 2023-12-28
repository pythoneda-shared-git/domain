"""
pythoneda/shared/git/git_add_all_failed.py

This file defines the GitAddAllFailed exception class.

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


class GitAddAllFailed(Exception, BaseObject):
    """
    Adding all changes to the git repository failed.

    Class name: GitAddAllFailed

    Responsibilities:
        - Represent the error when adding all changes to a git repository.

    Collaborators:
        - None
    """

    def __init__(self, folder: str, output: str):
        """
        Creates a new GitAddAllFailed instance.
        :param folder: The repository folder.
        :type folder: str
        :param output: The output of the git command.
        :type output: str
        """
        super().__init__(f'"git add -a" failed in {folder}')
        self._output = output

    @property
    def output(self) -> str:
        """
        Retrieves the output of the git command.
        :return: Such output.
        :rtype: str
        """
        return self._output
