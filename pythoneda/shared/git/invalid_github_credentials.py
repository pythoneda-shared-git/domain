# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/invalid_github_credentials.py

This file defines the InvalidGithubCredentials exception class.

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


class InvalidGithubCredentials(Exception, BaseObject):
    """
    Access to GitHub API was denied.

    Class name: InvalidGithubCredentials

    Responsibilities:
        - Represent the error when access to GitHub API was rejected.

    Collaborators:
        - None
    """

    def __init__(self, url: str):
        """
        Creates a new InvalidGithubCredentials instance.
        :param url: The url of the API.
        :type url: str
        """
        super().__init__(f"Bad credentials accessing {url}")
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
