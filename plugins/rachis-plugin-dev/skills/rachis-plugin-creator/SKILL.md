---
name: rachis-plugin-creator
description: Scaffold new QIIME 2 plugins from the official template
---

# QIIME 2 Plugin Creator

## Overview

Create a new QIIME 2 plugin project by writing files directly from the bundled template. No external tools (Copier, cookiecutter, etc.) are required — read the template reference and write each file with the user's values substituted in.

## Workflow

1. Confirm the destination path for the new plugin project.
2. Read [references/template-fields.md](references/template-fields.md) and collect any values the user wants to override. Apply the derivation rules for `module_name` and `plugin_name` unless the user provides explicit values.
3. Read [references/plugin-template.md](references/plugin-template.md) for the complete file structure and contents.
4. Create every directory and file listed in the template, substituting `{field_name}` placeholders with the resolved values. Pay close attention to:
   - File and directory names that contain `{package_name}`, `{module_name}`, or `{target_distro}`.
   - The `LICENSE` file: only populate it if the user chose `BSD-3-Clause`, `MIT`, or `Apache-2.0`. For `skip-license`, create an empty `LICENSE` file.
   - The `pyproject.toml` `[tool.versioningit.format]` section uses literal double braces (`{base_version}`, `{distance}`, etc.) — these are NOT template variables.
   - The `ci.yml` GitHub Actions workflow uses `${{ matrix.os }}` etc. — write these literally, they are GitHub Actions expressions.
   - Do NOT create `.copier-answers.yml` — it is a Copier artifact and is not needed.
5. Copy the binary test fixture `static/table-1.biom` into `{module_name}/tests/data/table-1.biom` in the generated project.
6. Create a conda environment using one of the environment files but install the plugin from the current working directory using pip rather than point to a GitHub repository (it may not exist yet). Never modify existing conda environments.
7. Run `qiime dev refresh-cache` in that environment followed by `qiime info`. Make sure that the returned plugin list contains the new plugin.
8. Initialize a git repository in the new project directory with `git init` and create an initial commit.

## References

- [references/template-fields.md](references/template-fields.md) — field names, defaults, derivation rules, and allowed values.
- [references/plugin-template.md](references/plugin-template.md) — complete file structure and contents for the plugin scaffold.

## Resources

- `static/table-1.biom` — binary BIOM test fixture to copy into generated projects.
