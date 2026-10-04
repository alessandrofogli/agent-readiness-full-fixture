# Profiling

- **Continuous profiling**: Pyroscope runs locally (`docker compose up pyroscope`,
  UI at http://localhost:4040). Services push profiles via `PYROSCOPE_SERVER`.
- **On-demand flame graphs**: `make profile` attaches py-spy to the running API
  and writes `profile.svg` (30-second sample).

```bash
make up        # start pyroscope
make profile   # capture a flame graph of the local API
```
