# QIIME 2 Plugin Template

Source: `https://github.com/caporaso-lab/plugin-template`
Retrieved: April 5, 2026

This document contains the complete file structure and contents for a QIIME 2 plugin scaffold. Variable placeholders use the names from [template-fields.md](template-fields.md).

## Directory Structure

```
{package_name}/
├── .gitattributes
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── environment-files/
│   ├── {package_name}-qiime2-{target_distro}-dev.yml
│   └── {package_name}-qiime2-{target_distro}-release.yml
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
├── setup.cfg
└── {module_name}/
    ├── __init__.py
    ├── _methods.py
    ├── citations.bib
    ├── plugin_setup.py
    └── tests/
        ├── __init__.py
        ├── test_methods.py
        └── data/
            └── table-1.biom   (binary — copy from static/table-1.biom)
```

---

## File Contents

### `.gitattributes`

```
pyproject.toml export-subst
```

### `.gitignore`

```
# This .gitignore file is derived from:
# https://github.com/github/gitignore/blob/4488915eec0b3a45b5c63ead28f286819c0917de/Python.gitignore

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
# .python-version

# pipenv
#Pipfile.lock

# poetry
#poetry.lock

# pdm
#pdm.lock
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# macOS
.DS_Store

# Version file from versioningit
_version.py
```

### `.github/workflows/ci.yml`

```yaml
name: Test build

on:
  pull_request:
    branches: ["main"]
  push:
    branches: ["main"]

jobs:
  build-q2-{plugin_name}:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-15-intel]

    steps:
    - name: checkout source
      uses: actions/checkout@v6.0.2

    - name: set up python 3.12
      uses: actions/setup-python@v6.2.0
      with:
        python-version: 3.12

    - name: install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -q flake8
        pip install -q https://github.com/qiime2/q2lint/archive/master.zip

    - name: Set up Conda
      uses: qiime2-cutlery/setup-miniconda@v3
      with:
        activate-environment: {package_name}-qiime2-{target_distro}-dev
        environment-file: environment-files/{package_name}-qiime2-{target_distro}-dev.yml
        auto-activate-base: false

    - name: Install plugin
      shell: bash -l {0}
      run: |
        cd {package_name}
        make install

    - name: Call info on the deployment
      shell: bash -l {0}
      run: |
        qiime info

    - name: Call --help on plugin
      shell: bash -l {0}
      run: |
        qiime {plugin_name} --help

    - name: Test plugin
      shell: bash -l {0}
      run: |
        cd {package_name}
        make test

    - name: Lint plugin
      shell: bash -l {0}
      run: |
        cd {package_name}
        flake8
        q2lint
```

### `environment-files/{package_name}-qiime2-{target_distro}-dev.yml`

```yaml
channels:
- https://packages.qiime2.org/qiime2/latest/{target_distro}/passed
- conda-forge
- bioconda
dependencies:
  - qiime2-{target_distro}
  # Note 1: Add any additional conda dependencies here.
  - pip
  - pip:
  # Note 2: Add any additional pip dependencies here.
  #   - # some pip dependency
  # Note 3: If you host your repository on GitHub, and you uncomment and modify
  # the following lines to replace:
  # REPO-OWNER with the user or organization name that owns the repository
  # DEFAULT-BRANCH with the default branch of the repository (typically 'main')
  # Your installation commands can be updated to install
  # from this file without additional steps.
  #   - {package_name}@git+https://github.com/REPO-OWNER/{package_name}.git@DEFAULT-BRANCH
```

### `environment-files/{package_name}-qiime2-{target_distro}-release.yml`

```yaml
channels:
- https://packages.qiime2.org/qiime2/stable/{target_distro}/released
- conda-forge
- bioconda
dependencies:
  - qiime2-{target_distro}
  # Note 1: Add any additional conda dependencies here.
  - pip
  - pip:
  # Note 2: Add any additional pip dependencies here.
  #   - # some pip dependency
  # Note 3: If you host your repository on GitHub, and you uncomment and modify
  # the following lines to replace:
  # REPO-OWNER with the user or organization name that owns the repository
  # DEFAULT-BRANCH with the default branch of the repository (typically 'main')
  # Your installation commands can be updated to install
  # from this file without additional steps.
  #   - {package_name}@git+https://github.com/REPO-OWNER/{package_name}.git@DEFAULT-BRANCH
```

### `LICENSE`

Only created when the `license` field is set to `BSD-3-Clause`, `MIT`, or `Apache-2.0`. When set to `skip-license`, create an empty `LICENSE` file.

#### BSD-3-Clause

```
BSD 3-Clause License

Copyright (c) 2024, {author_name}.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

#### MIT

```
MIT License

Copyright (c) 2024, {author_name}.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

#### Apache-2.0

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   [Full Apache 2.0 text]
```

For Apache-2.0, use the standard full text from https://www.apache.org/licenses/LICENSE-2.0.txt.

### `Makefile`

```makefile
.PHONY: all lint test install dev clean distclean

