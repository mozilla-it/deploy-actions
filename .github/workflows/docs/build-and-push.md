# Docker Build and Push Reusable Workflow

This reusable GitHub Actions workflow encapsulates an end-to-end process for building and pushing a
container image for a MozCloud service.

The inputs of this workflow are mostly used to configure [`docker-build`](../docker-build/README.md) 
and [`docker-push`](../docker-push/README.md). See their documentation for more details on some of 
these inputs.

## Overview

- Runs a `prebuild_script` to prepare the build environment (e.g. generate `version.json`)
- Builds and tags the Docker image using [`docker-build`](../docker-build/README.md)
- Provides an optional hook to run a `postbuild_script` after building (e.g. for running tests)
- Pushes the image to GCP Artifact Registry (and optionally GitHub Container Registry) using [docker-push](../docker-push/README.md)


## Inputs

| Name                                    | Required | Type    | Description                                                                                                     |
| --------------------------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------- |
| `image_name`                            | true     | string  | The name of the Docker image to build.                                                                          |
| `gar_name`                              | true     | string  | Name of the GAR repository. (typically `<tenant>-prod`)                                                         |
| `project_id`                            | true     | string  | GCP project ID where the Artifact Registry is located. (typically `moz-fx-<tenant>-prod`)                       |
| `workload_identity_pool_project_number` | false    | string  | GCP workload identity pool project number. (default: `${{ vars.GCPV2_WORKLOAD_IDENTITY_POOL_PROJECT_NUMBER }}`) |
| `prebuild_script`                       | false    | string  | Shell script (either inline or path to script) to run before building the image. (default: *see below)*         |
| `postbuild_script`                      | false    | string  | Shell script (either inline or path to script) to run after building the image.                                 |
| `image_build_context`                   | false    | string  | Build context path. (default: `"./"`)                                                                           |
| `image_tag_metadata`                    | false    | string  | Additional metadata for image tagging.                                                                          |
| `should_tag_ghcr`                       | false    | boolean | Whether to also tag and push the image to GHCR. (default: `false`)                                              |
| `should_tag_latest`                     | false    | boolean | Whether to tag the image as `latest`. (default: `false`)                                                        |
| `gar_location`                          | false    | string  | Artifact Registry location. (default: `"us"`)                                                                   |
| `service_account_name`                  | false    | string  | GCP service account for pushing to registry. (default: `"artifact-writer"`)                                     |

### Default `prebuild_script`

```bash
IMAGE_BUILD_CONTEXT_ABSPATH=$(realpath "$IMAGE_BUILD_CONTEXT")

printf '{"commit":"%s","version":"%s","source":"%s","build":"%s"}\n' \
"$GITHUB_SHA" \
"$GITHUB_REF_NAME" \
"$GITHUB_SERVER_URL/$GITHUB_REPOSITORY" \
"$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID" > "$IMAGE_BUILD_CONTEXT_ABSPATH/version.json"
```

This script generates a `version.json` file with commit, version, and build metadata.

## Permissions

- `contents: read` (required)
- `id-token: write` (required: for GCP authentication)
- `packages: write` (optional: for GHCR publishing)

## Usage

### Minimal configuration
```yaml
on:
  push:
    branches:
      - main
    tags:
      - v20[0-9][0-9].[01][0-9].[0-3][0-9]  # e.g. v2023.12.04
      - v20[0-9][0-9].[01][0-9].[0-3][0-9]-[0-9]  # e.g. v2023.12.04-2

jobs:
  build-and-push:
    secrets: inherit
    permissions:
      contents: read
      id-token: write
    uses: mozilla-it/deploy-actions/.github/workflows/build-and-push.yml@main
    with:
      image_name: your-service
      gar_name: your-tenant-prod
      project_id: moz-fx-you-tenant-prod
```

### Push to GHCR
```yaml
on:
  push:
    branches:
      - main
    tags:
      - v20[0-9][0-9].[01][0-9].[0-3][0-9]  # e.g. v2023.12.04
      - v20[0-9][0-9].[01][0-9].[0-3][0-9]-[0-9]  # e.g. v2023.12.04-2

jobs:
  build:
    secrets: inherit
    permissions:
      contents: read
      id-token: write
      packages: write
    uses: mozilla-it/deploy-actions/.github/workflows/build-and-push.yml@main
    with:
      image_name: your-service
      gar_name: your-tenant-prod
      project_id: moz-fx-you-tenant-prod
      should_tag_ghcr: true
```
