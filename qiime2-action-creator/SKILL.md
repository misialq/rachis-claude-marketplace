---
name: qiime2-action-creator
description: Extend an existing QIIME 2 plugin by adding a new method or visualizer that wraps an external command-line tool. Use when Codex needs to inspect an existing plugin package, implement a Python callable that invokes a third-party executable with subprocess.run, stage data through temporary files or output_dir, register the action in plugin_setup.py, and add or update tests for the new action.
---

# QIIME 2 Action Creator

## Overview

Add a CLI-backed action to an existing QIIME 2 plugin. Retrieve the current QIIME 2 developer docs before editing, then inspect the target plugin's structure and use [references/action-patterns.md](references/action-patterns.md) for the method, visualizer, registration, and testing patterns.

## Workflow

1. Retrieve the current QIIME 2 developer docs, starting with `https://develop.qiime2.org/en/stable/plugins/intro.html`. Retrieve the method or visualizer tutorial page that matches the requested action type.
2. Inspect the plugin package for `plugin_setup.py`, existing action modules such as `_methods.py` or `_visualizers.py`, relevant type or format definitions, and the current test layout.
3. Decide the action kind before editing:
   - Use a method when the action should return one or more artifacts.
   - Use a visualizer when the action should write report files into `output_dir` and return `None`.
4. Read [references/action-patterns.md](references/action-patterns.md). Reuse the method or visualizer skeleton there instead of rewriting the `subprocess.run` pattern from scratch.
5. Add the external package to the plugin's packaging metadata before writing the action implementation. Prefer `conda-recipe/meta.yaml`; if the project uses `meta.yml` instead, update that file. Keep any environment files aligned if the plugin repo maintains them.
6. Implement the callable in the appropriate module. Keep command construction explicit, pass arguments as a list, avoid `shell=True`, and convert external-tool failures into clear Python exceptions.
7. Register the callable in `plugin_setup.py` with matching imports, input or parameter or output types, descriptions, and citations.
8. Add or update tests. Cover success-path output handling and at least one failure case for the external command.
9. Keep file names and API style aligned with the plugin's existing conventions. If the plugin does not already have a `_visualizers.py` module or visualization tests, create them only when the new action requires them.

## Implementation Notes

- Preserve the plugin's existing package structure and naming. Prefer editing the plugin's established action modules over inventing a new layout.
- Treat the external executable as an environment dependency, not a runtime discovery problem. Prefer packaging fixes in `conda-recipe/meta.yaml` or `meta.yml` over adding `shutil.which` guards.
- Prefer small, typed helper functions around serialization and command execution when the external tool needs several files.
- When the tool expects file paths instead of in-memory views, stage inputs in a temporary working directory and load outputs back into the declared QIIME 2 return type.
- When the tool produces visualization assets, write final files into the provided `output_dir`. Use a temporary directory only for intermediate files.
- Prefer mocking `subprocess.run` in unit tests unless the user explicitly wants end-to-end coverage against a real executable.

## References

- Read [references/action-patterns.md](references/action-patterns.md) for reusable code skeletons, registration snippets, and test guidance.
- Refresh the QIIME 2 docs if the user asks to target a newer developer guide revision or if the local plugin uses APIs newer than the captured examples.