PYTHON ?= python

all: ;

lint:
	q2lint
	flake8

test: all
	py.test

install: all
	$(PYTHON) -m pip install -v .

dev: all
	pip install -e .

clean: distclean

distclean: ;
```

### `setup.cfg`
```
[flake8]
max-line-length = 88
extend-ignore = E203

[tool.isort]
profile = "black"
```

### `pyproject.toml`

```toml
[project]
name = "{package_name}"
authors = [
    {{ name = "{author_name}", email = "{author_email}"}}
]
description = "{plugin_short_description}"
readme = {{file = "README.md", content-type = "text/markdown"}}
license = {{file = "LICENSE"}}
dynamic = ["version"]

[project.urls]
Homepage = "{project_url}"

[project.entry-points.'qiime2.plugins']
"{package_name}" = "{module_name}.plugin_setup:plugin"

[build-system]
requires = [
    "setuptools",
    "versioningit",
    "wheel"
]
build-backend = "setuptools.build_meta"

[tool.versioningit.vcs]
method = "git-archive"
describe-subst = "$Format:%(describe)$"
default-tag = "0.0.1"

[tool.versioningit.next-version]
method = "minor"

[tool.versioningit.format]
distance = "{{base_version}}+{{distance}}.{{vcs}}{{rev}}"
dirty = "{{base_version}}+{{distance}}.{{vcs}}{{rev}}.dirty"
distance-dirty = "{{base_version}}+{{distance}}.{{vcs}}{{rev}}.dirty"

[tool.versioningit.write]
file = "{module_name}/_version.py"

[tool.versioningit]
default-version = "0.0.dev0"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
where = ["."]
include = ["{module_name}*"]

[tool.setuptools.package-data]
{module_name} = ["**/*"]
```

Note: In the `pyproject.toml`, the double braces in the `[tool.versioningit.format]` section are literal — they are NOT template variables. Write them exactly as shown.

### `.copier-answers.yml`

Do NOT create this file. It is a Copier-specific metadata file used for template updates. Since we are no longer using Copier, it serves no purpose.

### `README.md`

```markdown
# {package_name}

