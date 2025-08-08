# docker-build

This GitHub Action is designed to build a Docker container image, providing standard MozCloud tags for supported registries. It outputs a list of images in `image_tags` to be consumed by the [docker-push](../docker-push/README.md) action

## Inputs

| Name                  | Required | Description                                                                                                                                                                                |
| --------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `image_name`          | Yes      | Name to give to the built image                                                                                                                                                            |
| `gar_name`            | Yes      | Name of the GAR repository (typically `<tenant name>-prod`)                                                                                                                                |
| `project_id`          | Yes      | GCP project ID (typically `moz-fx-<tenant name>-prod`)                                                                                                                                     |
| `image_build_context` | No       | Path to the Docker build context. Default value is a path relative to the repository root (default: `./`)                                                                                  |
| `dockerfile_path`     | No       | Path to the Dockerfile used to build the image. Default value is a path relative to the repository root (default: `./Dockerfile`)                                                          |
| `gar_location`        | No       | GCP region where GAR is located (default: `us`)                                                                                                                                            |
| `should_tag_ghcr`     | No       | Whether or not to generate image tags for Github Container Registry (default: `false`)                                                                                                     |
| `should_tag_latest`   | No       | Whether or not to tag the image(s) as `latest` (default: `false`)                                                                                                                          |
| `image_tag_metadata`  | No       | Metadata to append to the image tag.<br><br>For example, for a workflow triggered by a git tag `v1.2.3` and an `image_tag_metadata` value `dev`, the final image tag will be `v1.2.3--dev` |

## Outputs

| Name         | Description                                             |
| ------------ | ------------------------------------------------------- |
| `image_tags` | A newline-delimited list of generated Docker image tags |

## Example

### Usage

This example demonstrates how to build a Docker container image for a service named `my-service`. The image is:

- Tagged with metadata indicating the target deployment environment (e.g., `dev`, `stage`, `prod`).
- Tagged so that it can be published to both Google Artifact Registry and GitHub Container Registry.

```yaml
- uses: mozilla-it/deploy-actions/docker-build@v4
  with:
    image_name: my-service
    gar_name: tenant-prod
    project_id: moz-fx-tenant-prod
    image_tag_metadata: ${{ steps.preflight.outputs.deployment-env }} # resolves to `dev` for the purposes of this example
    should_tag_ghcr: true
```

### Outputs

Assumes image was built in the repo `mozilla/my-repo`, triggered by pushing a tag `v1.0.0`

#### `image_tags`

```
ghcr.io/mozilla/my-repo/my-service:v1.0.0--dev
us-docker.pkg.dev/moz-fx-tenant-prod/tenant-prod/my-service:v1.0.0--dev
```
