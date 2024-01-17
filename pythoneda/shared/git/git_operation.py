# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_operation.py

This file declares the GitOperation class.

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
import abc
from git import Repo
import os
from pythoneda.shared import attribute, BaseObject
import subprocess
from typing import List


class GitOperation(BaseObject, abc.ABC):
    """
    Common logic for git operations.

    Class name: GitOperation

    Responsibilities:
        - Provides common logic for subclasses.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitOperation instance for given folder.
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

    def run(self, args: List[str]):
        """
        Runs given operation.
        :param args: The command-line args.
        :type args: List[str]
        :return: A tuple containing the return code, the stdout, and the stderr.
        :rtype: tuple(int, str, str)
        """
        result = (None, None, None)

        home_path = os.environ.get("HOME")

        custom_env = {
            "GIT_CONFIG_GLOBAL": os.path.join(home_path, ".gitconfig-UnveilingPartner"),
            "GIT_CONFIG_NOSYSTEM": "true",
            **dict(os.environ),  # Include existing environment variables
        }

        completed_process = subprocess.run(
            args,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=self.folder,
            env=custom_env,
        )

        return (
            completed_process.returncode,
            completed_process.stdout,
            completed_process.stderr,
        )
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
