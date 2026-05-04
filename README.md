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

### Claude
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

### Codex (and others)
If you want to use the skills provided in this plugin with OpenAI's Codex (before we can add them to their marketplace) you have two options:
1. if you use Claude (and you have the Codex app installed on your machine):

    - install the plugin in Claude as described above (or using the UI)
    
    - symlink the skills in the local `.codex` directory:
    
    ```bash
    find $HOME/.claude/plugins/marketplaces/rachis-dev-tools/plugins/rachis-plugin-dev/skills -maxdepth 1 -mindepth 1 -type d -exec ln -s '{}' $HOME/.codex/skills/ \;
    ```
    
2. if you don't use Claude - fetch the skills directly from GitHub:
    ```bash
    curl -L https://github.com/misialq/rachis-claude-marketplace/archive/refs/heads/main.tar.gz | tar -xz -C $HOME/.codex/skills --strip-components=4 "*/plugins/rachis-plugin-dev/skills/"
    ```
In either case, you should see the skills in the `.codex` subdirectory when you run:
```bash
ls .codex/skills
```
