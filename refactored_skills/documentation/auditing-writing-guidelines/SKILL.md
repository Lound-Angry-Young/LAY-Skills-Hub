---
name: auditing-writing-guidelines
description: >
  Reviews docs and prose for Writing Guidelines compliance, checking style, voice and tone against the writing handbook. Use this skill when: asked to review docs, check writing style, audit prose or check a page against the writing handbook. Do NOT use this skill when: cleaning invisible marks or provenance from text (use polishing-user-facing-prose or stripping-ai-provenance-marks) or writing architecture decision records (use documenting-architecture-decisions).
---

# Writing Guidelines

Review files for compliance with Writing Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/writing-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.
