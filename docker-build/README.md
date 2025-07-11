<!-- This document is automatically generated -- Do Not edit by hand! -->
# docker-build

Build a Docker container image, providing standard MozCloud tags for supported registries. Outputs a
newline-delimited list of images in `image_tags` to be consumed by the
[docker-push](../docker-push/README.md) action.


## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `image_name` | Name to give to the built image | True | |
| `gar_name` | Name of the GAR repository | True | |
| `project_id` | GCP project ID | True | |
| `image_build_context` | Path to the Docker build context | False | `./`|
| `gar_location` | GCP region where GAR is located | False | `us`|
| `should_tag_ghcr` | Whether or not to generate image tags for GitHub Container Registry | False | `false`|
| `should_tag_latest` | Whether or not to tag the image(s) as `latest` | False | `false`|
| `image_tag_metadata` | Metadata to append to the image tag. For example, for a workflow triggered by a git tag `v1.2.3` and an `image_tag_metadata` value `dev`, the final  image tag will be `v1.2.3--dev`. | False | |



## Outputs

| Name | Description |
|------|-------------|
| `image_tags` | A newline-delimited list of generated Docker image tags |


## Example Usage
### Minimal Configuration
```yaml
- uses: mozilla-it/deploy-actions/docker-build
  with:
    image_name: my-service
    gar_name: tenant-prod
    project_id: moz-fx-tenant-prod
```

### Minimal Configuration with Defaults
```yaml
- uses: mozilla-it/deploy-actions/docker-build
  with:
    image_name: my-service
    gar_name: tenant-prod
    project_id: moz-fx-tenant-prod
    image_build_context: ./
    gar_location: us
    should_tag_ghcr: false
    should_tag_latest: false
```


### Custom Usage Examples
Note that these examples are maintained by hand, unlike the examples above that are automatically
generated, and as a result may drift out of date. Always consult the input and output sections for
an up to date usage spec.

#### Tag Metadata and GHCR
In this example, the image is:
- Tagged with metadata indicating the target deployment environment (e.g., `dev`, `stage`, `prod`).
- Tagged so that it can be published to both Google Artifact Registry and GitHub Container Registry.

##### Inputs
```yaml
- uses: mozilla-it/deploy-actions/docker-build
  with:
    image_name: my-service
    gar_name: tenant-prod
    project_id: moz-fx-tenant-prod
    image_tag_metadata: ${{ steps.preflight.outputs.deployment-env }} # resolves to `dev` for the purposes of this example
    should_tag_ghcr: true
```

##### Outputs

Assumes image was built in the repo `mozilla/my-repo`, triggered by pushing a tag `v1.0.0`

###### `image_tags`

```
ghcr.io/mozilla/my-repo/my-service:v1.0.0--dev
us-docker.pkg.dev/moz-fx-tenant-prod/tenant-prod/my-service:v1.0.0--dev
```
