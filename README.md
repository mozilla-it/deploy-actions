# Mozilla Deployment GitHub Actions

This repository contains GitHub Actions Composite Actions used for Deployment Automation.

## Actions
* [`docker-build`](./docker-build/README.md)
* [`docker-push`](./docker-push//README.md)

## Workflows
* [build-and-push](./reusable-workflow-docs/build-and-push.md)


## Releases & Tags

Releases follow semantic versioning. Tags additionally provide "generic" versions (e.g. `v2`, `v3`) to allow specifying "moving" pointers in github actions (e.g. `mozilla-it/deploy-actions/slack@v3`.
