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
from .git_operation import GitOperation
from .git_tag_failed import GitTagFailed
from .invalid_github_credentials import InvalidGithubCredentials
from packaging import version
import re
import requests
import semver


class GitTag(GitOperation):
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
        super().__init__(folder)

    def create_tag(self, tag: str, message: str = "no message") -> bool:
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
        (code, stdout, stderr) = self.run(["git", "tag", "-m", message, tag])
        if code != 0:
            GitTag.logger().error(stderr)
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
        for tag in self.repo.tags:
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

    def current_tag(self) -> str:
        """
        Retrieves the current tag, i.e., the most recent tag pointing to the
        same commit as HEAD.
        :return: The current tag.
        :rtype: str
        """
        result = None

        # Get the commit object for HEAD
        head_commit = self.repo.head.commit

        # Initialize variables to keep track of the most recent tag and its commit date
        most_recent_date = None

        # Iterate through the tags
        for tag_ref in self.repo.tags:
            # Get the commit object for the tag
            tag_commit = tag_ref.commit

            # Check if the tag points to the same commit as HEAD
            if tag_commit == head_commit and self.is_valid_version(tag_ref.name):
                # Update the most recent tag and date if this tag is more recent
                if (
                    most_recent_date is None
                    or tag_commit.committed_datetime > most_recent_date
                ):
                    result = tag_ref.name
                    most_recent_date = tag_commit.committed_datetime

        return result

    def is_valid_version(self, tag: str) -> bool:
        """
        Checks if given tag is a valid version according to semantic versioning.
        :param tag: The tag to check.
        :type tag: str
        :return: True if it's a valid version.
        :rtype: bool
        """
        result = False
        try:
            semver.parse(tag)
            result = True
        except ValueError:
            result = False

        return result

    @classmethod
    def latest_github_tag(cls, token: str, owner: str, repo: str, hashValue: str) -> str:
        """
        Retrieves the highest gitHub tag pointing to given hash.
        :param token: The gitHub token.
        :type token: str
        :param owner: The repository owner.
        :type owner: str
        :param repo: The repository name.
        :type repo: str
        :param hashValue: The commit hash.
        :type hashValue: str
        :return: The highest tag pointing to given commit, or None if none found.
        :rtype: Union(str,None)
        """
        result = None
        # GitHub API URL for tags
        url = f"https://api.github.com/repos/{owner}/{repo}/tags"

        # Headers for authentication
        headers = {"Authorization": f"token {token}"}

        # Fetch the tags
        response = requests.get(url, headers=headers)
        tags = response.json()

        if (
            isinstance(tags, dict)
            and tags.get("message", None) == "Bad credentials"
        ):
            GitTag.logger().error("Invalid credentials")
            raise InvalidGithubCredentials(url)

        # Filter tags pointing to the commit
        commit_tags = [tag for tag in tags if tag["commit"]["sha"] == hashValue]

        # Parse versions and sort them
        valid_versions = []
        for tag in commit_tags:
            try:
                # Append the parsed version
                valid_versions.append(version.parse(tag["name"]))
            except version.InvalidVersion:
                # Ignore invalid semantic versions
                pass

        # Sort versions
        valid_versions.sort()

        # Highest version
        if valid_versions:
            result = valid_versions[-1]

        return result
