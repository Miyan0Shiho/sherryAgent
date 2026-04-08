## Summary

- linked_issue: Closes #<issue-id>
- change_type: `<axis-task | contract-change | conflict-decision>`
- branch_name: `codex/multi-agent-test/<issue-id>-<topic>`

## Governance Fields (Required)

- linked_issue: 
- branch_name: 
- contract_impact: `<yes/no>`
- spec_update: `<what changed in .trae/specs/*>`
- docs_update: `<what changed in docs/*>`
- gate_impact: `<gate:G1 | gate:G2 | gate:G3 | gate:G4>`
- evidence: `<logs/links/files proving this is safe>`
- rollback_plan: `<how to revert if wrong>`
- origin_role: `<Product Owner | Researcher | Architect | Spec Owner | Implementer | Reviewer | Release Governor>`
- review_role: `<usually Reviewer or Spec Owner>`
- gate_owner: `<usually Release Governor>`

## Risk & Scope (Required)

- risk_level: `<risk:low | risk:medium | risk:high>`
- axis_label: `<axis:...>`
- status_label: `<status:in_review before requesting review>`
- touch_scope: `<contracts/modules/files>`
- depends_on: `<issues or PRs>`

## Validation Checklist

- [ ] I followed branch naming: `codex/multi-agent-test/<issue-id>-<topic>`
- [ ] If `.trae/specs/*` changed, I also updated related `docs/*`
- [ ] I updated `docs/INDEX.md` for any non-trivial doc entry change
- [ ] I did not bypass dual authority rules in `docs/guides/spec-authority.md`
- [ ] If this is `contract-impacting`, both spec and docs authorities are requested for review
