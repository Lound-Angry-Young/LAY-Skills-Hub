---
name: generating-knowledge-graphs
description: >
  Answers questions about a codebase, its architecture, file relationships or project content by building and querying a persistent knowledge graph with graphify over code, docs, papers, images and videos, treating graphify-out/ as the first source when it exists. Use this skill when: asked about architecture, file relationships or project content, especially when graphify-out/ exists. Do NOT use this skill when: the question is a single-file edit with no structural context.
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

## Sections
- Usage
- What graphify is for
- What You Must Do When Invoked
- Interpreter guard for subcommands
- For --update and --cluster-only
- For /graphify query
- For /graphify add and --watch
- For the commit hook and native CLAUDE.md integration
- Honesty Rules

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
