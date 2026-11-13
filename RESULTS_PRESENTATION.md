# Results: A-MEM LoCoMo Subset Reproduction

## Evaluation Setup

The evaluation uses one LoCoMo conversation (`conv-26`) and the same 16 original D2 questions in both data conditions. The pilot condition contains D2 (17 turns); the expanded condition contains D2, D17, and D18 (67 turns total). Each condition was evaluated with `retrieve_k=10` and `retrieve_k=5`, with five repeated runs per setting. Within each data condition, the k settings and repeats share the same constructed memory cache.

## Aggregate Results

**Table 1. Mean and sample standard deviation across five runs**

| Memory condition | Retrieved memories (`k`) | Exact Match | Token F1 | BERTScore F1 | SBERT similarity |
|---|---:|---:|---:|---:|---:|
| Pilot, 17 turns | 10 | 0.3750 ± 0.0000 | 0.5942 ± 0.0158 | 0.9434 ± 0.0017 | 0.7272 ± 0.0032 |
| Pilot, 17 turns | 5 | 0.4000 ± 0.0559 | 0.5609 ± 0.0507 | 0.9387 ± 0.0069 | 0.6992 ± 0.0480 |
| Expanded, 67 turns | 10 | 0.4875 ± 0.0815 | 0.6203 ± 0.0896 | 0.9457 ± 0.0090 | 0.7357 ± 0.0822 |
| Expanded, 67 turns | 5 | 0.4625 ± 0.0342 | 0.6042 ± 0.0266 | 0.9406 ± 0.0046 | 0.7179 ± 0.0331 |

Each cell reports the mean and **sample standard deviation** of the five run-level aggregate scores. For example, the five Exact Match values in a condition are summarized across runs; this is not a standard deviation across individual questions. The five runs reuse the same 16 questions and, within each memory condition, the same memory cache. These standard deviations describe observed run-to-run variability and are not confidence intervals over independent datasets.

## Interpretation

In the 17-turn pilot, `k=10` had higher mean Token F1, BERTScore F1, and SBERT similarity, while `k=5` had a slightly higher mean Exact Match. In the 67-turn condition, `k=10` had higher means on all four aggregate metrics. The differences are modest, and some run-to-run standard deviations are similar in size to the differences between means. The results therefore provide limited, descriptive support for the local hypothesis that retrieving more seed memories may improve overall answer matching in this particular subset. They do not establish that `k=10` is generally better.

All four aggregate metrics were higher in the 67-turn condition than in the 17-turn pilot for each value of `k`. This is an observed difference between two separately constructed memory conditions, not evidence that adding conversation turns caused performance to improve. The experiment uses one conversation, a fixed 16-question set, and one cache per condition, so it cannot separate the effect of added context from cache construction and model-generation variability.

## Why We Report Aggregate Metrics Only

This is a small-scale reproduction based on one conversation and 16 questions. The questions are distributed unevenly across the benchmark's categories, leaving some category groups with only one or two items and omitting at least one category in this selected subset. With groups this small, a single answer can dominate a category-level score. Five repeated model runs do not add new questions or independent conversations, so they do not solve this sample-size problem.

For these reasons, the planned analysis uses overall Exact Match and Token F1 as its primary measures, with BERTScore F1 and SBERT similarity as aggregate cross-checks. It does not make category-level comparisons or conclusions. This keeps the claims aligned with the amount of evidence: the results describe average behavior on the selected question set, not stable differences between question types or performance across the full LoCoMo benchmark.

## Result Scope

The results reproduce selected execution and evaluation behavior of A-MEM's public implementation and compare two retrieval settings within that implementation. They do not reproduce the paper's full benchmark results, compare A-MEM with competing memory systems, or isolate the causal effect of linked memory evolution. The use of DeepSeek `deepseek-chat`, a single conversation, and a 16-question subset also prevents direct numerical comparison with the paper's reported scores.

## Source Files

- Pilot results: `pilot_k10.json`, `pilot_k10_rep2.json` through `pilot_k10_rep5.json`, and the corresponding `pilot_k5*.json` files in the repository root. The unnumbered file is the first run.
- Expanded results: `data/expanded_memory_67turns_fixed16/results/expanded_k10_rep1.json` through `expanded_k10_rep5.json`, and the corresponding `expanded_k5_rep*.json` files.
- Experiment design and detailed notes: `EXPERIMENT_STUDY_SUMMARY.md` and `data/expanded_memory_67turns_fixed16/results/阶段性结论.md`.
