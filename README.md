# Algorithmic Reproduction With Multi-Agent And LangSmith Tracking

A multi-agent system for **paper algorithm reproduction**, with full-link workflow orchestration and LangSmith-based tracing across planning, analysis, coding, debugging, and evaluation.

The system integrates multi-stage agent collaboration, unified LLM access, configurable model providers, and end-to-end execution tracking. API configuration and LangSmith observability are centralized to keep the workflow consistent and easy to manage.

The project provides:

- One `.env` file for environment configuration
- One shared `get_client()` interface for LLM access
- Automatic LangSmith tracing
- One environment/API diagnostic command
- One execution command
- One evaluation command

The upstream open-source components used in this project are distributed under the Apache-2.0 License. The project uses `bootstrap.sh` to obtain the required upstream source code and automatically applies the interface adaptations required by the current system.

## Getting Started

Python 3.10+ is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt

Create the environment configuration file:

cp .env.example .env

Edit .env:

P2C_API_KEY=YourDashScopeKey
P2C_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
P2C_MODEL=qwen-plus

P2C_LANGSMITH_ENABLED=true
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=YourLangSmithKey
LANGSMITH_PROJECT=Paper-algorithm-reproduction
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com

Then initialize and run the system:

bash scripts/bootstrap.sh
python scripts/doctor.py
bash scripts/run_qwen.sh
Evaluation

Run a single evaluation:

GENERATED_N=1 bash scripts/eval_qwen.sh

For repeated formal evaluation:

GENERATED_N=8 bash scripts/eval_qwen.sh
Uploading to GitHub
Option A: Source Initialization on Demand

Upload the current repository directly.

After cloning the repository, initialize the required source files with:

bash scripts/bootstrap.sh
Option B: Include the Source Code

Before uploading, run:

bash scripts/vendor_for_github.sh

This script retrieves the required source code, applies the interface adaptations, and removes the nested .git directory.

Then run:

git init

git add .

git commit -m "Paper algorithm reproduction with Multi-Agent and LangSmith"

git branch -M main

git remote add origin <YOUR_GITHUB_REPO>

git push -u origin main
Unified API Interface

LLM access is managed through a shared interface instead of initializing clients independently across multiple Agent modules.

The unified interface is:

from p2c_runtime import get_client

client = get_client()

The model provider, API endpoint, API key, and model name are managed through .env.

This allows the system to switch between Qwen, OpenAI, and other OpenAI-compatible APIs without modifying individual Agent modules.

LangSmith Tracking

LangSmith tracing is integrated into the complete multi-agent workflow.

The tracing pipeline covers:

Planning
   ↓
Analysis
   ↓
Coding
   ↓
Debugging
   ↓
Evaluation

Each stage can be inspected independently in LangSmith while preserving the execution relationship between different Agent stages.

Tracing configuration is also managed through .env, so enabling or disabling LangSmith does not require modifying individual Agent scripts.

Example:

P2C_LANGSMITH_ENABLED=true
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=YourLangSmithKey
LANGSMITH_PROJECT=Paper-algorithm-reproduction
System Workflow

The overall workflow is organized as:

Paper
  ↓
Planning Agent
  ↓
Analysis Agent
  ↓
Coding Agent
  ↓
Debugging Agent
  ↓
Execution
  ↓
Evaluation

The system combines multi-agent collaboration with structured context transfer, code generation, execution feedback, debugging, and full-link observability.

Security

Do not upload .env to GitHub.

If API keys have previously appeared in chat messages, terminal logs, or other public locations, rotate both the DashScope and LangSmith keys before publishing the repository.

Before committing, check for accidentally included secrets:

git status

git grep -nE 'sk-[A-Za-z0-9_-]{10,}|lsv2_[A-Za-z0-9_-]{10,}' || true
Upstream

Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning

Original repository:

going-doer/Paper2Code

The original project is distributed under the Apache-2.0 License.

Acknowledgements

This project references the work presented in:

Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning

Acknowledged authors:

Jinheon Baek
Sung Ju Hwang
