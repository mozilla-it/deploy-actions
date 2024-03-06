# Render and diff helm charts

This action is used to render helm charts on the base and ref branches of a pull request, create a diff between charts that have been modified and then post the diff as a comment on the pull request. 

## Inputs

### `chart_path`

The path filter for helm charts in the repository. Default `'**/k8s/**/**'`

### Example usage
```
name: render-and-diff-charts

on:
  pull_request:
    paths:
      - '**/k8s/**/**'

jobs:
  run_helm_chart_diff:
    permissions:
      contents: read
      pull-requests: write
    runs-on: ubuntu-latest
    steps:
      - name: Render and diff modified helm charts
        uses: mozilla-it/deploy-actions/deployment-status@v3.9.0
```