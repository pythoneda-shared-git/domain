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
from .git_operation import GitOperation
from .git_stash_pop_failed import GitStashPopFailed
from .git_stash_push_failed import GitStashPushFailed
import re


class GitStash(GitOperation):
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
        super().__init__(folder)

    def push(self, message: str = None) -> str:
        """
        Performs a git stash push.
        :param message: The message.
        :type message: str
        :return: The stash id.
        :rtype: str
        """
        result = None

        args = ["git", "stash", "push"]
        if message:
            args.extend(["-m", message])
        (code, stdout, stderr) = self.run(args)
        if code == 0:
            # Parse the output to get the stash identifier
            match = re.search(
                r"Saved working directory and index state (\w+ on .+: [a-f0-9]+ .+)",
                stdout,
            )
            if match:
                result = match.group(1)
        else:
            GitStash.logger().error(stderr)
            raise GitStashPushFailed(self.folder)

        return result

    def pop(self, stashId: str) -> str:
        """
        Performs a git stash pop for given id.
        :param stashId: The stash id.
        :type stashId: str
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None

        (code, stdout, stderr) = self.run(["git", "stash", "pop", stashId])
        if code == 0:
            result = execution.stdout
        else:
            GitStash.logger().error(stderr)
            raise GitStashPopFailed(self.folder)

        return result
