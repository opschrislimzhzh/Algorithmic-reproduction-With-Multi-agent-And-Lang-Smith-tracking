# Reproducibility notes

The upstream API path initializes `OpenAI(...)` independently in multiple
scripts. This package replaces those constructions with one shared runtime:

```python
from p2c_runtime import get_client, traceable
client = get_client()
```

Provider/model/secrets come from `.env`.

Default Qwen/DashScope configuration:

```dotenv
P2C_API_KEY=...
P2C_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
P2C_MODEL=qwen-plus
```

Any OpenAI-compatible provider can be substituted by changing only these
variables. For native OpenAI, leave `P2C_BASE_URL` empty.

The compatibility proxy removes `reasoning_effort` for non-OpenAI reasoning
model families, which avoids Qwen incompatibilities in scripts originally
written for o3/o4 models.

Not committed:
- API keys
- LangSmith keys
- generated outputs
- virtual environments

For a byte-for-byte copy of a locally hand-edited Paper2Code tree, replace
`paper2code_src` with that local tree before committing.
