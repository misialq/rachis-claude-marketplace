# QIIME 2 Plugin Template Fields

Source: `https://github.com/caporaso-lab/plugin-template`
Retrieved: April 5, 2026

## Fields

- `package_name`
  Default: `q2-hello-world`
  Purpose: Package name used as the top-level directory name.

- `module_name`
  Default: `package_name` with `-` replaced by `_`
  Purpose: Python module name.
  Constraint: Must be a valid Python identifier.

- `plugin_name`
  Default: `package_name` with a leading `q2-` removed
  Purpose: Shorter QIIME 2 plugin name.

- `author_name`
  Default: `A QIIME 2 Plugin Developer`
  Purpose: Author name.

- `author_email`
  Default: `q2-dev@example.com`
  Purpose: Author email.

- `project_url`
  Default: `https://github.com`
  Purpose: Main plugin website.

- `plugin_description`
  Default: `A QIIME 2 plugin template.`
  Purpose: Longer description shown when plugin information is requested.

- `plugin_short_description`
  Default: `Plugin template.`
  Purpose: Shorter description shown in lists.

- `target_distro`
  Default: `tiny`
  Choices: `tiny`, `amplicon`, `moshpit`
  Purpose: Target QIIME 2 distribution.

- `license`
  Default: `skip-license`
  Choices: `BSD-3-Clause`, `MIT`, `Apache-2.0`, `skip-license`
  Purpose: License selection. `skip-license` leaves room for a custom license or retaining all rights.
