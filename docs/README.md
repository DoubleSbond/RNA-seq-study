# Documentation

Use this directory for human-readable records of the CYP family study workflow and the reusable standards for future detoxification gene-family analyses.

Key files:

- `workflow.md`: reconstructed step-by-step CYP analysis workflow.
- `gene_family_method_blueprint.md`: portable RNA-seq-to-gene-family study template derived from the CYP workflow.
- `family_standardization.md`: standard layer names, stage gates, naming rules, and required structure for CYP, CarE, GST, UGT, SULT, ABC, and related families.
- `archive_status.md`: current public archive state and remaining gaps.
- `archive_completeness_audit.md`: README coverage and omission-check summary.
- `external_archive_policy.md`: policy for large/raw/external assets.
- `hpc_confirmation_runbook.md`: final HPC-side version, checksum, and primer-confirmation workflow.
- `hpc_evidence_collection_checklist.md`: short checklist for the next live HPC evidence-collection pass.
- `release_readiness_checklist.md`: pre-release checklist for the first archive tag.
- `release_gate_matrix.md`: release gate table separating required, preferred, and deferrable items.
- `release_blockers.md`: consolidated blocker tracker for owner decisions, HPC confirmation, and external assets.
- `release_notes_v0.1_draft.md`: draft GitHub Release notes for the first archive tag.
- `citation_and_license_decisions.md`: citation metadata and license decision notes.
- `citation_cff_draft.md`: placeholder-based inputs for a future `CITATION.cff`.
- `license_decision_matrix.md`: license strategy options before adding a formal `LICENSE`.
- `collection_narrative_audit.md`: evidence audit for recovered local/HPC material.
- `script_provenance_index.md`: mapping from public scripts to workflow blocks.
- `data_versions.md`: project data layer definitions and caution notes.
- `audit/`: small consistency audit notes.
- `notes/`: short interpretation notes for specific analysis layers.

Standardization entry points:

- Start with `docs/family_standardization.md` for directory structure and stage gates.
- Fill `config/families/<family>.yaml` before running a new family screen.
- Keep broad pool, high-confidence core set, unknown/ambiguous candidates, and validation candidates as separate layers.
