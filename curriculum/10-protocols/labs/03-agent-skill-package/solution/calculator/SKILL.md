---
name: calculator
description: Evaluate a basic arithmetic expression (+, -, *, /, parentheses) and return the numeric result. Use this whenever the user asks for a calculation or arithmetic result.
---

# Calculator

To evaluate an arithmetic expression safely:

1. Parse the expression with Python's `ast.parse(expression, mode="eval")`.
2. Walk the resulting expression tree, allowing only `ast.BinOp` (with
   `ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div`), `ast.UnaryOp` (with
   `ast.USub`/`ast.UAdd`), and numeric `ast.Constant` nodes.
3. Reject (raise an error for) any other node type.

**Never use `eval()` or `exec()` on the expression directly** -- it is
arbitrary Python code execution, not arithmetic evaluation, and is unsafe for
any input that wasn't fully trusted before this skill ran. See Module 03,
lesson 1 (`curriculum/03-tool-use/lessons/01-tool-schemas.md`) and its lab's
`solution/tools.py` for a complete, tested implementation of this exact
approach.
