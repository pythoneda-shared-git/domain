# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_push_tags_failed.py

This file defines the GitPushTagsFailed exception class.

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
from pythoneda.shared import BaseObject


class GitPushTagsFailed(Exception, BaseObject):
    """
    Running git push --tags failed.

    Class name: GitPushTagsFailed

    Responsibilities:
        - Represent the error when running git push --tags.

    Collaborators:
        - None
    """

    def __init__(self, folder: str):
        """
        Creates a new GitPushTags instance.
        :param folder: The folder with the cloned repository.
        :type folder: str
        """
        super().__init__(f'"git push --tags" in folder {folder} failed')
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
