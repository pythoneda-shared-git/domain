"""
pythoneda/shared/git/git_tag.py

This file declares the GitTag class.

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
import logging
import os
from pythoneda import attribute
from pythoneda.shared.git import GitTagFailed
import re
import semver
import subprocess
from typing import Dict

class GitTag():
    """
    Provides git operations related to tags.

    Class name: GitTag

    Responsibilities:
        - Provides the "git tag" operation.

    Collaborators:
        - None
    """
    def __init__(self, folder: str):
        """
        Creates a new GitTag instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__()
        self._folder = folder

    @property
    @attribute
    def folder(self) -> str:
        """
        Retrieves the folder of the cloned repository.
        :return: Such folder.
        :rtype: str
        """
        return self._folder

    def create_tag(self, tag: str) -> bool:
        """
        Creates a tag in a local repository.
        :param localRepo: The cloned repository.
        :type localRepo: str
        :param tag: The tag to create.
        :type tag: str
        :return: True if the operation succeeds.
        :rtype: bool
        """
        print(f'Creating tag {tag} in {self._folder}')
        try:
            subprocess.run(
                ["git", "tag", tag],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                cwd=self._folder,
            )
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise GitTagFailed(tag, self.folder)
        print('done')
        return True
