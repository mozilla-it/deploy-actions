#!/usr/bin/env python3

import click, jwt, requests, time, json, os
from cryptography.hazmat.backends import default_backend


@click.group()
@click.option(
    "--key",
    "-k",
    help="Private key of github app",
    envvar="PRIVATE_KEY",
    default="/app/key.pem",
    show_default=True,
)
@click.option(
    "--repo",
    "-r",
    help="Github repository being deployed",
    default="fxa",
    show_default=True,
)
@click.option(
    "--organization",
    "-o",
    help="Github organization containing repository",
    default="mozilla",
    show_default=True,
)
@click.option(
    "--app_id",
    help="Application ID of Github App with deployment and release permissions in desired repository",
    envvar="APPLICATION_ID",
    required=True,
)
@click.option(
    "--install_id",
    help="Installation ID of Github App installed in desired repository",
    envvar="INSTALLATION_ID",
    required=True,
)
def main(key, repo, organization, app_id, install_id):
    if key.endswith('.pem'):
      keyfile = open(key, 'r').read()
      private_pem = keyfile.encode()
    else:
      private_pem = key.encode()

    main.private_key = default_backend().load_pem_private_key(private_pem, None)
    main.gh_repo = repo
    main.gh_org = organization
    main.gh_app_id = app_id
    main.installation_id = install_id
    pass


def get_token():
    payload = {
        # issued at time, 60 seconds in the past to allow for clock drift
        "iat": int(time.time()),
        # JWT expiration time (10 minute maximum)
        "exp": int(time.time()) + (10 * 60),
        # GitHub App identifier
        "iss": main.gh_app_id,
    }

    bearer = jwt.encode(payload, main.private_key, algorithm="RS256")
    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/vnd.github.machine-man-preview+json",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        f"https://api.github.com/app/installations/{main.installation_id}/access_tokens",
        headers=headers,
    )
    content_json = json.loads(resp.content.decode())

    return content_json["token"]


def get_headers():
    headers = {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github.machine-man-preview+json",
        "Content-Type": "application/json",
    }
    return headers


def create_release(tag):
    data = f'{{"tag_name": "{tag}", "name": "{tag}", "prerelease": true, "generate_release_notes": true}}'
    resp = requests.post(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/releases",
        headers=get_headers(),
        data=data,
    )

    content_json = json.loads(resp.content.decode())
    return content_json


def get_release(tag):
    resp = requests.get(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/releases/tags/{tag}",
        headers=get_headers(),
    )
    content_json = json.loads(resp.content.decode())
    if resp.status_code == 404:
        return False
    else:
        return content_json["id"]


@click.command()
@click.option(
    "--environment",
    "-e",
    default="staging",
    help="Deployment environment: (development|staging|production)",
    show_default=True,
)
@click.option(
    "--tag", "-t", help="Git tag being deployed: (1.224.1|1.228.0)", required=True
)
def update_release(tag, environment):
    release_id = get_release(tag)

    if not release_id:
        tag_content = create_release(tag)
        print(tag_content["html_url"])
        return tag_content

    if environment == "production":
        data = '{"prerelease": false}'
    else:
        data = '{"prerelease": true}'

    resp = requests.patch(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/releases/{release_id}",
        headers=get_headers(),
        data=data,
    )
    content_json = json.loads(resp.content.decode())
    print(content_json["html_url"])
    return resp.status_code


@click.command()
@click.option("--release-id", help="Release ID", required=True)
def delete_release(release_id):
    resp = requests.delete(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/releases/{release_id}",
        headers=get_headers(),
    )
    return resp.status_code


def create_deployment(tag, environment):
    data = f'{{"ref": "{tag}", "environment": "{environment}", "task":"deploy", "auto_merge": false, "required_contexts": [] }}'

    resp = requests.post(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/deployments",
        headers=get_headers(),
        data=data,
    )
    content_json = json.loads(resp.content.decode())
    if resp.status_code == 200:
        return content_json["id"]
    else:
        return content_json


def get_deployment(tag, environment):
    resp = requests.get(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/deployments",
        headers=get_headers(),
    )
    content_json = json.loads(resp.content.decode())
    try:
        matching_deployment = next(
            deployment
            for deployment in content_json
            if (deployment["environment"] == environment and deployment["ref"] == tag)
        )
        deployment_id = matching_deployment["id"]
    except StopIteration:
        deployment_id = ""

    return deployment_id


@click.command()
@click.option(
    "--tag", "-t", help="Git tag being deployed: (1.224.1|1.228.0)", required=True
)
@click.option(
    "--environment",
    "-e",
    default="staging",
    help="Deployment environment: (staging|production)",
    show_default=True,
)
@click.option(
    "--state",
    "-s",
    default="in_progress",
    help="Deployment state: (in_progress|success|failed)",
    show_default=True,
)
@click.option(
    "--environment_url",
    "-u",
    default="https://mozilla.org",
    help="Environment url: ex. (https://accounts.firefox.com)",
    show_default=False,
)
def update_deployment(tag, environment, environment_url, state="in_progress"):
    deployment_id = get_deployment(tag, environment)

    if not deployment_id:
        create_deployment(tag, environment)
        deployment_id = get_deployment(tag, environment)

    data = f'{{"environment": "{environment}", "state": "{state}", "environment_url": "{environment_url}" }}'

    resp = requests.post(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/deployments/{deployment_id}/statuses",
        headers=get_headers(),
        data=data,
    )
    content_json = json.loads(resp.content.decode())
    print(content_json)
    return resp.status_code


@click.command()
def get_all_releases():
    resp = requests.get(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/releases",
        headers=get_headers(),
    )
    content_json = json.loads(resp.content.decode())
    print(f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/releases")
    print(content_json)


@click.command()
def get_all_deployments():
    resp = requests.get(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/deployments",
        headers=get_headers(),
    )
    content_json = json.loads(resp.content.decode())
    print(content_json)


@click.command()
@click.option("--deployment-id", help="Deployment ID", required=True)
def delete_deployment(deployment_id):
    resp = requests.delete(
        f"https://api.github.com/repos/{main.gh_org}/{main.gh_repo}/deployments/{deployment_id}",
        headers=get_headers(),
    )

    return resp.status_code


# Adding commands to main
main.add_command(update_deployment)
main.add_command(update_release)
main.add_command(get_all_deployments)
main.add_command(get_all_releases)
main.add_command(delete_deployment)
main.add_command(delete_release)


if __name__ == "__main__":
    main()
