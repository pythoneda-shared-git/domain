# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_apply.py

This file declares the GitApply class.

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
from .git_apply_failed import GitApplyFailed
from .git_operation import GitOperation


class GitApply(GitOperation):
    """
    Provides git apply operations.

    Class name: GitApply

    Responsibilities:
        - Provides "git apply" operations.

    Collaborators:
        - pythoneda.shared.git.GitApplyFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitApply instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__(folder)

    def apply(self, patchFile: str) -> str:
        """
        Applies the changes.
        :param patchFile: The location of the patch file to apply.
        :type patchFile: str
        :return: The output of the operation, should it succeeds.
        :rtype: str
        """
        result = None
        (code, stdout, stderr) = self.run(["git", "apply", patchFile])
        if code == 0:
            result = stdout
        else:
            GitApply.logger().debug(stderr)
            raise GitApplyFailed(self.folder)

        return result

    def apply3way(self) -> str:
        """
        Retrieves the diff.
        :return: The diff if the operation succeeds.
        :rtype: str
        """
        result = None
        (code, stdout, stderr) = self.run(["git", "apply", "--3way"])
        if code == 0:
            result = stdout
        else:
            GitApply.logger().error(stderr)
            raise GitApplyFailed(self.folder)

        return result
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
