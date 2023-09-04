"""
pythoneda/shared/git/git_stash.py

This file declares the GitStash class.

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
from pythoneda.shared.git import GitStashFailed
import re
import subprocess

class GitStash(BaseObject):
    """
    Provides git stash operations.

    Class name: GitStash

    Responsibilities:
        - Provides "git stash" operations.

    Collaborators:
        - pythoneda.shared.git.GitStashFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitStash instance for given folder.
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

    def push(self, message:str=None) -> str:
        """
        Performs a git stash push.
        :param message: The message.
        :type message: str
        :return: The stash id.
        :rtype: str
        """
        result = None

        args = [ "git", "stash", "push" ]
        if message:
            args.extend(["-m", message])
        try:
            execution = subprocess.run(
                args,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.folder,
            )
            output = execution.stdout

            # Parse the output to get the stash identifier
            match = re.search(r'Saved working directory and index state (\w+ on .+: [a-f0-9]+ .+)', output)
            if match:
                result = match.group(1)
        except subprocess.CalledProcessError as err:
            logger().error(err)
            raise GitStashFailed(self.folder)

        return result

    def pop(self, stashId:str) -> str:
        """
        Performs a git stash pop for given id.
        :param stashId: The stash id.
        :type stashId: str
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None

        try:
            execution = subprocess.run(
                ["git", "stash", "pop", stashId],
                check=True,
                capture_output=True,
                text=True,
                cwd=self.folder,
            )
            result = execution.stdout
        except subprocess.CalledProcessError as err:
            logger().error(err)
            raise GitStashFailed(self.folder)

        return result
