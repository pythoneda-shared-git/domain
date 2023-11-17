"""
pythoneda/shared/git/git_commit.py

This file declares the GitCommit class.

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
from .git_commit_failed import GitCommitFailed
from .git_operation import GitOperation


class GitCommit(GitOperation):
    """
    Models commits in git.

    Class name: GitCommit

    Responsibilities:
        - Represents commits in git.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitCommit instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__(folder)

    def commit(self, message: str) -> str:
        """
        Commits staged changes.
        :param message: The message.
        :type message: str
        :return: A tuple containing the hash and diff of the commit.
        :rtype: tuple(str, str)
        """
        (code, stdout, stderr) = self.run(["git", "commit", "-S", "-m", message])
        if code != 0:
            if stderr != "":
                GitCommit.logger().error(stderr)
            if stdout != "":
                GitCommit.logger().error(stdout)
            raise GitCommitFailed(self.folder, stderr)

        return self.latest_commit()

    def latest_commit(self):
        """
        Retrieves the hash and diff of the latest commit.
        :return: A tuple containing the hash and diff of the latest commit.
        :rtype: tuple(str, str)
        """
        latest_commit = self.repo.head.commit
        latest_commit_hash = latest_commit.hexsha
        latest_commit_diff = latest_commit.diff("HEAD~1")

        return (latest_commit_hash, str(latest_commit_diff))
