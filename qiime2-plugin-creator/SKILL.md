---
name: qiime2-plugin-creator
description: Scaffold new QIIME 2 plugins from the caporaso-lab/plugin-template with Copier. Use when an agent needs to create, bootstrap, or regenerate a QIIME 2 plugin project, map user-provided answers onto the template's Copier fields, install Copier if it is missing, or run the template non-interactively with explicit answer data.
---

# QIIME 2 Plugin Creator

## Overview

Create a new QIIME 2 plugin project from `https://github.com/caporaso-lab/plugin-template` with Copier. Prefer the bundled script for non-interactive scaffolding, and read [references/template-fields.md](references/template-fields.md) when you need the current answer keys, defaults, or allowed values.

## Workflow

1. Confirm the destination path for the new plugin project.
2. Read [references/template-fields.md](references/template-fields.md) and collect any values the user wants to override. Leave `module_name` and `plugin_name` unset unless the user wants something different from the template-derived defaults.
3. Check whether Copier is installed with `command -v copier`. If it is missing, install it with `python3 -m pip install copier`.
4. Prefer `scripts/create_qiime2_plugin.py` for execution. It installs Copier if needed and translates CLI options into repeated `copier copy --data` flags.
5. Use `--dry-run` before creating files when the destination is sensitive or the answers may be wrong. Use `--force` only when the user explicitly wants existing files overwritten.

## Execution

Run the helper script from the skill directory:

```bash
python3 scripts/create_qiime2_plugin.py /path/to/destination \
  --package-name q2-my-plugin \
  --author-name "Your Name" \
  --author-email "you@example.com" \
  --project-url "https://example.com/q2-my-plugin" \
  --plugin-description "Longer plugin description." \
  --plugin-short-description "Short plugin description." \
  --target-distro tiny \
  --license BSD-3-Clause
```

The script resolves template defaults locally, passes all known fields explicitly, and adds `--defaults` so new upstream fields fall back to their Copier defaults instead of prompting interactively.

If the helper script is not appropriate, run Copier directly:

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

## References

- Read [references/template-fields.md](references/template-fields.md) for the current field list captured from the upstream `copier.yaml` on March 1, 2026.
- Refresh that reference if the user asks to align the skill with newer upstream template changes.

## Resources

- Use `scripts/create_qiime2_plugin.py` to scaffold a plugin repository from the template without interactive prompts.
- Use `references/template-fields.md` to inspect field meanings, defaults, derived values, and valid choices before running Copier.
