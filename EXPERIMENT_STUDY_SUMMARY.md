# A-MEM 对话记忆问答复现：实验设计与结论

> 本文是正式报告的实验部分草稿，概述研究问题、实验流程和可以由现有结果支持的结论。运行命令、逐题答案和完整日志保留在原始实验文件中。

## Research Background and Paper Overview

Long-running interactions create a memory problem for LLM-based agents: relevant facts and experiences may be scattered across many conversations, while a simple append-only history or isolated note store offers limited support for finding relationships between them. Xu et al. introduce **A-MEM (Agentic Memory for LLM Agents)** to organize an agent's memories and support their use in later tasks.

A-MEM represents experiences as structured memory notes. When a note is added, the system uses an LLM to derive and contextualize its content, including keywords and tags, and searches for related notes. It can create links between related memories and update existing notes as new information changes their context. At query time, the system retrieves relevant notes and uses them as context for the LLM's answer. The design draws on the Zettelkasten idea of connected notes; its central proposal is that memory organization and ongoing updates can help agents use accumulated experience more effectively than treating each memory as an isolated record.

The original paper evaluates A-MEM on the authors' benchmark settings and compares it with other memory approaches. This study uses the paper to motivate its focus on memory construction, retrieval, and linked context, but it does not reproduce the paper's full benchmark comparison.

## Positioning of the Reproduction

This project reproduces a **bounded workflow from A-MEM's public implementation**: it ingests conversation turns, constructs memory notes and a sentence-embedding index, retrieves seed notes for each question, expands retrieved context through memory links, generates answers with an LLM, and evaluates those answers against the supplied reference answers. The evaluation uses one LoCoMo conversation (`conv-26`) and the same 16 original D2 questions in both conditions. The initial condition contains D2 (17 turns); the expanded condition adds D17 and D18 (67 turns total). Within each condition, we compare the repository's default retrieval setting (`k=10`) with `k=5`, using five repeated evaluation runs.

The purpose is to examine whether this public workflow runs on a small, controlled subset and to describe the effect of changing the retrieval parameter in this setup. It is **not a numerical replication of the paper's headline results**. The paper's full benchmark coverage, model configuration, and evaluation conditions are not reproduced here. In particular, this study uses DeepSeek `deepseek-chat` as the LLM backend, one conversation and 16 questions rather than the paper's complete evaluation set, and the repository's robust evaluation script. The expanded condition is a derived subset of the provided LoCoMo data, not an additional independent benchmark.

Consequently, scores reported below support comparisons **within this experiment** (for example, `k=10` versus `k=5` on the same question set); they should not be compared numerically with scores in the paper as evidence that the paper's results have or have not been reproduced. Nor does this design isolate or directly test the causal contribution of A-MEM's linked memory evolution: it includes no ablation of those mechanisms and no competing memory baseline. The results are therefore a small-scale reproduction of selected implementation behavior plus a local parameter comparison, rather than a replication of the paper's full claims.

### Reference

