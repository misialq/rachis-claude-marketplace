# QIIME 2 Plugin Template Fields

Source: `https://github.com/caporaso-lab/plugin-template/blob/main/copier.yaml`  
Retrieved: March 1, 2026

Use this file when you need the current Copier answer keys for the QIIME 2 plugin template.

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
  Default: `https://example.com`
  Purpose: Main plugin website.

- `plugin_description`
  Default: `A QIIME 2 plugin template.`
  Purpose: Longer description shown when plugin information is requested.

- `plugin_short_description`
  Default: `Plugin template.`
  Purpose: Shorter description shown in lists.

- `target_distro`
  Default: `tiny`
  Choices: `tiny`, `amplicon`, `metagenome`
  Purpose: Target QIIME 2 distribution.

- `license`
  Default: `skip-license`
  Choices: `BSD-3-Clause`, `MIT`, `Apache-2.0`, `skip-license`
  Purpose: License selection. `skip-license` leaves room for a custom license or retaining all rights.

## Direct Copier Pattern

```bash
copier copy --vcs-ref HEAD --defaults \
  --data package_name=q2-my-plugin \
  --data module_name=q2_my_plugin \
  --data plugin_name=my-plugin \
  --data author_name="Your Name" \
  --data author_email="you@example.com" \
  --data project_url="https://example.com/q2-my-plugin" \
  --data plugin_description="Longer plugin description." \
  --data plugin_short_description="Short plugin description." \
  --data target_distro=tiny \
  --data license=BSD-3-Clause \
  https://github.com/caporaso-lab/plugin-template \
  /path/to/destination
```
