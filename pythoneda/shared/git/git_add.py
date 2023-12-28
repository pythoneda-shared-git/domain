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
from .git_operation import GitOperation


class GitAdd(GitOperation):
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
        super().__init__(folder)

    def add(self, file: str) -> str:
        """
        Adds changes in given file to the staging area.
        :param file: The file to add.
        :type file: str
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None
        (code, stdout, stderr) = self.run(["git", "add", file])
        GitAdd.logger().info(f"git add {file} -> {code}")
        if code == 0:
            result = stdout
        else:
            if stderr != "":
                GitAdd.logger().error(stderr)
            if stdout != "":
                GitAdd.logger().error(stdout)
            raise GitAddFailed(self.folder, file, stderr)

        return result

    def add_all(self) -> str:
        """
        Adds all changes to the staging area.
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None
        (code, stdout, stderr) = self.run(["git", "add", "--all"])
        if code == 0:
            result = stdout
        else:
            if stderr != "":
                GitAdd.logger().error(stderr)
            if stdout != "":
                GitAdd.logger().error(stdout)
            raise GitAddAllFailed(self.folder, stderr)

        return result