Xu, W., Liang, Z., Mei, K., Gao, H., Tan, J., & Zhang, Y. (2025). *A-Mem: Agentic Memory for LLM Agents*. In **Advances in Neural Information Processing Systems**. See the [A-MEM project repository](https://github.com/WujiangXu/A-mem) for the paper citation and public implementation.

## 研究问题与假设

A-MEM 将对话内容组织为带有属性和链接的记忆条目，再按问题检索记忆来生成答案。本研究是一个**小范围复现**：只使用一个 LoCoMo 对话及 16 道问题，因此问题数量不足以支持稳定的分类别比较。本研究预先将总体 Exact Match 和 Token F1 设为主要观察量，不进行分类别结果处理或分析。首先考察公开实现能否在这个可控子集上完成记忆构建、检索与问答流程。随后提出一个**局部工作假设**：在同一记忆库和同一组问题上，检索较多的候选记忆（`k=10`）可能比检索较少候选（`k=5`）更容易覆盖答案线索，从而提高总体问答匹配分数。更多候选也可能引入噪声，因此这是待检验的方向，而非必然结果。

作为辅助观察，我们还将对话从 17 轮增至 67 轮，保持问题不变，观察较大的记忆库是否改变回答表现。这个比较并未预设“记忆越多，性能越差”，也不构成对遗忘现象的直接测试。

## 数据与实验设计

数据来自仓库提供的 LoCoMo 文件 `data/locomo10.json`。我们选取其中的 `conv-26`，构造两个派生条件：

| 条件 | 纳入的会话 | 对话轮次 | 评估问题 |
|---|---|---:|---:|
| 初始子集 | D2 | 17 | D2 中有证据的原始 16 题 |
| 扩展子集 | D2、D17、D18 | 67 | 与初始子集完全相同的 16 题 |

没有改写问题、参考答案或原始 `locomo10.json`。扩展条件增加的是同一对话中较晚的背景信息，因而可以在固定问题的前提下观察记忆库变化。

每个数据条件分别运行 `k=10`（仓库脚本默认值）和 `k=5`（唯一计划内的检索参数改动），每种组合运行五次，共 20 份成功结果。相同数据条件内，两种 k 共享一次构建的记忆缓存；两种数据条件使用不同缓存。五组配对运行分别使用 seed 42–46。seed 只影响一类选择题的选项顺序，不能固定 LLM 的全部生成行为，因此重复运行用于描述实际波动。

## 实验流程与评价方法

每个数据条件先将对话轮次转换为 A-MEM 记忆条目并建立句向量检索索引。回答每道题时，模型先生成查询关键词；向量检索返回前 k 条种子记忆，系统再加入与种子相连的邻居记忆；回答模型依据得到的上下文生成短答案。这里的 k 是**种子记忆数量**，不等于最终上下文中记忆条目的精确数量。

评估脚本将生成答案与 LoCoMo 原始参考答案比较，记录 Exact Match、Token F1、BERT F1、SBERT 相似度等指标。本研究以**总体 Exact Match 和 Token F1** 为主要观察量，其他总体指标用于交叉检查；对每种组合计算五次运行均值和标准差，并查看 k=10/k=5 的配对差异。

## 结果

| 条件 | k | Exact Match（均值 ± 标准差） | Token F1（均值 ± 标准差） |
|---|---:|---:|---:|
| 17 轮 | 10 | 0.375 ± 0.000 | 0.594 ± 0.016 |
| 17 轮 | 5 | 0.400 ± 0.056 | 0.561 ± 0.051 |
| 67 轮 | 10 | 0.488 ± 0.082 | 0.620 ± 0.090 |
| 67 轮 | 5 | 0.463 ± 0.034 | 0.604 ± 0.027 |

在 **17 轮**条件下，k=10 的 Token F1 均值高于 k=5（0.594 对 0.561）；k=5 的 Exact Match 均值略高（0.400 对 0.375），但这一差异主要来自五次中的一次较好结果。在 **67 轮**条件下，k=10 的 Exact Match 和 Token F1 均略高于 k=5（分别高 0.025 和 0.016）；五组配对运行中，k=10 有四组取得较高的 Token F1。BERT F1 与 SBERT 相似度在两个数据条件下也呈现 k=10 均值略高的方向。

固定问题的跨长度比较中，67 轮条件在两种 k 下的 Exact Match 和 Token F1 均值都高于 17 轮条件。例如 k=10 的 Token F1 从 0.594 升至 0.620；k=5 从 0.561 升至 0.604。本次实验**没有观察到扩充背景轮次后的总体分数下降**。

## 假设检验与结论

局部工作假设获得了**有限的方向性支持**：两个数据条件下，k=10 的 Token F1 均值都高于 k=5；在 67 轮条件下，五组中四组也有这一方向。但差值较小，Exact Match 的方向在两个条件下并不一致，运行波动与均值差距处于相近量级。因此，我们只能得出“在这个子集和固定记忆缓存上，较大的检索范围与略高的总体答案匹配分数相关”的结论，不能断言 k=10 在其他对话或模型上普遍占优。

一种可能机制是 k=10 带来更多种子记忆及其链接邻居，提高了包含正确线索的机会。但当前结果没有测量证据召回率、最终上下文长度或噪声比例，**不能把分数差异归因于这个机制**。67 轮条件分数较高也只是描述性观察：两种长度分别构建了记忆缓存，新增内容可能提供有用信息，LLM 输出也有随机波动，故不能说“增加文本使系统变好”。

本实验复现了 A-MEM 公开实现的**记忆构建、检索、链接扩展与问答评估流程**，并测量了一个检索参数改动的影响。它**没有直接验证论文关于动态记忆组织或记忆演化优于其他方法的核心主张**，因为没有设置无链接、无演化或其他记忆方法的对照组。

## 与原论文实验结果的一致性

**流程层面一致。** 原论文及公开仓库围绕“将历史对话整理成可检索、可链接、可更新的记忆，再用于长程问答”展开。本实验使用其公开实现和 LoCoMo 原始对话、问题，成功构建记忆、检索并完成问答评价。因此，我们复现了所选子集上的基本运行行为。

**性能结论不能判定为一致或不一致。** 公开仓库概述论文在多个基础模型上优于既有基线，并提示应按模型调整检索参数 k。本实验没有运行论文中的竞争记忆方法，也没有使用论文的完整数据及模型配置；k=10 与 k=5 只是同一 A-MEM 实现内部的参数对照。k=10 的 Token F1 在两种记忆长度下均略高，说明该子集的结果与“检索范围会影响表现、k 值需要调节”的经验性说法相容，但既不能证明 A-MEM 优于其他方法，也不能拿当前分数与论文表格直接判定数值复现成功或失败。

若未来出现与论文全量趋势不同的数字，合理的候选解释包括：只选一个对话的 16 道题、使用 DeepSeek 而非论文模型、按证据筛选会话、robust 脚本与论文原始评测流程的差异，以及 LLM 生成波动。当前设计无法分离这些因素的影响，故不将差异归因于其中任一因素。

## 解释边界

本研究沿用了 A-MEM 仓库实现和 LoCoMo 原始对话/问题，但采用了单一对话子集与 DeepSeek `deepseek-chat` 后端，未使用论文完整数据和原模型配置。因此本文结果适合比较本地实现内的条件差异，不宜与论文全量分数直接作数值对齐。每个长度只构建一次记忆缓存，使同长度的 k 对照更可比，却无法估计记忆构建的随机性。五次重复共享同一组 16 道问题，不是五个独立测试集；本文不据此声称统计显著性。

## 数据与结果位置

- 17 轮数据：`data/locomo_conv30_d2_pilot.json`（文件名沿用早期命名，实际样本为 `conv-26`）；结果：仓库根目录 `pilot_k10*.json`、`pilot_k5*.json`。
- 67 轮数据：`data/expanded_memory_67turns_fixed16/locomo_conv26_d2_d17_d18_fixed16.json`；结果：同目录 `results/expanded_k10_rep1..5.json`、`expanded_k5_rep1..5.json`。
- 更详细的指标和运行记录：`data/expanded_memory_67turns_fixed16/results/阶段性结论.md`。
