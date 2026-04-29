# QIIME 2 Action Patterns

## Source Docs

Use these official QIIME 2 pages as the source of truth. The patterns below were refreshed on March 3, 2026.

- Intro: `https://develop.qiime2.org/en/stable/plugins/intro.html`
- Create a method: `https://develop.qiime2.org/en/stable/plugins/tutorials/add-nw-align-method.html`
- Create a visualizer: `https://develop.qiime2.org/en/stable/plugins/tutorials/add-alignment-visualizer.html`

## Plugin GitHub References

Browse these repos to discover available semantic types, formats, and registration patterns before writing new code. Prefer reusing types and formats that already exist over defining new ones.

- **q2-types** — https://github.com/qiime2/q2-types — primary source of semantic types (`FeatureTable`, `FeatureData`, `SampleData`, etc.) and their format classes
- **q2-feature-table** — https://github.com/qiime2/q2-feature-table — reference for `FeatureTable`-based methods and registration style
- **q2-diversity** — https://github.com/qiime2/q2-diversity — reference for methods that produce distance matrices and visualizers that call emperor
- **q2-dada2** — https://github.com/qiime2/q2-dada2 — reference for subprocess-heavy methods that call external R or compiled tools
- **q2-vsearch** — https://github.com/qiime2/q2-vsearch — reference for wrapping a Unix CLI tool with multiple input/output artifacts
- **q2-cutadapt** — https://github.com/qiime2/q2-cutadapt — reference for per-sample subprocess dispatch and `SampleData` handling
- **q2-feature-classifier** — https://github.com/qiime2/q2-feature-classifier — reference for methods with large model artifacts
- **q2-phylogeny** — https://github.com/qiime2/q2-phylogeny — reference for tools that consume and produce tree artifacts
- **q2-taxa** — https://github.com/qiime2/q2-taxa — reference for taxonomy-related types and barplot visualizers
- **q2-emperor** — https://github.com/qiime2/q2-emperor — reference for visualizers that embed interactive HTML output
- **q2-annotate** — https://github.com/bokulich-lab/q2-annotate — reference for shotgun metagenomics methods with a lot of action examples

## Decide the Action Kind

- Use a method when the external tool should produce data that the plugin returns as one or more artifacts.
- Use a visualizer when the external tool should produce a visual output. QIIME 2 visualizer callables take `output_dir` as the first argument and return `None`.

## Package Checklist

Inspect and update only the files the target plugin already uses:

- `pyproject.toml` — entry point and project metadata (single source of truth; do not use `setup.py`)
- `plugin_setup.py`
- `_methods.py` for methods
- `_visualizers.py` for visualizers
- `tests/test_methods.py` or `tests/test_visualizers.py`
- `conda-recipe/meta.yaml` or `conda-recipe/meta.yml`
- `citations.bib` when the external tool or paper should be cited

If a plugin does not already have `_visualizers.py` or visualization tests, create them only when the new action is a visualizer.

## Type Discovery

Before choosing input and output types, look up what is available:

1. Check `q2-types` at https://github.com/qiime2/q2-types — scan `q2_types/` subdirectories for semantic type definitions.
2. Grep the target plugin's `plugin_setup.py` for existing imports from `q2_types` and `qiime2.plugin` to see which types are already in use.
3. Prefer types the plugin already imports. Only introduce a new type or format if nothing suitable exists.

Common types and their import origins:

```python
from qiime2.plugin import Int, Str, Float, Bool, Choices, Range, Metadata

from q2_types.feature_table import FeatureTable, Frequency, RelativeFrequency
from q2_types.feature_data import FeatureData, Sequence, Taxonomy, AlignedSequence
from q2_types.sample_data import SampleData, SequencesWithQuality, PairedEndSequencesWithQuality
from q2_types.tree import Phylogeny, Rooted, Unrooted
from q2_types.distance_matrix import DistanceMatrix
from q2_types.ordination import PCoAResults
```

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
- Add `tool-name` to `pyproject.toml` dependencies (and `conda-recipe/meta.yaml` or `meta.yml` if present) instead of probing for it with `shutil.which`.

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

