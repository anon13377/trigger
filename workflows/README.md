# Workflows

Workflows are Markdown SOPs (Standard Operating Procedures) that define how to accomplish specific objectives.

## Workflow Structure

Each workflow should include:

### 1. **Objective**
Clear, concise statement of what this workflow accomplishes.

### 2. **Required Inputs**
What information or data is needed to run this workflow?

### 3. **Tools Used**
Which Python scripts from `tools/` are required?

### 4. **Step-by-Step Procedure**
The actual workflow - numbered steps, decision points, tools to call.

### 5. **Expected Output**
What should the workflow produce? Where does it go?

### 6. **Error Handling**
How to handle common failures, rate limits, edge cases.

### 7. **Notes & Learnings**
Updates based on real execution - quirks, timing, constraints discovered.

## Workflow Template

```markdown
# Workflow: [Name]

## Objective
[What does this accomplish?]

## Required Inputs
- Input 1: [description]
- Input 2: [description]

## Tools Used
- `tools/script_name.py` - [purpose]

## Procedure

1. [First step]
2. [Second step]
3. Call `tools/script_name.py` with parameters:
   - param1: [what to pass]
   - param2: [what to pass]
4. [Handle result]
5. [Final output]

## Expected Output
[What should we have when done? Where does it go?]

## Error Handling
- **Error X**: [How to handle it]
- **Error Y**: [How to handle it]
- **Rate limits**: [What we know about API limits]

## Notes & Learnings
[Updates based on execution experience]
```

## Best Practices

- Write workflows as if you're briefing a team member
- Be specific about parameters and expected outputs
- Document constraints you discover (rate limits, timing, edge cases)
- Update workflows as you learn what works
- Keep workflows readable - they're instructions, not code
