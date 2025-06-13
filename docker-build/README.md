# docker-build

Build a MozCloud service image

## Inputs

| Name                  | Required | Description                                                                                                                                                                               |
| --------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_name`          | Yes      | Name to give to the built image                                                                                                                                                           |
| `gar_location`        | Yes      | GCP region where GAR is located (default: `us`)                                                                                                                                           |
| `gar_name`            | Yes      | Name of the GAR repository                                                                                                                                                                |
| `project_id`          | Yes      | GCP project ID                                                                                                                                                                            |
| `image_build_context` | Yes      | Path to the Docker build context (default: `./`)                                                                                                                                          |
| `image_tag_metadata`  | No       | Metadata to append to the image tag.<br><br>For example, for a workflow triggred by a git tag `v1.2.3` and an `image_tag_metadata` value `dev`, the final image tag will be `v1.2.3--dev` |
| `should_tag_ghcr`     | No       | Whether or not to generate image tags for Github Container Registry (default: `false`)                                                                                                    |
| `should_tag_latest`   | No       | Whether or not to tag the image(s) as `latest` (default: `false`)                                                                                                                         |

## Outputs

| Name         | Description                                  |
| ------------ | -------------------------------------------- |
| `image_tags` | The list of generated Docker images and tags |

## Example

```yaml
- uses: mozilla/deploy-actions/docker-build@v4
  with:
    image_name: my-service
    gar_name: tenant-prod
    project_id: moz-fx-tenant-prod
    image_tag_metadata: dev
    should_tag_ghcr: true
```
