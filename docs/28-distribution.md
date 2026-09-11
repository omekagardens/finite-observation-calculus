# 28 — Distribution at scale

The architecture is **map-reduce**: each node is independently certifiable
(`docs/22` §2), the composition is a union of probes → intersection of annihilators
(`docs/20` §5), and exact arithmetic makes results bit-identical. This note shards
nodes across processes and measures it.

## 1. The run

```
python3 scripts/distribute.py --reps 16
```

```
jobs       : 128
serial     : 7040.3 ms
parallel   : 1215.7 ms   speedup 5.79x
agreement  : True  (bit-identical across processes)
certificate: {"task": "add", "min_lift": "linear", "verdict": "separated", "losses": {...}}
```

**5.79×** on 128 node jobs, over ~8–10 usable cores — and `agreement: True`: the
parallel result is **bit-identical** to serial (exact arithmetic has no
re-association error, unlike floats).

## 2. The transports

- **Independence** (`docs/22` §2): a node's certificate does not depend on the
  others, so the batch shards freely.
- **JSON certificates** (`docs/14` style): the wire object between processes;
  here each certificate carries the task, its minimal lift, verdict, and the
  exact losses as strings.
- **Associativity**: combining nodes is a fold over the probe union — order and
  grouping do not matter, so it parallelises and is fault-tolerant per node.

## 3. Caveats

- **Spawn, not fork**: on macOS the pool re-imports `__main__`, so the runner must
  be a file (`scripts/distribute.py`), not piped input.
- **Overhead on tiny nodes**: with few or very cheap nodes the process startup
  dominates (an earlier 64-job run showed serial fast, parallel unavailable).
  The speedup appears once the batch is large enough — as here.
- **Nodes, not the router**: the router is the one shared component; at scale it
  becomes the coordinator (and a single point of contention, `docs/21`).

## 4. Status

Implemented as `foc.distributed` (`node_certificate`, `run_serial`, `run_parallel`,
`benchmark_distributed`) and `scripts/distribute.py`.

**Back to** [README](../README.md).
