# Rachis Claude Marketplace
This repository contains plugins and skills for agentic AI assistants to work during Rachis development. 

> [!WARNING]  
> **Experimental:** These skills are experimental. Please be aware that AI models, LLMs, and agents can make mistakes or hallucinate incorrect information. Always review the generated code and results carefully.

## Overview of Skills

The skills listed below are packaged into a single `rachis-plugin-dev` Claude Code plugin:

* **`rachis-plugin-creator`**: Scaffold new Rachis plugins from the official template directly, without requiring external tools.
* **`rachis-action-creator`**: Extend an existing Rachis plugin by adding a CLI-backed action (new method or visualizer).
* **`rachis-unit-test-writer`**: Write or update unit tests for Rachis plugin code, following local repository test styles and mocking external boundaries.

## Installation

To make the plugin available in your Claude Code instance follow the steps below (from within Claude Code):

- add the marketplace:
```
/plugin marketplace add misialq/rachis-claude-marketplace
```
- install the plugin
```
/plugin install rachis-plugin-dev@rachis-dev-tools
```
- reload plugins
```
/reload-plugins
```