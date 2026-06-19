# WAT Framework Project

This project follows the **WAT architecture** (Workflows, Agents, Tools) to separate reasoning from execution.

## Directory Structure

```
.tmp/              # Temporary files (regenerated as needed)
tools/             # Python scripts for deterministic execution
workflows/         # Markdown SOPs defining objectives and procedures
.env               # API keys and environment variables (do not commit)
.env.example       # Template for environment variables
CLAUDE.md          # Agent instructions and framework guidelines
```

## Getting Started

### 1. Set Up Environment
```bash
cp .env.example .env
# Edit .env and fill in your API keys and credentials
```

### 2. Create a Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Write Your First Workflow
- Create a `.md` file in `workflows/` directory
- Define: objective, required inputs, tools to use, expected outputs, edge cases

### 4. Create Tools
- Write Python scripts in `tools/` directory
- Scripts should be deterministic and testable
- Load credentials from `.env` file

## Workflow Template

See `workflows/README.md` for workflow structure and examples.

## Tool Template

See `tools/README.md` for tool guidelines and examples.

## Key Principles

1. **Deliverables go to the cloud** - Final outputs to Google Sheets, Slides, etc.
2. **Intermediates are temporary** - Everything in `.tmp/` is regenerable
3. **Tools are deterministic** - API calls, transformations, file operations
4. **Workflows are instructions** - What to do and how, written in plain language
5. **Agents orchestrate** - Connect workflows to tools, handle failures, ask clarifying questions

## Workflow: AI Reasoning + Execution Loop

1. Read relevant workflow
2. Determine required inputs
3. Execute tools in sequence
4. Handle errors and failures
5. Update workflow with learnings
6. Move forward with improved system
