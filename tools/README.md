# Tools

Tools are Python scripts that handle deterministic execution: API calls, data transformations, file operations, database queries.

## Tool Structure

Each tool should be:
- **Deterministic**: Same inputs always produce same outputs
- **Testable**: Can be run and verified independently
- **Fast**: Optimized for execution, not reasoning
- **Clear**: Single responsibility, obvious purpose

## Tool Template

```python
#!/usr/bin/env python3
"""
Tool: [Tool Name]
Purpose: [What does this tool do?]
Inputs: [What parameters does it take?]
Output: [What does it return?]
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main execution function."""
    # Get credentials from environment
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print("Error: API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)
    
    # TODO: Implement tool logic
    pass

if __name__ == "__main__":
    main()
```

## Guidelines

### 1. Environment Variables
- Load credentials from `.env` using `python-dotenv`
- Never hardcode API keys or secrets
- Handle missing credentials gracefully with clear error messages

### 2. Error Handling
```python
try:
    # Tool logic
    pass
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### 3. Logging
- Use `print()` for normal output
- Use `print(..., file=sys.stderr)` for errors
- Include descriptive messages

### 4. Return Values
- Exit code 0 for success
- Exit code 1 for failure
- Print results to stdout
- Print errors to stderr

### 5. Testing
Tools should be testable independently:
```bash
python tools/tool_name.py --input "value"
```

## Execution from Workflows

When an agent runs a tool from a workflow:
```bash
python tools/tool_name.py
```

The tool reads from `.env` and produces output that the workflow uses.

## Common Tool Patterns

### API Calls
Use `requests` library, handle rate limits and errors.

### File Operations
Work with files in `.tmp/` or specified paths.

### Data Transformations
Read data, process, write results.

### Database Queries
Connect with appropriate client, handle transactions.

## Dependencies

Add required packages to your environment:
```bash
pip install requests python-dotenv pandas
```

Keep dependencies minimal and well-documented.
