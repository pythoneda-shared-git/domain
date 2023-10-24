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
import os
from pythoneda import attribute, BaseObject
from git import Repo
import subprocess


class GitCommit(BaseObject):
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
        super().__init__()
        self._folder = folder
        self._repo = Repo(self.folder)

    @property
    @attribute
    def folder(self) -> str:
        """
        Retrieves the folder of the cloned repository.
        :return: Such folder.
        :rtype: str
        """
        return self._folder

    @property
    def repo(self):
        """
        Retrieves the GitPython repository.
        :return: Such instance.
        :rtype: git.Repo
        """
        return self._repo

    def commit(self, message:str) -> str:
        """
        Commits staged changes.
        :param message: The message.
        :type message: str
        :return: A tuple containing the hash and diff of the commit.
        :rtype: tuple(str, str)
        """
        result = None

        home_path = os.environ.get("HOME")

        # Define custom Git settings
        custom_env = {
            "GIT_CONFIG_GLOBAL": os.path.join(home_path, ".gitconfig-UnveilingPartner"),
            "GIT_CONFIG_NOSYSTEM": "true",
            **dict(os.environ)  # Include existing environment variables
        }

        completed_process = subprocess.run(
            [ "git", "commit", "-S", "-m", message],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=self.folder,
            env=custom_env
        )

        if completed_process.returncode == 0:
            result = completed_process.stdout
        else:
            GitCommit.logger().error(completed_process.stderr)
            raise GitCommitFailed(self.folder, completed_process.stdout)

        return self.latest_commit()

    def latest_commit(self):
        """
        Retrieves the hash and diff of the latest commit.
        :return: A tuple containing the hash and diff of the latest commit.
        :rtype: tuple(str, str)
        """
        latest_commit = self.repo.head.commit
        latest_commit_hash = latest_commit.hexsha
        latest_commit_diff = latest_commit.diff('HEAD~1')

        return (latest_commit_hash, str(latest_commit_diff))
