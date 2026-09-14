# LangSmith

This reproducibility layer uses the standard LangSmith OpenAI wrapper.

You only configure environment variables; individual agents no longer need
their own LangSmith setup.

## `.env`

```dotenv
P2C_LANGSMITH_ENABLED=true
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=Paper2Code-repro
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
```

If your LangSmith account uses the US endpoint instead:

```dotenv
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

The patch gives API helper calls stage names such as Planning LLM, Analysis
LLM, Coding LLM, Debugging LLM and Evaluation LLM. The underlying
`client.chat.completions.create(...)` is wrapped with `wrap_openai`.

Disable tracing by setting:

```dotenv
P2C_LANGSMITH_ENABLED=false
LANGSMITH_TRACING=false
```
