"""
pythoneda/shared/git/git_progress_logging.py

This file declares the GitProgressLogging class.

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
from git.util import RemoteProgress
from pythoneda import BaseObject


class GitProgressLogging(RemoteProgress, BaseObject):
    """
    Shows the progress of long-running git operations.

    Class name: GitProgressLogging

    Responsibilities:
        - Logs the progress of git operations.

    Collaborators:
        - GitRepo: Uses me for certain git operations.
    """

    def update(self, opCode: str, curCount: int, maxCount: int = None, message: str = ""):
        """
        Gets notified regularly of the progress of an operation.
        :param opCode: The operation code.
        :type opCode: str
        :param curCount: The current count.
        :type curCount: int
        :param maxCount: The total count.
        :type maxCount: int
        :param message: The message.
        :type message: str
        """
        GitProgressLogging.logger().debug(self._cur_line)
