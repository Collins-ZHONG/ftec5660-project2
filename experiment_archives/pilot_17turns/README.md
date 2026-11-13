# Pilot cache archive

- cached_memories_robust_openai_deepseek-chat: prior 17-turn pilot memory cache, preserved before expanding the dataset.
- cached_memories_robust_openai_deepseek-chat_empty-session-cache: previously isolated invalid empty-session cache; do not reuse.

The evaluator reads its cache from the repository root. These archived folders are no longer found automatically.
For the expanded D2/D17/D18 dataset, the first run must create 67 memories. Subsequent k=10/k=5 runs and repetitions should reuse that new cache.
Pilot results (pilot_*.json) and logs remain in their original locations; the evaluator does not use them as input.
Do not restore the pilot cache while running expanded datasets. To restore it for a pilot rerun, first archive the expanded cache, then move the valid pilot cache back to the repository root.
