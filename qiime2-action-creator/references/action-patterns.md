# QIIME 2 Action Patterns

## Source Docs

Use these official QIIME 2 pages as the source of truth. The patterns below were refreshed on March 3, 2026.

- Intro: `https://develop.qiime2.org/en/stable/plugins/intro.html`
- Create a method: `https://develop.qiime2.org/en/stable/plugins/tutorials/create-method/`
- Create a visualizer: `https://develop.qiime2.org/en/stable/plugins/tutorials/create-visualizer/`

## Decide the Action Kind

- Use a method when the external tool should produce data that the plugin returns as one or more artifacts.
- Use a visualizer when the external tool should produce files for a visualization. QIIME 2 visualizer callables take `output_dir` as the first argument and return `None`.

## Package Checklist

Inspect and update only the files the target plugin already uses:

- `plugin_setup.py`
- `_methods.py` for methods
- `_visualizers.py` for visualizers
- `tests/test_methods.py` or `tests/test_visualizers.py`
- `conda-recipe/meta.yaml` or `conda-recipe/meta.yml` for the external package dependency
- `citations.bib` when the external tool or paper should be cited

If a plugin does not already have `_visualizers.py` or visualization tests, create them only when the new action is a visualizer.
If a plugin has both a conda recipe and environment files, keep them consistent.

## Method Skeleton

Use this pattern when the tool consumes files and returns data:

```python
from pathlib import Path
import subprocess
import tempfile


def run_external_tool(input_view, threads: int = 1):
    with tempfile.TemporaryDirectory(prefix="q2-tool-") as tmpdir:
        tmpdir = Path(tmpdir)
        input_path = tmpdir / "input.ext"
        output_path = tmpdir / "output.ext"

        write_input_view(input_view, input_path)

        cmd = [
            "tool-name",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--threads",
            str(threads),
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.strip() or exc.stdout.strip()
            raise RuntimeError(
                f"tool-name failed with exit code {exc.returncode}: {detail}"
            ) from exc

        return read_output_view(output_path)
```

Notes:

- Keep `cmd` as a list of strings.
- Avoid `shell=True`.
- Put view-to-file and file-to-view logic in focused helpers such as `write_input_view` and `read_output_view`.
- Add `tool-name` to `conda-recipe/meta.yaml` or `meta.yml` instead of probing for it with `shutil.which`.

## Visualizer Skeleton

Use this pattern when the tool writes reports or plots:

```python
from pathlib import Path
import shutil
import subprocess
import tempfile


def render_external_tool(output_dir: str, input_view, title: str = "Report") -> None:
    final_dir = Path(output_dir)
    final_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="q2-tool-") as tmpdir:
        tmpdir = Path(tmpdir)
        input_path = tmpdir / "input.ext"
        staged_output_dir = tmpdir / "report"
        staged_output_dir.mkdir()

        write_input_view(input_view, input_path)

        cmd = [
            "tool-name",
            "--input",
            str(input_path),
            "--output-dir",
            str(staged_output_dir),
            "--title",
            title,
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.strip() or exc.stdout.strip()
            raise RuntimeError(
                f"tool-name failed with exit code {exc.returncode}: {detail}"
            ) from exc

        shutil.copytree(staged_output_dir, final_dir, dirs_exist_ok=True)
```

Notes:

- Keep `output_dir` as the first parameter.
- Write final visualization assets into `output_dir`.
- Use a temporary directory only for intermediate files or tool staging.
- Add the executable's package to the conda recipe instead of adding preflight PATH checks.

## Registration Pattern

Import the new callable in `plugin_setup.py` and register it with the matching action collection:

```python
plugin.methods.register_function(
    function=run_external_tool,
    inputs={"table": FeatureTable[Frequency]},
    parameters={"threads": Int},
    outputs=[("filtered_table", FeatureTable[Frequency])],
    input_descriptions={"table": "Input table to pass to tool-name."},
    parameter_descriptions={"threads": "Number of worker threads."},
    output_descriptions={"filtered_table": "Processed output from tool-name."},
    name="Run tool-name",
    description="Run tool-name on an input table and return the processed table.",
    citations=[],
)
```

```python
plugin.visualizers.register_function(
    function=render_external_tool,
    inputs={"table": FeatureTable[Frequency]},
    parameters={"title": Str},
    input_descriptions={"table": "Input table to render."},
    parameter_descriptions={"title": "Title to embed in the report."},
    name="Render tool-name report",
    description="Run tool-name and write its visualization assets.",
    citations=[],
)
```

Checklist:

- Match the Python callable signature to the registered inputs and parameters.
- Use `plugin.methods.register_function` for methods and `plugin.visualizers.register_function` for visualizers.
- Add a citation entry when the wrapped tool has a paper or required citation text.
- Declare the external package in `conda-recipe/meta.yaml` or `meta.yml`.
- Preserve the plugin's naming and description style.

## Testing Pattern

- Test the Python callable directly first.
- Mock `subprocess.run` for unit coverage of command construction and error handling.
- Assert that expected temp-file outputs are loaded or copied into the declared return location.
- Add a failure-path test that proves `CalledProcessError` becomes a useful `RuntimeError`.
- Run a real executable only when the user explicitly wants an integration test and the dependency is available in the environment.
