# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_branch.py

This file declares the GitBranch class.

Copyright (C) 2024-today rydnr's pythoneda-shared-git/shared

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
from .git_branch_failed import GitBranchFailed
from .git_branch_unset_upstream_failed import GitBranchUnsetUpstreamFailed
from .git_operation import GitOperation


class GitBranch(GitOperation):
    """
    Models branches in git.

    Class name: GitBranch

    Responsibilities:
        - Performs "git branch" operations.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitBranch instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__(folder)

    def branch(self, branch: str):
        """
        Creates a new branch.
        :param branch: The name of the branch.
        :type branch: str
        """
        (code, stdout, stderr) = self.run(["git", "branch", "-M", branch])
        if code != 0:
            if stderr != "":
                GitBranch.logger().error(stderr)
            if stdout != "":
                GitBranch.logger().error(stdout)
            raise GitBranchFailed(self.folder, branch, stderr)

    def unset_upstream(self):
        """
        Unsets the upstream.
        """
        (code, stdout, stderr) = self.run(["git", "branch", "--unset-upstream"])
        if code != 0:
            if stderr != "":
                GitBranch.logger().error(stderr)
            if stdout != "":
                GitBranch.logger().error(stdout)
            raise GitBranchUnsetUpstreamFailed(self.folder, stderr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
