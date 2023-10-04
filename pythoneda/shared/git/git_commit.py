"""
pythoneda/shared/git/git_commit.py

This file declares the GitCommit class.

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
from git import Repo

class GitCommit(BaseObject):
    """
    Models commits in git.

    Class name: GitCommit

    Responsibilities:
        - Represents commits in git.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitCommit instance for given folder.
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

    def latest_commit(self) -> str:
        """
        Retrieves the hash of the latest commit.
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        repo = Repo(self.folder)

        return repo.head.commit.hexsha
