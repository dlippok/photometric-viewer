---
name: prepare-release
description: Prepare a Photometry application release by reviewing changes, choosing or confirming a version, updating release metadata, and validating the release. Use when asked to prepare, stage, or bump a new release version.
---

# Prepare a release

Prepare release changes in the current working tree. Do not publish a GitHub release, create or push a tag, or commit unless the user explicitly asks.

## Workflow

1. Inspect `git status`, the latest version tag, and commits since that tag. Preserve unrelated work and review the actual changes before drafting release notes. The repository uses `v<major>.<minor>.<patch>` tags and Semantic Versioning.
2. Determine the version increment from the changes: patch for compatible fixes, minor for backward-compatible features, major for incompatible changes. If the impact or target version cannot be established confidently, ask the user before changing release files.
3. If not yet happened, create a git branch `release-v<major>.<minor>.<patch>` derived from the master branch. This will be used for creating a pull request at a later stage.
4. Check whether the release changes affect the UI or otherwise make the current screenshots inaccurate. If new screenshots are needed, ask the user to provide/update them and pause the release workflow here. Do not edit release metadata until the screenshots have been updated.
5. Update the version in `setup.py` and add the new release as the first entry in `data/io.github.dlippok.photometric-viewer.metainfo.xml`. Use the release date in `YYYY-MM-DD` format and concise notes that accurately describe shipped changes. Keep the existing English, German, and Polish release-note paragraphs; do not invent translations or claim unverified changes. Ask for missing release-note details or translations when needed.
6. Check the rest of the repository for other application-version references and update only those that genuinely represent the application version. In particular, `snapcraft.yaml` reads the AppStream metadata via `parse-info`, and `flatpak.yaml` builds from the source tree; do not change runtime versions as part of an application release.
7. Validate with `make test` and, when available, `appstream-util validate-relax data/io.github.dlippok.photometric-viewer.metainfo.xml`. Review the final diff for version consistency, release-note accuracy, and unrelated edits. Report any validation tool that was unavailable or failed.
8. Prepare a pull request from the release branch into `master` with the version and AppStream release-note changes. Use a concise title identifying the release version and include a summary and validation results in the description. Do not merge the pull request.

Leave publishing and distribution tasks (tagging, GitHub release creation, and store submissions) for a separate explicitly requested step.
