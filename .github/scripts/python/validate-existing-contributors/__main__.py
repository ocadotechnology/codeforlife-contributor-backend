"""
© Ocado Group
Created on 08/01/2024 at 09:47:25(+00:00).

Validate all contributors have signed the contribution agreement.
"""

import json
import os
import typing as t

import requests

# TODO: figure out the right import later
# from .....api.models import AgreementSignature  # type: ignore


PullRequest = t.Dict[str, t.Any]
Contributors = t.Set[str]

BOTS = {
    "49699333+dependabot[bot]@users.noreply.github.com",
    "codeforlife-bot@ocado.com",
}

# Information about the repo
GH_ORG = "ocadotechnology"
GH_REPO = "codeforlife-workspace"
GH_FILE = "CONTRIBUTING.md"


def get_inputs():
    """Get script's inputs.

    Returns:
        A JSON object of the pull request.
    """

    pull_request: PullRequest = json.loads(os.environ["PULL_REQUEST"])

    return pull_request


def get_signed_contributors() -> Contributors:
    """Get the latest commit hash/ID of the contributor agreement,
       and return the contributors that have signed that contribution agreement.

    Returns:
        A set of the contributors' email addresses.
    """

    # Get the latest commit hash/ID of the contributor agreement,
    param: t.Dict[str, t.Any] = {"path": GH_FILE, "per_page": 1}
    response = requests.get(
        url=f"https://api.github.com/repos/{GH_ORG}/{GH_REPO}/commits",
        headers={"X-GitHub-Api-Version": "2022-11-28"},
        params=param,
        timeout=5,
    )
    if not response.ok:
        response.raise_for_status()
        data = response.json()
        print("ERROR: ", data)
        return set()

    latest_commit_id = response.json()[0]["sha"]

    # TODO: Uncomment this when database is created
    # signed_contributors = AgreementSignature.objects.filter(
    #     latest_commit_id=latest_commit_id
    # )

    # contributors_emails = {
    #     contributor.contributor.email.lower()
    #     for contributor in signed_contributors
    # }
    # return contributors_emails

    # TODO: remove dummy data once database is set up
    dummy_signed_contributors = {"salman.ashraf2513@gmail.com"}
    return dummy_signed_contributors


def assert_contributors(
    pull_request: PullRequest,
    signed_contributors: Contributors,
):
    """Assert that all contributors have signed the contribution agreement.

    Args:
        pull_request: The JSON object of the pull request.
        signed_contributors: The contributors that have signed the contribution
            agreement.
    """

    contributors: Contributors = {
        author["email"].lower()
        for commit in pull_request["commits"]
        for author in commit["authors"]
    }

    unsigned_contributors = contributors.difference(
        signed_contributors.union(BOTS),
    )

    assert not unsigned_contributors, (
        "The following contributors have not signed the agreement:"
        f" {', '.join(unsigned_contributors)}."
    )


def main():
    """Entry point."""

    pull_request = get_inputs()

    signed_contributors = get_signed_contributors()

    assert_contributors(pull_request, signed_contributors)


if __name__ == "__main__":
    main()
