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
from git import Repo
import os
from pythoneda import attribute, BaseObject
from pythoneda.shared.git import GitTagFailed
import re
import semver
import subprocess
from typing import Dict

class GitTag(BaseObject):
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
        self._repo = Repo(folder)

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

    def create_tag(self, tag: str, message:str="no message") -> bool:
        """
        Creates a tag in a local repository.
        :param tag: The tag to create.
        :type tag: str
        :param message: A message.
        :type message: str
        :return: True if the operation succeeds.
        :rtype: bool
        :raise pythoneda.shared.git.GitTagFailed: If the tag fails.
        """
        try:
            subprocess.run(
                ["git", "tag", "-m", message, tag],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                cwd=self.folder,
            )
        except subprocess.CalledProcessError as err:
            GitTag.logger().error(err.stdout)
            GitTag.logger().error(err.stderr)
            raise GitTagFailed(tag, self.folder)

        return True

    def latest_tag(self) -> str:
        """
        Retrieves the latest tag.
        :return: Such name.
        :rtype: str
        """
        result = None
        versions = []
        for tag in self._repo.tags:
            try:
                version_info = semver.VersionInfo.parse(tag.name)
                build = 0
                match = re.search(r"\+build\.(\d+)", tag.name)
                if match:
                    build = int(match.group(1))

                versions.append((version_info, build, tag.name))
            except ValueError:
                pass

        if versions:
            versions.sort(key=lambda v: (v[0], v[1]), reverse=True)
            result = versions[0][2]

        return result
