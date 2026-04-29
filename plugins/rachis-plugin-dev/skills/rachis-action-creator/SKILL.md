---
name: rachis-action-creator
description: Extend an existing QIIME 2 plugin by adding a new method or visualizer
---

# QIIME 2 Action Creator

## Overview

Add a CLI-backed action to an existing QIIME 2 plugin. Retrieve the current QIIME 2 developer docs before editing, then inspect the target plugin's structure and use [references/action-patterns.md](references/action-patterns.md) for the method, visualizer, registration, and testing patterns.

## Workflow

1. Retrieve the current QIIME 2 developer docs, starting with `https://develop.qiime2.org/en/stable/plugins/intro.html`. Retrieve the method or visualizer tutorial page that matches the requested action type.
2. Inspect the plugin package for `plugin_setup.py`, existing action modules such as `_methods.py` or `_visualizers.py`, relevant type or format definitions, and the current test layout. Also inspect `pyproject.toml` to confirm the `[qiime2.plugins]` entry point and the project's declared dependencies.
3. Discover the available QIIME 2 semantic types before choosing input and output types. Browse `q2-types` (https://github.com/qiime2/q2-types) and check what the target plugin already imports from `qiime2.plugin` and `q2_types`. Prefer types that already appear in the plugin over inventing new ones.
4. Decide the action kind before editing:
   - Use a method when the action should return one or more artifacts.
   - Use a visualizer when the action should write report files into `output_dir`, return `None` and create a visual output.
5. Read [references/action-patterns.md](references/action-patterns.md). Reuse the method or visualizer skeleton there instead of rewriting the `subprocess.run` pattern from scratch.
6. Add the external package to `conda-recipe/meta.yaml` or `meta.yml` if the plugin repo maintains one.
7. Implement the callable in the appropriate module. Keep command construction explicit, pass arguments as a list, avoid `shell=True`, and convert external-tool failures into clear Python exceptions.
8. Register the callable in `plugin_setup.py` with matching imports, input or parameter or output types, descriptions, and citations. Follow the import pattern in [references/action-patterns.md](references/action-patterns.md) to ensure all types and semantic primitives are imported correctly.
9. Add a citation entry in `citations.bib` when the wrapped tool has a paper or required citation text. Follow the BibTeX pattern in [references/action-patterns.md](references/action-patterns.md).
10. Add or update tests. Cover success-path output handling and at least one failure case for the external command. Add a small synthetic dataset which is well suited for a human visual inspection and use it in an integration test.
11. Validate registration by importing the plugin module in a Python shell or running `qiime <plugin-name> --help` and confirming the new action appears.
12. Keep file names and API style aligned with the plugin's existing conventions. If the plugin does not already have a `_visualizers.py` module or visualization tests, create them only when the new action requires them.
13. Create a conda environment using one of the environment files but install the plugin from the current working directory using pip rather than point to a GitHub repository (it may not exist yet). Never modify existing conda environments.
14. Run `qiime dev refresh-cache` in that environment followed by `qiime <plugin-name> --help`. Make sure that the returned action list contains the new action.

## Implementation Notes

- Preserve the plugin's existing package structure and naming. Prefer editing the plugin's established action modules over inventing a new layout.
- Use `pyproject.toml` as the single source of truth for the `[qiime2.plugins]` entry point. Do not use `setup.py`. Use `conda-recipe/meta.yaml` or `meta.yml` if the plugin repo maintains one for the source of truth for dependencies. If not present, use the latest environment file from the `environment-files` directory.
- Treat the external executable as an environment dependency, not a runtime discovery problem. Prefer packaging fixes in `conda-recipe/meta.yaml` or `meta.yml` (if present) as well as environment files in the `environment-files` directory over adding `shutil.which` guards.
- Prefer small, typed helper functions around serialization and command execution when the external tool needs several files.
- When the tool expects file paths instead of in-memory views, stage inputs in a temporary working directory and load outputs back into the declared QIIME 2 return type.
- When the tool produces visualization assets, write final files into the provided `output_dir`. Use a temporary directory only for intermediate files.
- Prefer mocking `subprocess.run` in unit tests unless the user explicitly wants end-to-end coverage against a real executable.

## References

- Read [references/action-patterns.md](references/action-patterns.md) for reusable code skeletons, registration snippets, citation format, and test guidance.
- Refresh the QIIME 2 docs if the user asks to target a newer developer guide revision or if the local plugin uses APIs newer than the captured examples.
