---
name: rachis-unit-test-writer
description: Write or update unit tests for QIIME 2 plugin code.
---

# QIIME 2 Unit Test Writer

## Overview

Add or update unit tests for QIIME 2 plugin code by mirroring the local repo's test style instead of writing generic pytest tests. Inspect the nearest existing tests first, then use [references/qiime2-test-patterns.md](references/qiime2-test-patterns.md) to match the conventions captured from `q2-annotate` (https://github.com/bokulich-lab/q2-annotate). Use when Codex needs to add tests for a module, method, function, pipeline, helper, or regression in a QIIME 2 plugin repo, especially when the repo expects TestPluginBase, reusable fixtures under tests/data, patched external APIs or command-line tools, and targeted pytest runs in a dedicated conda environment.

## Workflow

1. Inspect the code under test, the nearest existing `test_*.py` files, the package's `tests/data/` directory, and the repo's `environment-files/` directory before editing.
2. Discover the target conda environment by inspecting `environment-files/`. Prefer the most recent development environment file (e.g. `environment-files/<package>-qiime2-<epoch>-py<ver>-<platform>-conda.yml`). Extract the environment name from the `name:` field at the top of that file.
3. Prefer extending an existing package-specific test module. Create a new `test_*.py` only when there is no natural home for the new coverage.
4. Subclass test classes from `qiime2.plugin.testing.TestPluginBase`. Set `package = "<package_path>.tests"` so `self.get_data_path(...)` resolves fixtures.
5. Choose the right shared-state hook:
   - Use `setUp` when each test needs its own isolated copy of a fixture or mock — `setUp` runs before every test method.
   - Use `setUpClass` only for expensive, read-only shared state (e.g., loading a large artifact once) that is safe to share across all tests in the class.
6. Reuse or add stable fixture files under the matching `tests/data/` directory. Treat reusable files as the default for inputs and expected outputs.
7. Patch every external boundary:
   - Patch command execution such as `subprocess.run` or the repo's command wrapper unless the user explicitly asks to test the command execution.
   - Patch network or remote API calls such as `requests.get`.
   - Patch plugin actions, renderers, copy helpers, or filesystem side effects when the code under test delegates to them.
   - Patch at the lookup site used by the module under test, not at an arbitrary import path.
8. Assert behavior precisely. Prefer explicit command-list assertions, `assert_has_calls`, output type checks, dataframe equality checks, existence checks for materialized files, and `assertRaisesRegex` for failure paths.
9. Keep tests narrow. Cover the requested behavior, one or more edge cases, and at least one failure path when the code wraps an external tool or remote call.
10. Prepare the conda environment and run the new tests. If an environment matching the discovered name already exists, use it as-is — never modify it. If it does not exist, create it from the environment file and install the plugin from the current working directory. Follow the execution and iteration steps in the **Test Execution** section below.

## Rules

- Use `TestPluginBase` for unit tests in this style, even for helper-focused tests, unless the user explicitly asks to follow a different house style.
- Use `self.get_data_path(...)` instead of hard-coding fixture paths.
- Prefer `setUp` for per-test isolation; use `setUpClass` only for read-only shared state that is safe to reuse across all tests.
- Use `self.plugin.methods[...]` or `self.plugin.pipelines[...]` when testing registered plugin actions instead of reimplementing plugin wiring.
- Never create input fixture content on the fly inside a test when a reusable file in `tests/data/` can represent it.
- Use temporary directories only for outputs, staging, or code paths that inherently require a temporary working directory.
- Never hit the network or execute real external tools in unit tests.
- Preserve the module's local naming, import style, and assertion style when it already matches the surrounding repo.

## Test Execution

### Environment setup

Discover the environment name from `environment-files/` as described in step 2, then:

- **If the environment already exists** — use it as-is. Never modify an existing conda environment.
- **If the environment does not exist** — create it from the environment file, then install the plugin from the current working directory:

```bash
conda env create -f environment-files/<env-file>.yml
conda run -n <env-name> pip install -e . --no-deps --no-build-isolation
```

Only run the `pip install` step again if `pyproject.toml` dependencies change after the environment was created.

### Running tests

Always start with the narrowest possible selection and widen only after the target tests pass:

```bash
# Single test
conda run -n <env-name> python -m pytest path/to/test_file.py::TestClass::test_name -x --tb=short -v

# Full test class
conda run -n <env-name> python -m pytest path/to/test_file.py::TestClass -x --tb=short -v

# Full test file
conda run -n <env-name> python -m pytest path/to/test_file.py -x --tb=short -v

# Full package test suite (only after the above pass)
conda run -n <env-name> python -m pytest path/to/tests/ --tb=short
```

Use `-x` (fail fast) and `--tb=short` while iterating. Switch to `--tb=long` only when a traceback is too truncated to diagnose.

### Iteration loop

1. Run the narrowest relevant selection.
2. If a test fails, read the full traceback before making changes.
   - If the failure is in the test itself (wrong mock target, wrong assertion, missing fixture), fix the test.
   - If the failure exposes a real bug in the implementation, report it to the user before touching production code.
3. Fix one issue at a time. Re-run the same narrow selection after each fix.
4. Once all target tests pass, widen to the full test file, then the full package suite, to confirm nothing was broken.

## References

- Read [references/qiime2-test-patterns.md](references/qiime2-test-patterns.md) before writing tests. It points at concrete `q2-annotate` examples and highlights patterns to copy versus legacy patterns to avoid.
