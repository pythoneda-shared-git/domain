"""
pythoneda/shared/git/git_init.py

This file declares the GitInit class.

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
from pythoneda import attribute, BaseObject
from pythoneda.shared.git import GitDiffFailed
import subprocess

class GitInit(BaseObject):
    """
    Provides git init operations.

    Class name: GitInit

    Responsibilities:
        - Provides "git init" operations.

    Collaborators:
        - pythoneda.shared.git.GitInitFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitInit instance for given folder.
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

    def init(self):
        """
        Runs git init.
        """
        result = None

        try:
            execution = subprocess.run(
                ["git", "-C", self.folder, "init"],
                check=True,
                capture_output=True,
                text=True,
                cwd=self.folder,
            )
            result = execution.stdout
        except subprocess.CalledProcessError as err:
            GitInit.logger().error(err)
            raise GitInitFailed(self.folder)

        return result
