#!/usr/bin/env python3
"""
Tool: Template Tool
Purpose: Starter template for creating new tools
Inputs: Command line arguments or environment variables
Output: Results to stdout, errors to stderr
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """Main execution function."""
    try:
        # Example: Get an API key from environment
        api_key = os.getenv('API_KEY')

        if not api_key:
            raise ValueError("API_KEY not set in .env file")

        # Example: Get command line argument if provided
        if len(sys.argv) > 1:
            input_data = sys.argv[1]
        else:
            input_data = "default_value"

        # TODO: Replace with actual tool logic
        result = {
            "status": "success",
            "input": input_data,
            "message": "Template tool executed successfully"
        }

        # Output result as JSON
        print(json.dumps(result, indent=2))
        return 0

    except Exception as e:
        error_msg = {"status": "error", "message": str(e)}
        print(json.dumps(error_msg, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