## Registration Pattern

Import the new callable in `plugin_setup.py`. Always import types explicitly — do not rely on star imports.

```python
# plugin_setup.py — imports section (add only what the new action needs)
from qiime2.plugin import Int, Str, Citations

from q2_types.feature_table import FeatureTable, Frequency

from my_plugin._methods import run_external_tool
from my_plugin._visualizers import render_external_tool
```

Register with the matching action collection:

```python
citations = Citations.load("citations.bib", package="my_plugin")

plugin.methods.register_function(
    function=run_external_tool,
    inputs={"table": FeatureTable[Frequency]},
    parameters={"threads": Int % Range(1, None)},
    outputs=[("filtered_table", FeatureTable[Frequency])],
    input_descriptions={"table": "Input table to pass to tool-name."},
    parameter_descriptions={"threads": "Number of worker threads."},
    output_descriptions={"filtered_table": "Processed output from tool-name."},
    name="Run tool-name",
    description="Run tool-name on an input table and return the processed table.",
    citations=[citations["tool_name_paper_2020"]],
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
    citations=[citations["tool_name_paper_2020"]],
)
```

Checklist:

- Match the Python callable signature to the registered inputs and parameters.
- Use `plugin.methods.register_function` for methods and `plugin.visualizers.register_function` for visualizers.
- Import every type used in registration explicitly at the top of `plugin_setup.py`.
- Add a citation entry when the wrapped tool has a paper or required citation text.
- Declare the external package in `pyproject.toml` (and `conda-recipe/meta.yaml` or `meta.yml` if present).
- Preserve the plugin's naming and description style.

## Citation Pattern

Add an entry to `citations.bib` for the wrapped tool. Use the BibTeX key that matches what you pass to `citations[...]` in `plugin_setup.py`. Avoid including abstracts or other non-essential information. Validate the existence of the DOI or URL.

```bibtex
@article{tool_name_paper_2020,
  author  = {Author, First and Author, Second},
  title   = {Tool-name: a tool for doing the thing},
  journal = {Journal Name},
  year    = {2020},
  volume  = {1},
  pages   = {1--10},
  doi     = {10.0000/placeholder},
}
```

If the tool has no paper, omit the citation entry and pass `citations=[]` in the registration call.

## pyproject.toml Entry Point

The plugin must declare itself as a QIIME 2 plugin entry point in `pyproject.toml`. Confirm this exists before adding new dependencies; add it if missing.

```toml
[project]
name = "my-plugin"

[project.entry-points."qiime2.plugins"]
my-plugin = "my_plugin.plugin_setup:plugin"
```

Do not use `setup.py` for entry-point or dependency declaration.

## Testing Pattern

- Test the Python callable directly first.
- Mock `subprocess.run` for unit coverage of command construction and error handling.
- Assert that expected temp-file outputs are loaded or copied into the declared return location.
- Add a failure-path test that proves `CalledProcessError` becomes a useful `RuntimeError`.
- Run a real executable only when the user explicitly wants an integration test and the dependency is available in the environment.
- Never create data on the fly. Always create and reuse data files.

```python
from unittest.mock import patch, MagicMock
import pytest


def test_run_external_tool_success(tmp_path):
    mock_result = MagicMock(returncode=0, stdout="", stderr="")
    with patch("my_plugin._methods.subprocess.run", return_value=mock_result) as mock_run:
        # call the function with a test view ...
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "tool-name"
        assert "--threads" in cmd


def test_run_external_tool_failure():
    import subprocess
    with patch("my_plugin._methods.subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["tool-name"], stderr="something went wrong"
        )
        with pytest.raises(RuntimeError, match="tool-name failed"):
            run_external_tool(input_view=..., threads=1)
```

## Validation

After registration, verify the action is discoverable before finishing:

```bash
# Import the plugin module — any registration error surfaces here
python -c "import my_plugin.plugin_setup"

# Confirm the action appears in the CLI
qiime my-plugin --help
```

If either command fails, fix the registration error before closing the task.
