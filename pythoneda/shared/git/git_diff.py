# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_diff.py

This file declares the GitDiff class.

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
from .git_diff_failed import GitDiffFailed
from .git_operation import GitOperation


class GitDiff(GitOperation):
    """
    Provides git diff operations.

    Class name: GitDiff

    Responsibilities:
        - Provides "git diff" operations.

    Collaborators:
        - pythoneda.shared.git.GitDiffFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitDiff instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__(folder)

    def diff(self) -> str:
        """
        Retrieves the diff.
        :return: The diff if the operation succeeds.
        :rtype: str
        """
        result = None

        (code, stdout, stderr) = self.run(["git", "diff"])
        if code == 0:
            result = stdout
        else:
            GitDiff.logger().error(stderr)
            raise GitDiffFailed(self.folder)

        return result

    def committed_diff(self) -> str:
        """
        Retrieves the diff.
        :return: The diff if the operation succeeds.
        :rtype: str
        """
        result = None

        (code, stdout, stderr) = self.run(["git", "diff", "HEAD^", "HEAD"])
        if code == 0:
            result = stdout
        else:
            GitDiff.logger().error(stderr)
            raise GitDiffFailed(self.folder)

        return result
