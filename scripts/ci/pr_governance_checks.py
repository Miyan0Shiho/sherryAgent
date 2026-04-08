#!/usr/bin/env python3
"""SherryAgent GitHub PR governance checks.

This script is intentionally dependency-free so it can run in local dev and GitHub Actions.
Usage:
  python scripts/ci/pr_governance_checks.py --check spec-docs-sync
  python scripts/ci/pr_governance_checks.py --check glossary-consistency
  python scripts/ci/pr_governance_checks.py --check gate-eligibility
  python scripts/ci/pr_governance_checks.py --check no-active-conflict-claim
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


GATE_LABELS = {"gate:G1", "gate:G2", "gate:G3", "gate:G4"}
RISK_LABEL_PREFIX = "risk:"
AXIS_LABEL_PREFIX = "axis:"
STATUS_IN_REVIEW = "status:in_review"
BRANCH_PATTERN = re.compile(r"^codex/multi-agent-test/[0-9]+-[A-Za-z0-9][A-Za-z0-9-]*$")
QUANT_SUMMARY_PATTERN = re.compile(r"(?im)^(?:quant_summary:|#+\s*quantitative summary\b)")


@dataclass
class PRContext:
    number: int | None
    title: str
    body: str
    labels: list[str]
    changed_files: list[str]
    branch_name: str


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def fail(msg: str) -> None:
    print(f"[ERROR] {msg}")
    raise SystemExit(1)


def read_event_payload() -> dict[str, Any]:
    path = os.getenv("GITHUB_EVENT_PATH")
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def run_git_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1..HEAD"],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def gh_api_get(url: str) -> Any:
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_changed_files(repo: str, pr_number: int) -> list[str]:
    api = os.getenv("GITHUB_API_URL", "https://api.github.com")
    page = 1
    files: list[str] = []
    while True:
        url = (
            f"{api}/repos/{repo}/pulls/{pr_number}/files"
            f"?per_page=100&page={page}"
        )
        try:
            data = gh_api_get(url)
        except urllib.error.URLError as exc:
            info(f"GitHub API unavailable ({exc}); using local git diff fallback.")
            return run_git_changed_files()

        if not data:
            break
        files.extend(item.get("filename", "") for item in data if item.get("filename"))
        page += 1
    return files


def parse_pr_context() -> PRContext:
    event = read_event_payload()
    pr = event.get("pull_request", {})

    labels = [item["name"] for item in pr.get("labels", []) if "name" in item]
    number = pr.get("number")
    title = pr.get("title") or ""
    body = pr.get("body") or ""
    branch_name = (
        pr.get("head", {}).get("ref")
        or os.getenv("GITHUB_HEAD_REF")
        or os.getenv("GITHUB_REF_NAME")
        or ""
    )

    repo = os.getenv("GITHUB_REPOSITORY")
    if repo and number:
        changed_files = fetch_changed_files(repo, number)
    else:
        changed_files = run_git_changed_files()

    return PRContext(
        number=number,
        title=title,
        body=body,
        labels=labels,
        changed_files=changed_files,
        branch_name=branch_name,
    )


def has_label(labels: list[str], target: str) -> bool:
    return target in labels


def find_label_with_prefix(labels: list[str], prefix: str) -> str | None:
    for label in labels:
        if label.startswith(prefix):
            return label
    return None


def has_quant_summary(body: str) -> bool:
    return bool(QUANT_SUMMARY_PATTERN.search(body))


def check_spec_docs_sync(ctx: PRContext) -> None:
    spec_touched = any(p.startswith(".trae/specs/") for p in ctx.changed_files)
    contract_docs_touched = any(
        p.startswith("docs/specs/")
        or p.startswith("docs/architecture/")
        or p.startswith("docs/plans/")
        or p == "docs/guides/spec-authority.md"
        for p in ctx.changed_files
    )

    if spec_touched and not contract_docs_touched:
        fail("Spec-Docs Sync failed: `.trae/specs/*` changed without related contract docs update.")

    contract_labeled = has_label(ctx.labels, "type:contract-change")
    if contract_labeled and not (spec_touched and contract_docs_touched):
        fail("Spec-Docs Sync failed: `type:contract-change` requires both `.trae/specs/*` and contract docs changes.")

    info("Spec-Docs Sync passed.")


def check_glossary_consistency(ctx: PRContext) -> None:
    glossary_path = "docs/reference/glossary.md"
    if not os.path.exists(glossary_path):
        fail("Glossary Consistency failed: missing `docs/reference/glossary.md`.")

    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary = f.read()

    required_terms = ["Task", "Run", "Evidence", "Decision", "Cost Record", "G1", "G2", "G3", "G4"]
    missing = [term for term in required_terms if term not in glossary]
    if missing:
        fail(f"Glossary Consistency failed: glossary missing required terms: {', '.join(missing)}")

    info("Glossary Consistency passed.")


def check_gate_eligibility(ctx: PRContext) -> None:
    # Local non-PR runs should not fail just because PR metadata is unavailable.
    if ctx.number is None and not ctx.body.strip():
        info("Gate Eligibility skipped: no pull request context available in local run.")
        return

    required_fields = [
        "linked_issue:",
        "contract_impact:",
        "spec_update:",
        "docs_update:",
        "gate_impact:",
        "evidence:",
        "rollback_plan:",
    ]
    lowered_body = ctx.body.lower()
    missing_fields = [field for field in required_fields if field not in lowered_body]
    if missing_fields:
        fail(
            "Gate Eligibility failed: PR body misses required governance fields: "
            + ", ".join(missing_fields)
        )

    if not has_quant_summary(ctx.body):
        fail(
            "Gate Eligibility failed: PR body misses `quant_summary` / quantitative summary section."
        )

    gate_label = next((label for label in ctx.labels if label in GATE_LABELS), None)
    if not gate_label:
        fail("Gate Eligibility failed: missing one `gate:G1~G4` label.")

    if ctx.number is not None:
        if not ctx.branch_name:
            fail("Gate Eligibility failed: missing PR head branch name.")

        if not BRANCH_PATTERN.match(ctx.branch_name):
            fail(
                "Gate Eligibility failed: branch must follow "
                "`codex/multi-agent-test/<issue-id>-<topic>`."
            )

    if has_label(ctx.labels, "type:contract-change"):
        risk_label = find_label_with_prefix(ctx.labels, RISK_LABEL_PREFIX)
        if risk_label is None:
            fail("Gate Eligibility failed: `type:contract-change` requires a `risk:*` label.")

    info("Gate Eligibility passed.")


def parse_subdomain(title: str) -> str | None:
    # Expected: [axis/subdomain] short topic
    m = re.match(r"\[[^\]/]+/([^\]]+)\]", title.strip())
    if not m:
        return None
    return m.group(1).strip().lower()


def fetch_open_prs(repo: str) -> list[dict[str, Any]]:
    api = os.getenv("GITHUB_API_URL", "https://api.github.com")
    page = 1
    prs: list[dict[str, Any]] = []
    while True:
        url = f"{api}/repos/{repo}/pulls?state=open&per_page=100&page={page}"
        data = gh_api_get(url)
        if not data:
            break
        prs.extend(data)
        page += 1
    return prs


def check_no_active_conflict_claim(ctx: PRContext) -> None:
    if not has_label(ctx.labels, STATUS_IN_REVIEW):
        info("No Active Conflict Claim skipped: current PR is not `status:in_review`.")
        return

    axis_label = find_label_with_prefix(ctx.labels, AXIS_LABEL_PREFIX)
    if axis_label is None:
        fail("No Active Conflict Claim failed: missing `axis:*` label.")

    subdomain = parse_subdomain(ctx.title)
    if subdomain is None:
        fail("No Active Conflict Claim failed: PR title must match `[axis/subdomain] short topic`.")

    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo or ctx.number is None or not os.getenv("GITHUB_TOKEN"):
        info("No Active Conflict Claim running locally or without token; skip remote conflict scan.")
        return

    others = fetch_open_prs(repo)
    conflicts = []
    for pr in others:
        number = pr.get("number")
        if number == ctx.number:
            continue

        labels = [item.get("name", "") for item in pr.get("labels", [])]
        if STATUS_IN_REVIEW not in labels:
            continue
        if axis_label not in labels:
            continue

        other_subdomain = parse_subdomain(pr.get("title", "") or "")
        if other_subdomain == subdomain:
            conflicts.append(number)

    if conflicts:
        fail(
            "No Active Conflict Claim failed: found other in-review PR(s) with same axis/subdomain: "
            + ", ".join(f"#{num}" for num in conflicts)
        )

    info("No Active Conflict Claim passed.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        required=True,
        choices=[
            "spec-docs-sync",
            "glossary-consistency",
            "gate-eligibility",
            "no-active-conflict-claim",
        ],
    )
    args = parser.parse_args()

    ctx = parse_pr_context()
    info(f"Running check: {args.check}")
    info(f"Changed files: {len(ctx.changed_files)}")

    if args.check == "spec-docs-sync":
        check_spec_docs_sync(ctx)
    elif args.check == "glossary-consistency":
        check_glossary_consistency(ctx)
    elif args.check == "gate-eligibility":
        check_gate_eligibility(ctx)
    elif args.check == "no-active-conflict-claim":
        check_no_active_conflict_claim(ctx)
    else:
        fail(f"Unsupported check: {args.check}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as exc:
        fail(f"GitHub API error: {exc}")
