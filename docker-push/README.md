# docker-push

This GitHub Action is designed to push Docker images to Google Artifact Registry (GAR) and optionally GitHub Container Registry (GHCR).

## Inputs

| Name                                    | Required | Description                                                                                                                                                                                                                                                                       |
| --------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `project_id`                            | Yes      | GCP `project_id` used to construct the service account                                                                                                                                                                                                                            |
| `image_tags`                            | Yes      | Newline-delimited list of images to be pushed.<br> Typically generated by [`mozilla-it/deploy-actions/docker-build`](../docker-build/README.md), but may also be provided manually. See [GAR][1] and [GHCR][2] documentation for how to tag images for these supported registries |
| `workload_identity_pool_project_number` | Yes      | Project number of the workload identity pool used for OIDC authentication. Should be available as the variable `vars.GCPV2_WORKLOAD_IDENTITY_POOL_PROJECT_NUMBER`                                                                                                                 |
| `should_authenticate_to_ghcr`           | No       | Whether or not to authenticate to GitHub Container Registry. Set this to `true` if one of the image tags includes `ghcr.io` (default: `false`)                                                                                                                                    |
| `service_account_name`                  | No       | Service account used to authenticate to GAR. (default: `artifact-writer`)                                                                                                                                                                                                         |
| `gar_location`                          | No       | GCP region where the target GAR is located (default: `us`)                                                                                                                                                                                                                        |

[1]: https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling#tag
[2]: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images

## Example Usage

```yaml
- name: Push Docker image to GAR and GHCR
  uses: mozilla-it/deploy-actions/docker-push@v4
  with:
    # typically provided from another step's output
    image_tags: |
      ghcr.io/mozilla/my-repo/my-service:v1.0.0
      us-docker.pkg.dev/moz-fx-tenant-prod/tenant-prod/my-service:v1.0.0
    should_authenticate_to_ghcr: true
    project_id: moz-fx-tenant-prod
    workload_identity_pool_project_number: ${{ vars.GCPV2_WORKLOAD_IDENTITY_POOL_PROJECT_NUMBER }}
```
