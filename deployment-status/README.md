# GitHub Deployment/Release Script

This action is used to manage github deployments and releases on a target repository

ex. https://github.com/mozilla/fxa/deployments & https://github.com/mozilla/fxa/releases

## Inputs

### `command`

The command to run. Supported values delete-deployment, delete-release, get-all-deployments, get-all-releases, update-deployment, update-release. Default `"update-deployment"`

### `github_org`

The GitHub organization hosting the target repository. Default `"mozilla"`

### `repository`

**Required** The GitHub repository to target.

### `environment_url`

The environment URL to set in the deployment request. 

### `state`

The deployment state. Supported values in_progress, success, failed. Default `"in_progress"`

### `environment`

The target deployment environment. Default `"staging"`

### `ref`

**Required** The git ref being deployed from the target repository.

### Example usage
```
name: github-deployment-update

on:
  workflow_dispatch:
    inputs:
      state:
        type: string
        default: "in_progress"
      environment:
        description: "Target deployment environment"
        type: string
        default: "staging"
      ref: 
        description: "Deployed git ref"
        required: true
        default: "v1.269.2"

env:
  APPLICATION_ID: ${{ secrets.APPLICATION_ID }}
  INSTALLATION_ID: ${{ secrets.INSTALLATION_ID }}
  PRIVATE_KEY: ${{ secrets.PRIVATE_KEY }}

jobs:
  update_deployment_job:
    permissions:
      contents: read
      id-token: write
    runs-on: ubuntu-latest
    steps:
      - name: Set repository deployment status
        uses: mozilla-it/deploy-actions/deployment-status@v4.0.0
        with:
          repository: fxa
          environment_url: "https://accounts.stage.mozaws.net/__version__"
          state: ${{ github.event.inputs.state }}
          environment: ${{ github.event.inputs.environment }}
          ref: ${{ github.event.inputs.ref }}
```


### Required Secrets

A GitHub app with the permissions to create/modify deployments and/or releases on the target repositories must be created to use this function. The following secrets are also required to be passed in as environment variables:

- `APPLICATION_ID` - The application ID of the required GitHub app

- `INSTALLATION_ID` - The installation ID of the GitHub app installed in the target repository

- `PRIVATE_KEY` - The private key of the required GitHub app