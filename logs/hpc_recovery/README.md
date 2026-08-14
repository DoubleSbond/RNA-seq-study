# HPC Recovery Logs

This directory stores sanitized records for files recovered from HPC into the GitHub archive workflow.

Current audit table:

```text
hpc_recovered_files_sha256.tsv
```

The table records relative file paths, SHA256 checksums, byte sizes, and line counts for recovered small files.

Additional sanitized HPC confirmation records:

- `hpc_tool_versions_confirmed_20260814.tsv`: tool versions confirmed from live HPC commands or recovered logs.
- `hpc_91cyp_command_search_20260814.md`: first live HPC search note for the original 91-CYP candidate-generation command sequence.
