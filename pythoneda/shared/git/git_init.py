# vim: set fileencoding=utf-8
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
from .git_init_failed import GitInitFailed
from .git_operation import GitOperation


class GitInit(GitOperation):
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
        super().__init__(folder)

    def init(self):
        """
        Runs git init.
        """
        result = None

        (code, stdout, stderr) = self.run(["git", "init"])
        if code == 0:
            result = stdout
        else:
            GitInit.logger().error(stderr)
            raise GitInitFailed(self.folder, stderr)

        return result
