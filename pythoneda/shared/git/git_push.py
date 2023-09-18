"""
pythoneda/shared/git/git_push.py

This file declares the GitPush class.

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
from pythoneda.shared.git import GitPushFailed
import subprocess

class GitPush(BaseObject):
    """
    Provides git push operations.

    Class name: GitPush

    Responsibilities:
        - Provides "git push" operations.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitPush instance for given folder.
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

    def push(self) -> bool:
        """
        Pushes changes to a remote repository.
        :return: True if the operation succeeds.
        :rtype: bool
        """
        try:
            subprocess.run(
                ["git", "push"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.folder,
            )
        except subprocess.CalledProcessError as err:
            GitPush.logger().error(err.stdout)
            GitPush.logger().error(err.stderr)
            raise GitPushFailed(self.folder)

        return True

    def push_tags(self) -> bool:
        """
        Pushes changes to a remote repository.
        :return: True if the operation succeeds.
        :rtype: bool
        """
        try:
            subprocess.run(
                ["git", "push", "--tags"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.folder,
            )
        except subprocess.CalledProcessError as err:
            GitPush.logger().error(err.stdout)
            GitPush.logger().error(err.stderr)
            raise GitPushFailed(self.folder)

        return True
