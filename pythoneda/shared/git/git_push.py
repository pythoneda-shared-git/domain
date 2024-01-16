# vim: set fileencoding=utf-8
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
from .git_operation import GitOperation
from .git_push_branch_failed import GitPushBranchFailed
from .git_push_failed import GitPushFailed
from .git_push_tags_failed import GitPushTagsFailed


class GitPush(GitOperation):
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
        super().__init__(folder)

    def push_branch(self, branch: str) -> bool:
        """
        Pushes changes in a given branch to a remote repository.
        :param branch: The branch.
        :type branch: str
        :return: True if the operation succeeds.
        :rtype: bool
        """
        (code, stdout, stderr) = self.run(["git", "push", branch])
        if code != 0:
            GitPush.logger().error(stderr)
            raise GitPushBranchFailed(self.folder, branch)

        return True

    def push(self) -> bool:
        """
        Pushes changes in all branches to a remote repository.
        :return: True if the operation succeeds.
        :rtype: bool
        """
        (code, stdout, stderr) = self.run(["git", "push"])
        if code != 0:
            GitPush.logger().error(stderr)
            raise GitPushFailed(self.folder)

        return True

    def push_tags(self) -> bool:
        """
        Pushes changes to a remote repository.
        :return: True if the operation succeeds.
        :rtype: bool
        """
        (code, stdout, stderr) = self.run(["git", "push", "--tags"])
        if code != 0:
            GitPush.logger().error(stderr)
            raise GitPushTagsFailed(self.folder)

        return True
