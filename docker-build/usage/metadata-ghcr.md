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
