"""GitHub app common module."""

import logging

from github.GithubException import UnknownObjectException

from apps.github.models.issue import Issue
from apps.github.models.label import Label
from apps.github.models.organization import Organization
from apps.github.models.release import Release
from apps.github.models.repository import Repository
from apps.github.models.user import User
from apps.github.utils import check_owasp_site_repository

logger = logging.getLogger(__name__)


def sync_repository(gh_repository, organization=None, user=None):
    """Sync GitHub repository data."""
    entity_key = gh_repository.name.lower()
    is_owasp_site_repository = check_owasp_site_repository(entity_key)

    # GitHub repository organization.
    if organization is None:
        gh_organization = gh_repository.organization
        if gh_organization is not None:
            organization = Organization.update_data(gh_organization)

    # GitHub repository owner.
    if user is None:
        user = User.update_data(gh_repository.owner)

    # GitHub repository.
    commits = gh_repository.get_commits()
    contributors = gh_repository.get_contributors()
    languages = None if is_owasp_site_repository else gh_repository.get_languages()

    repository = Repository.update_data(
        gh_repository,
        commits=commits,
        contributors=contributors,
        languages=languages,
        organization=organization,
        user=user,
    )

    # GitHub repository issues.
    if not repository.is_archived:
        # Sync open issues for the first run.
        kwargs = {
            "direction": "asc",
            "sort": "created",
            "state": "open",
        }
        latest_issue = Issue.objects.filter(repository=repository).order_by("-updated_at").first()
        if latest_issue:
            # Sync open/closed issues for subsequent runs.
            kwargs.update(
                {
                    "since": latest_issue.updated_at,
                    "state": "all",
                }
            )
        for gh_issue in gh_repository.get_issues(**kwargs):
            # Skip pull requests.
            if gh_issue.pull_request:
                continue

            # GitHub issue author.
            if gh_issue.user is not None:
                author = User.update_data(gh_issue.user)

            issue = Issue.update_data(gh_issue, author=author, repository=repository)

            # Assignees.
            issue.assignees.clear()
            for gh_issue_assignee in gh_issue.assignees:
                issue.assignees.add(User.update_data(gh_issue_assignee))

            # Labels.
            issue.labels.clear()
            for gh_issue_label in gh_issue.labels:
                try:
                    issue.labels.add(Label.update_data(gh_issue_label))
                except UnknownObjectException:
                    logger.info("Couldn't get GitHub issue label %s", issue.url)

    # GitHub repository releases.
    releases = []
    if not is_owasp_site_repository:
        existing_release_node_ids = set(
            Release.objects.filter(repository=repository).values_list("node_id", flat=True)
            if repository.id
            else ()
        )
        for gh_release in gh_repository.get_releases():
            release_node_id = Release.get_node_id(gh_release)
            if release_node_id in existing_release_node_ids:
                break

            # GitHub release author.
            if gh_release.author is not None:
                author = User.update_data(gh_release.author)

            # GitHub release.
            releases.append(Release.update_data(gh_release, author=author, repository=repository))

    return organization, repository, releases