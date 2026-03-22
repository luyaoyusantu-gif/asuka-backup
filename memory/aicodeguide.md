# AI Code Guide (AI-Assisted Programming & Vibe Coding Guide)

**Source:** [https://github.com/automata/aicodeguide](https://github.com/automata/aicodeguide)

## Core Concepts

*   **AI Copilot (Assistance)**: Programmer-led. AI is used for code completion, explaining errors, or writing tests (e.g., using Cursor for autocompletion).
*   **AI Pilot (Vibe Coding)**: AI handles full code generation (enabling Agent / YOLO mode). The human is solely responsible for prompting and reviewing.

## Optimal Workflow

1.  **PRD (Product Requirements Document)**: Brainstorm with the LLM first to output a detailed PRD. Avoid trying to build a complex system with a single-sentence prompt.
2.  **Task Breakdown**: Based on the PRD, generate a detailed Markdown to-do list (`todo.md`), including task dependencies.
3.  **Rules & Constraints**: Create `.cursor/rules/` or `rules.md` in the project to standardize architecture, tech stack, and code style, significantly reducing AI hallucinations.
4.  **Test-Driven Development (TDD)**: AI will generate bugs that look plausible but fail to run. Use TDD and property-based tests to constrain AI-generated code.
5.  **Prompt Logging**: Save conversational logs with the AI and append your own thought annotations for easier backtracking.

## Protocols & Frontier Technologies

*   **MCP (Model Context Protocol)**: An Anthropic standard for communication between LLMs and external resources (databases, tools, etc.).
*   **SLOP (Simple Language Open Protocol)**: A more lightweight protocol similar to MCP.
*   **A2A (Agent to Agent Protocol)**: Proposed by Google, focusing on multi-agent communication.
*   **Multi-agent Orchestration**: Multiple agents collaborating (e.g., Gas Town, where one AI acts as a manager distributing tasks while other AIs write code).

## Tools & Ecosystem

*   **Editors / IDEs**: Cursor, Windsurf, VSCode (Copilot Agent Mode), OpenHands, Cline.
*   **CLI Tools**: Claude Code, Aider, Roo Code.
*   **Zero-code Web Platforms**: Bolt.new, v0.dev, Lovable.