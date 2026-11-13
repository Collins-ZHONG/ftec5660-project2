# A-MEM: Background and Reproduction Scope

## Research Background and Paper Overview

Long-running interactions create a memory problem for LLM-based agents: relevant facts and experiences may be scattered across many conversations, while a simple append-only history or isolated note store offers limited support for finding relationships between them. Xu et al. introduce **A-MEM (Agentic Memory for LLM Agents)** to organize an agent's memories and support their use in later tasks.

A-MEM represents experiences as structured memory notes. When a note is added, the system uses an LLM to derive and contextualize its content, including keywords and tags, and searches for related notes. It can create links between related memories and update existing notes as new information changes their context. At query time, the system retrieves relevant notes and uses them as context for the LLM's answer. The design draws on the Zettelkasten idea of connected notes. Its central proposal is that memory organization and ongoing updates can help agents use accumulated experience more effectively than treating each memory as an isolated record.

The original paper evaluates A-MEM on the authors' benchmark settings and compares it with other memory approaches. This study uses the paper to motivate its focus on memory construction, retrieval, and linked context, but it does not reproduce the paper's full benchmark comparison.

## Positioning of the Reproduction

This project reproduces a **bounded workflow from A-MEM's public implementation**: it ingests conversation turns, constructs memory notes and a sentence-embedding index, retrieves seed notes for each question, expands retrieved context through memory links, generates answers with an LLM, and evaluates those answers against the supplied reference answers. The evaluation uses one LoCoMo conversation (`conv-26`) and the same 16 original D2 questions in both conditions. The initial condition contains D2 (17 turns); the expanded condition adds D17 and D18 (67 turns total). Within each condition, we compare the repository's default retrieval setting (`k=10`) with `k=5`, using five repeated evaluation runs.

The purpose is to examine whether this public workflow runs on a small, controlled subset and to describe the effect of changing the retrieval parameter in this setup. It is **not a numerical replication of the paper's headline results**. The paper's full benchmark coverage, model configuration, and evaluation conditions are not reproduced here. In particular, this study uses DeepSeek `deepseek-chat` as the LLM backend, one conversation and 16 questions rather than the paper's complete evaluation set, and the repository's robust evaluation script. The expanded condition is a derived subset of the provided LoCoMo data, not an additional independent benchmark.

Consequently, scores reported below support comparisons **within this experiment** (for example, `k=10` versus `k=5` on the same question set); they should not be compared numerically with scores in the paper as evidence that the paper's results have or have not been reproduced. This design also does not isolate or directly test the causal contribution of A-MEM's linked memory evolution: it includes no ablation of those mechanisms and no competing memory baseline. The results are therefore a small-scale reproduction of selected implementation behavior plus a local parameter comparison, rather than a replication of the paper's full claims.

## Experimental Environment

| Component | Recorded configuration |
|---|---|
| Repository | User's GitHub fork, cloned from [Collins-ZHONG/ftec5660-project2](https://github.com/Collins-ZHONG/ftec5660-project2) |
| Repository revision | `f9a173dec325d84fcc97e7828775c7b241c33466` (checkout `HEAD` when this environment was inspected) |
| Operating environment | Windows, run from PowerShell |
| Python | Python 3.11.4, in the project-local `.venv` virtual environment |
| LLM backend | DeepSeek API through the OpenAI-compatible client; base URL `https://api.deepseek.com` |
| LLM model | `deepseek-chat` |
| Embedding model | Sentence Transformers `all-MiniLM-L6-v2` |
| Evaluation implementation | Repository script `test_advanced_robust.py` with the robust memory layer |
| Data and evaluation | LoCoMo `conv-26`; 16 fixed original D2 questions; `ratio=1.0`; conversation-level memory scope |
| Retrieval parameter | `retrieve_k=10` (repository default) versus `retrieve_k=5` |
| Repeated runs | Five runs per condition, seeds 42–46; the seed changes category-5 answer-option ordering only, not LLM generation |
| Temperature | Category 5: `0.5`; other answer categories use the script's `0.7` setting |

The repository's `requirements.txt` lists dependencies without version pins. The inspected virtual environment reports these key package versions: `openai` 3.46.0, `sentence-transformers` 6.2.0, `torch` 2.15.0, `numpy` 2.4.6, `scikit-learn` 1.9.1, and `bert-score` 0.3.13. These versions describe the local environment; the repository does not provide a complete lockfile, so they do not by themselves guarantee an identical installation elsewhere. The API key is deliberately not recorded.

## Reference

Xu, W., Liang, Z., Mei, K., Gao, H., Tan, J., & Zhang, Y. (2025). *A-Mem: Agentic Memory for LLM Agents*. In **Advances in Neural Information Processing Systems**. See the [A-MEM project repository](https://github.com/WujiangXu/A-mem) for the paper citation and public implementation.
