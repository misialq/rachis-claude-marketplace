#!/usr/bin/env python3
"""Scaffold a QIIME 2 plugin from the caporaso-lab Copier template."""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE_SRC = "https://github.com/caporaso-lab/plugin-template"
DEFAULT_PACKAGE_NAME = "q2-hello-world"
DEFAULT_AUTHOR_NAME = "A QIIME 2 Plugin Developer"
DEFAULT_AUTHOR_EMAIL = "q2-dev@example.com"
DEFAULT_PROJECT_URL = "https://example.com"
DEFAULT_PLUGIN_DESCRIPTION = "A QIIME 2 plugin template."
DEFAULT_PLUGIN_SHORT_DESCRIPTION = "Plugin template."
TARGET_DISTROS = ("tiny", "amplicon", "metagenome")
LICENSE_CHOICES = ("BSD-3-Clause", "MIT", "Apache-2.0", "skip-license")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a QIIME 2 plugin from the Copier template.",
    )
    parser.add_argument(
        "destination",
        help="Directory where the new plugin project should be created.",
    )
    parser.add_argument(
        "--vcs-ref",
        default="HEAD",
        help="Template git ref to use. Defaults to HEAD to track the current main branch.",
    )
    parser.add_argument(
        "--package-name",
        default=DEFAULT_PACKAGE_NAME,
        help="Package name used as the top-level directory and Python package prefix.",
    )
    parser.add_argument(
        "--module-name",
        help="Python module name. Defaults to package_name with dashes replaced by underscores.",
    )
    parser.add_argument(
        "--plugin-name",
        help="QIIME 2 plugin name. Defaults to package_name with a leading q2- removed.",
    )
    parser.add_argument(
        "--author-name",
        default=DEFAULT_AUTHOR_NAME,
        help="Plugin author name.",
    )
    parser.add_argument(
        "--author-email",
        default=DEFAULT_AUTHOR_EMAIL,
        help="Plugin author email.",
    )
    parser.add_argument(
        "--project-url",
        default=DEFAULT_PROJECT_URL,
        help="Primary project or documentation URL.",
    )
    parser.add_argument(
        "--plugin-description",
        default=DEFAULT_PLUGIN_DESCRIPTION,
        help="Long description shown when plugin information is requested.",
    )
    parser.add_argument(
        "--plugin-short-description",
        default=DEFAULT_PLUGIN_SHORT_DESCRIPTION,
        help="Short description shown in plugin lists.",
    )
    parser.add_argument(
        "--target-distro",
        choices=TARGET_DISTROS,
        default="tiny",
        help="QIIME 2 target distribution.",
    )
    parser.add_argument(
        "--license",
        choices=LICENSE_CHOICES,
        default="skip-license",
        help="Project license selection.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the render without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing destination by passing --force to Copier.",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Fail if Copier is missing instead of installing it with pip.",
    )
    return parser.parse_args()


def remove_prefix(value: str, prefix: str) -> str:
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def ensure_copier(skip_install: bool) -> list[str]:
    copier_path = shutil.which("copier")
    if copier_path:
        return [copier_path]

    if skip_install:
        raise SystemExit(
            "copier is not installed. Install it with 'python3 -m pip install copier' and rerun.",
        )

    print("copier is not installed; installing with pip...", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "pip", "install", "copier"], check=True)

    copier_path = shutil.which("copier")
    if copier_path:
        return [copier_path]

    try:
        subprocess.run(
            [sys.executable, "-m", "copier", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise SystemExit("copier installation completed, but the CLI is still unavailable.") from exc

    return [sys.executable, "-m", "copier"]


def resolve_answers(args: argparse.Namespace) -> list[tuple[str, str]]:
    module_name = args.module_name or args.package_name.replace("-", "_")
    if not module_name.isidentifier():
        raise SystemExit(
            f"module_name '{module_name}' is not a valid Python identifier.",
        )

    plugin_name = args.plugin_name or remove_prefix(args.package_name, "q2-")

    return [
        ("package_name", args.package_name),
        ("module_name", module_name),
        ("plugin_name", plugin_name),
        ("author_name", args.author_name),
        ("author_email", args.author_email),
        ("project_url", args.project_url),
        ("plugin_description", args.plugin_description),
        ("plugin_short_description", args.plugin_short_description),
        ("target_distro", args.target_distro),
        ("license", args.license),
    ]


def build_command(copier_cmd: list[str], args: argparse.Namespace) -> list[str]:
    command = [
        *copier_cmd,
        "copy",
        "--vcs-ref",
        args.vcs_ref,
        "--defaults",
    ]

    if args.dry_run:
        command.append("--pretend")
    if args.force:
        command.append("--force")

    for key, value in resolve_answers(args):
        command.extend(["--data", f"{key}={value}"])

    command.extend([TEMPLATE_SRC, str(Path(args.destination).expanduser())])
    return command


def main() -> int:
    args = parse_args()
    copier_cmd = ensure_copier(args.skip_install)
    command = build_command(copier_cmd, args)

    print(shlex.join(command))
    subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
