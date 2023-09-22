"""
pythoneda/shared/git/git_add.py

This file declares the GitAdd class.

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
from .git_add_failed import GitAddFailed
from .git_add_all_failed import GitAddAllFailed
from pythoneda import attribute, BaseObject
import subprocess

class GitAdd(BaseObject):
    """
    Provides git add operations.

    Class name: GitAdd

    Responsibilities:
        - Provides "git add" operations.

    Collaborators:
        - pythoneda.shared.git.GitAddFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitAdd instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__()
        self._folder = folder

    @property
    @attribute
    def folder(self) -> str:
        """
        Retrieves the folder of the cloned repository.
        :return: Such folder.
        :rtype: str
        """
        return self._folder

    def add(self, file:str) -> str:
        """
        Adds changes in given file to the staging area.
        :param file: The file to add.
        :type file: str
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None

        try:
            execution = subprocess.run(
                ["git", "add", file],
                check=True,
                capture_output=True,
                text=True,
                cwd=self.folder,
            )
            result = execution.stdout
        except subprocess.CalledProcessError as err:
            GitAdd.logger().error(err)
            GitAdd.logger().error(err.stderr)
            raise GitAddFailed(self.folder, file, err.stderr)

        return result

    def add_all(self) -> str:
        """
        Adds all changes to the staging area.
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None

        try:
            execution = subprocess.run(
                ["git", "add", "--all"],
                check=True,
                capture_output=True,
                text=True,
                cwd=self.folder,
            )
            result = execution.stdout
        except subprocess.CalledProcessError as err:
            GitAdd.logger().error(err)
            GitAdd.logger().error(err.stderr)
            raise GitAddAllFailed(self.folder, err.stderr)

        return result