A [QIIME 2](https://qiime2.org) plugin [developed](https://develop.qiime2.org) by {author_name} ({author_email}).

## Installation instructions

**The following instructions are intended to be a starting point** and should be replaced when `{package_name}` is ready to share with others.
They will enable you to install the most recent *development* version of `{package_name}`.
Remember that *release* versions should be used for all "real" work (i.e., where you're not testing or prototyping) - if there aren't instructions for installing a release version of this plugin, it is probably not yet intended for use in practice.

### Install Prerequisites

[Miniconda](https://conda.io/miniconda.html) provides the `conda` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of `conda`:

```bash
conda update conda
```

###  Install development version of `{package_name}`

Next, you need to get into the top-level `{package_name}` directory.
If you already have this (e.g., because you just created the plugin), this may be as simple as running `cd {package_name}`.
If not, you'll need the `{package_name}` directory on your computer.
How you do that will differ based on how the package is shared, and ideally the developer will update these instructions to be more specific (remember, these instructions are intended to be a starting point).
For example, if it's maintained in a GitHub repository, you can achieve this by [cloning the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
Once you have the directory on your computer, change (`cd`) into it.

If you're in a conda environment, deactivate it by running `conda deactivate`.


Then, follow the install instructions below, based on your machine's architecture:

<details>
<summary><strong>Apple Silicon (ARM)</strong></summary>
<p></p>

Start by creating a new conda environment:

```shell
CONDA_SUBDIR=osx-64 conda env create -n {package_name}-dev --file ./environment-files/{package_name}-qiime2-{target_distro}-dev.yml
```

After this completes, activate the new environment you created by running:

```shell
conda activate {package_name}-dev
```

Once this new environment has been activated, update your conda config to set the subdir to osx-64:

```shell
conda config --env --set subdir osx-64
```

Finally, run:

```shell
make install
```
</details>

<details>
<summary><strong>All other architectures (Apple Intel, Linux, WSL)</strong></summary>
<p></p>

Start by creating a new conda environment:

```shell
conda env create -n {package_name}-dev --file ./environment-files/{package_name}-qiime2-{target_distro}-dev.yml
```

After this completes, activate the new environment you created by running:

```shell
conda activate {package_name}-dev
```

Finally, run:

```shell
make install
```
</details>

## Testing and using the most recent development version of `{package_name}`

After completing the install steps above, confirm that everything is working as expected by running:

```shell
make test
```

You should get a report that tests were run, and you should see that all tests passed and none failed.
It's usually ok if some warnings are reported.

If all of the tests pass, you're ready to use the plugin.
Start by making QIIME 2's command line interface aware of `{package_name}` by running:

```shell
qiime dev refresh-cache
```

You should then see the plugin in the list of available plugins if you run:

```shell
qiime info
```

You should be able to review the help text by running:

```shell
qiime {plugin_name} --help
```

Have fun!

## About

The `{package_name}` Python package was [created from a template](https://develop.qiime2.org/en/stable/plugins/tutorials/create-from-template.html).
To learn more about `{package_name}`, refer to the [project website]({project_url}).
To learn how to use QIIME 2, refer to the [QIIME 2 User Documentation](https://docs.qiime2.org).
To learn QIIME 2 plugin development, refer to [*Developing with QIIME 2*](https://develop.qiime2.org).

`{package_name}` is a QIIME 2 community plugin, meaning that it is not necessarily developed and maintained by the developers of QIIME 2.
Please be aware that because community plugins are developed by the QIIME 2 developer community, and not necessarily the QIIME 2 developers themselves, some may not be actively maintained or compatible with current release versions of the QIIME 2 distributions.
More information on development and support for community plugins can be found [here](https://library.qiime2.org).
If you need help with a community plugin, first refer to the [project website]({project_url}).
If that page doesn't provide information on how to get help, or you need additional help, head to the [Community Plugins category](https://forum.qiime2.org/c/community-contributions/community-plugins/14) on the QIIME 2 Forum where the QIIME 2 developers will do their best to help you.
```

### `{module_name}/__init__.py`

```python
# flake8: noqa
# ----------------------------------------------------------------------------
# Copyright (c) 2024, {author_name}.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = '0.0.0+notfound'
```

### `{module_name}/_methods.py`

```python
# ----------------------------------------------------------------------------
# Copyright (c) 2024, {author_name}.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd


def duplicate_table(table: pd.DataFrame) -> pd.DataFrame:
    return table
```

### `{module_name}/citations.bib`

```bibtex
@MISC{Caporaso-Bolyen-2024,
  title        = "Developing with {QIIME} 2",
  author       = "{Caporaso, J Gregory and Bolyen, Evan}",
  year         =  2024,
  howpublished = "https://develop.qiime2.org"
}
```

### `{module_name}/plugin_setup.py`

```python
# ----------------------------------------------------------------------------
# Copyright (c) 2024, {author_name}.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin
from q2_types.feature_table import FeatureTable, Frequency
from {module_name} import __version__
from {module_name}._methods import duplicate_table

citations = Citations.load("citations.bib", package="{module_name}")

plugin = Plugin(
    name="{plugin_name}",
    version=__version__,
    website="{project_url}",
    package="{module_name}",
    description="{plugin_description}",
    short_description="{plugin_short_description}",
    # The plugin-level citation of 'Caporaso-Bolyen-2024' is provided as
    # an example. You can replace this with citations to other references
    # in citations.bib.
    citations=[citations['Caporaso-Bolyen-2024']]
)

plugin.methods.register_function(
    function=duplicate_table,
    inputs={'table': FeatureTable[Frequency]},
    parameters={},
    outputs=[('new_table', FeatureTable[Frequency])],
    input_descriptions={'table': 'The feature table to be duplicated.'},
    parameter_descriptions={},
    output_descriptions={'new_table': 'The duplicated feature table.'},
    name='Duplicate table',
    description=("Create a copy of a feature table with a new uuid. "
                 "This is for demonstration purposes only. "),
    citations=[]
)
```

### `{module_name}/tests/__init__.py`

```python
# flake8: noqa
# ----------------------------------------------------------------------------
# Copyright (c) 2024, {author_name}.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
```

### `{module_name}/tests/test_methods.py`

```python
# ----------------------------------------------------------------------------
# Copyright (c) 2024, {author_name}.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
import pandas.testing as pdt

from qiime2.plugin.testing import TestPluginBase
from qiime2.plugin.util import transform
from q2_types.feature_table import BIOMV100Format

from {module_name}._methods import duplicate_table


class DuplicateTableTests(TestPluginBase):
    package = '{module_name}.tests'

    def test_simple1(self):
        in_table = pd.DataFrame(
            [[1, 2, 3, 4, 5], [9, 10, 11, 12, 13]],
            columns=['abc', 'def', 'jkl', 'mno', 'pqr'],
            index=['sample-1', 'sample-2'])
        observed = duplicate_table(in_table)

        expected = in_table

        pdt.assert_frame_equal(observed, expected)

    def test_simple2(self):
        # test table duplication with table loaded from file this time
        # (for demonstration purposes)
        in_table = transform(
            self.get_data_path('table-1.biom'),
            from_type=BIOMV100Format,
            to_type=pd.DataFrame)
        observed = duplicate_table(in_table)

        expected = in_table

        pdt.assert_frame_equal(observed, expected)
```

### `{module_name}/tests/data/table-1.biom`

This is a binary file. Copy it from the skill's `static/table-1.biom` file into the generated project at `{module_name}/tests/data/table-1.biom`.
