# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_clone.py

This file declares the GitClone class.

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
from .git_clone_failed import GitCloneFailed
from .git_operation import GitOperation


class GitClone(GitOperation):
    """
    Clones git repositories.

    Class name: GitClone

    Responsibilities:
        - Represents the clone operation in git.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitClone instance for given folder.
        :param folder: The folder to host the cloned repository.
        :type folder: str
        """
        super().__init__(folder, False)

    def clone(self, url: str, subfolder: str = None):
        """
        Clones this repo.
        :param url: The repository url.
        :type url: str
        :param subfolder: An optional subfolder.
        :type subfolder: str
        """
        args = ["git", "clone", url]

        if subfolder:
            args.append(subfolder)

        (code, stdout, stderr) = self.run(args)
        if code != 0:
            if stderr != "":
                GitClone.logger().error(stderr)
            if stdout != "":
                GitClone.logger().error(stdout)
            raise GitCloneFailed(self.folder, stderr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
