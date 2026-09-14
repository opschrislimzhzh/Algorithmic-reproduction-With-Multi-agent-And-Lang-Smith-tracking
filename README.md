# Paper2Code Repro — Qwen + LangSmith

这是一个面向 **Paper2Code API 路径复现** 的 GitHub-ready 包装层。

核心目标：把原先散落在多个 Agent 脚本里的 API 和 LangSmith 配置，简化成：

1. 一个 `.env`
2. 一个共享 `get_client()`
3. 自动 LangSmith tracing
4. 一个环境/API 自检命令
5. 一个运行命令
6. 一个评测命令

上游 Paper2Code 是 Apache-2.0 项目。本仓库通过 `bootstrap.sh` 获取上游代码，
然后自动应用小范围、可重复的接口补丁。

## 最快复现

推荐 Python 3.10+：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

cp .env.example .env
```

编辑 `.env`：

```dotenv
P2C_API_KEY=你的DashScopeKey
P2C_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
P2C_MODEL=qwen-plus

P2C_LANGSMITH_ENABLED=true
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=你的LangSmithKey
LANGSMITH_PROJECT=Paper2Code-repro
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
```

然后：

```bash
bash scripts/bootstrap.sh
python scripts/doctor.py
bash scripts/run_qwen.sh
```

## 评测

```bash
GENERATED_N=1 bash scripts/eval_qwen.sh
```

正式重复评测：

```bash
GENERATED_N=8 bash scripts/eval_qwen.sh
```

## 上传 GitHub

### 方式 A：推荐，仓库更小

直接上传本包装仓库。其他人 clone 后运行：

```bash
bash scripts/bootstrap.sh
```

### 方式 B：把上游源码也一起上传

在上传前运行：

```bash
bash scripts/vendor_for_github.sh
```

它会拉取上游代码、打补丁，并移除嵌套 `.git`。然后：

```bash
git init
git add .
git commit -m "Paper2Code reproducible Qwen + LangSmith setup"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO>
git push -u origin main
```

## 接口简化

原本多个文件分别写：

```python
client = OpenAI(...)
```

现在统一为：

```python
from p2c_runtime import get_client
client = get_client()
```

换 Qwen / OpenAI / 其他 OpenAI-compatible API 时只改 `.env`。

LangSmith 同理，开关 tracing 不再需要逐个修改 Agent。

## 安全

不要上传 `.env`。此前如果 API key 曾出现在聊天或日志里，建议先轮换
DashScope 和 LangSmith key，再上传 GitHub。

提交前可检查：

```bash
git status
git grep -nE 'sk-[A-Za-z0-9_-]{10,}|lsv2_[A-Za-z0-9_-]{10,}' || true
```

## 上游

Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning  
Upstream: going-doer/Paper2Code
