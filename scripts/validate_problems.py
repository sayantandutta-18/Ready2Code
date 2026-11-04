#!/usr/bin/env python3
"""
Problem Bank Validator & Test Harness Runner
Enforces schema requirements and executes reference solutions against all sample and hidden tests.
Exits with 0 if all problems pass; exits with 1 on any failure.
"""

import os
import sys
import glob
import json
import re
import subprocess
import time

VALID_TOPICS = {
    "Arrays and Hashing",
    "Two Pointers and Sliding Window",
    "Strings",
    "Stack and Queue",
    "Linked List",
    "Trees",
    "Graphs",
    "Binary Search",
    "Dynamic Programming",
    "Heap and Intervals"
}

VALID_DIFFICULTIES = {"easy", "medium", "hard"}

def normalize_output(val: str) -> str:
    """Normalize output for robust comparison."""
    if val is None:
        return ""
    s = str(val).strip().replace("\r\n", "\n")
    # If wrapped in literal quotes, unwrap
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    # Collapse json array / object spacing
    try:
        parsed = json.loads(s)
        return json.dumps(parsed, separators=(',', ':')).lower()
    except Exception:
        # Text normalization
        return re.sub(r'\s+', '', s).lower()

def execute_python_solution(code: str, input_str: str, timeout_s: float = 3.0):
    """
    Executes Python code against input_str using the harness matching submissions runner.
    """
    harness = f"""
import sys, json

{code}

_raw_input = {repr(input_str)}.strip().split('\\n')
_parsed_args = []
for line in _raw_input:
    line = line.strip()
    if not line:
        continue
    try:
        _parsed_args.append(json.loads(line))
    except Exception:
        try:
            _parsed_args.append(eval(line))
        except Exception:
            _parsed_args.append(line)

_func_candidates = [v for k, v in list(locals().items()) if callable(v) and not k.startswith('_')]
if _func_candidates:
    target_fn = _func_candidates[-1]
    res = target_fn(*_parsed_args)
    if res is True:
        print("true")
    elif res is False:
        print("false")
    elif isinstance(res, (dict, list)):
        print(json.dumps(res, separators=(',', ':')))
    else:
        print(res)
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", harness],
            capture_output=True,
            text=True,
            timeout=timeout_s
        )
        if proc.returncode != 0:
            return False, f"Runtime error: {proc.stderr.strip()}"
        return True, proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Time Limit Exceeded"
    except Exception as e:
        return False, f"Execution exception: {str(e)}"

def validate_problem(data: dict, filepath: str) -> list[str]:
    """Validates problem schema against all Phase 2 requirements."""
    errors = []
    fname = os.path.basename(filepath)

    # 1. slug
    slug = data.get("slug")
    if not slug or not re.match(r'^[a-z0-9-]+$', slug):
        errors.append(f"{fname}: Invalid or missing 'slug' ({slug})")

    # 2. title
    if not data.get("title") or len(data["title"].strip()) < 3:
        errors.append(f"{fname}: Missing or too short 'title'")

    # 3. difficulty
    diff = data.get("difficulty", "").lower()
    if diff not in VALID_DIFFICULTIES:
        errors.append(f"{fname}: Invalid 'difficulty' ({diff}), must be one of {VALID_DIFFICULTIES}")

    # 4. topic
    topic = data.get("topic")
    if topic not in VALID_TOPICS:
        errors.append(f"{fname}: Invalid 'topic' ({topic}), must be one of {VALID_TOPICS}")

    # 5. tags
    tags = data.get("tags")
    if not tags or not isinstance(tags, list) or len(tags) == 0:
        errors.append(f"{fname}: 'tags' must be a non-empty list including pattern name")

    # 6. statement_md
    stmt = data.get("statement_md", "")
    if len(stmt.strip()) < 30:
        errors.append(f"{fname}: 'statement_md' is missing or too brief")

    # 7. examples
    examples = data.get("examples")
    if not examples or not isinstance(examples, list) or len(examples) < 2:
        errors.append(f"{fname}: Must have at least 2 'examples' with explanations (found {len(examples) if examples else 0})")
    else:
        for idx, ex in enumerate(examples):
            if not ex.get("input") or not ex.get("output") or not ex.get("explanation"):
                errors.append(f"{fname}: Example {idx + 1} missing input, output, or explanation")

    # 8. sample_tests
    samples = data.get("sample_tests")
    if not samples or not isinstance(samples, list) or len(samples) < 2:
        errors.append(f"{fname}: Must have at least 2 sample_tests (found {len(samples) if samples else 0})")

    # 9. hidden_tests
    hidden = data.get("hidden_tests")
    if not hidden or not isinstance(hidden, list) or len(hidden) < 8:
        errors.append(f"{fname}: Must have at least 8 hidden_tests (found {len(hidden) if hidden else 0})")

    # 10. hints
    hints = data.get("hints")
    if not hints or len(hints) != 3:
        errors.append(f"{fname}: Must contain exactly 3 hints (levels 1, 2, 3)")
    else:
        level3 = next((h for h in hints if h.get("level") == 3), None)
        if level3:
            # Level 3 names data structure but contains NO code
            if "`" in level3.get("text", ""):
                errors.append(f"{fname}: Hint level 3 must not contain code blocks or backticks")

    # 11. editorial_md
    editorial = data.get("editorial_md", "")
    if not editorial or len(editorial.strip()) < 40:
        errors.append(f"{fname}: 'editorial_md' missing or too short")
    else:
        ed_lower = editorial.lower()
        if "complexity" not in ed_lower:
            errors.append(f"{fname}: 'editorial_md' must document complexity")
        if "pitfall" not in ed_lower and "mistake" not in ed_lower:
            errors.append(f"{fname}: 'editorial_md' must document common pitfalls or mistakes")

    # 12. reference_solutions
    ref = data.get("reference_solutions")
    if not ref or not isinstance(ref, dict):
        errors.append(f"{fname}: Missing 'reference_solutions' dictionary")
    else:
        for lang in ["brute_python", "optimal_python", "optimal_java", "optimal_cpp"]:
            if not ref.get(lang) or len(ref[lang].strip()) < 10:
                errors.append(f"{fname}: Missing reference solution for '{lang}'")

    return errors

def run_tests_for_problem(data: dict, filepath: str) -> list[str]:
    """Runs optimal_python against all tests and brute_python against sample tests."""
    failures = []
    fname = os.path.basename(filepath)
    ref = data.get("reference_solutions", {})
    optimal_py = ref.get("optimal_python")
    brute_py = ref.get("brute_python")

    all_tests = []
    for idx, t in enumerate(data.get("sample_tests", [])):
        all_tests.append(("sample", idx + 1, t))
    for idx, t in enumerate(data.get("hidden_tests", [])):
        all_tests.append(("hidden", idx + 1, t))

    # Test optimal_python
    if optimal_py:
        for category, num, test in all_tests:
            inp = test.get("input_text", "")
            exp = test.get("expected_output", "")
            ok, actual = execute_python_solution(optimal_py, inp)
            if not ok:
                failures.append(f"{fname} [optimal_python {category} #{num}]: {actual} (Input: {inp!r})")
            elif normalize_output(actual) != normalize_output(exp):
                failures.append(
                    f"{fname} [optimal_python {category} #{num}]: Output mismatch.\n"
                    f"  Expected: {exp}\n"
                    f"  Actual:   {actual}\n"
                    f"  Input:    {inp!r}"
                )

    # Test brute_python against sample tests
    if brute_py:
        for idx, test in enumerate(data.get("sample_tests", [])):
            inp = test.get("input_text", "")
            exp = test.get("expected_output", "")
            ok, actual = execute_python_solution(brute_py, inp)
            if not ok:
                failures.append(f"{fname} [brute_python sample #{idx + 1}]: {actual}")
            elif normalize_output(actual) != normalize_output(exp):
                failures.append(
                    f"{fname} [brute_python sample #{idx + 1}]: Output mismatch.\n"
                    f"  Expected: {exp}\n"
                    f"  Actual:   {actual}"
                )

    return failures

def main():
    problems_dir = os.path.join(os.path.dirname(__file__), "..", "content", "problems")
    files = sorted(glob.glob(os.path.join(problems_dir, "*.json")))

    print("=" * 70)
    print(f"READY2CODE PROBLEM BANK VALIDATION & CI TEST HARNESS")
    print(f"Scanning directory: {os.path.abspath(problems_dir)}")
    print(f"Discovered problem files: {len(files)}")
    print("=" * 70)

    if not files:
        print("ERROR: No problem JSON files discovered in content/problems/")
        sys.exit(1)

    schema_errors = []
    runtime_failures = []
    topic_distribution = {}
    difficulty_distribution = {"easy": 0, "medium": 0, "hard": 0}

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as fp:
            try:
                data = json.load(fp)
            except Exception as e:
                schema_errors.append(f"{os.path.basename(fpath)}: Corrupted JSON - {str(e)}")
                continue

        # Tally stats
        top = data.get("topic", "Unknown")
        diff = data.get("difficulty", "unknown").lower()
        topic_distribution[top] = topic_distribution.get(top, 0) + 1
        if diff in difficulty_distribution:
            difficulty_distribution[diff] += 1

        # Validate Schema
        errs = validate_problem(data, fpath)
        if errs:
            schema_errors.extend(errs)
        else:
            # Run code tests if schema passed
            fails = run_tests_for_problem(data, fpath)
            if fails:
                runtime_failures.extend(fails)

    print("\n--- Current Topic Distribution ---")
    for top, cnt in sorted(topic_distribution.items()):
        print(f"  {top}: {cnt}")

    print("\n--- Difficulty Distribution ---")
    for diff, cnt in difficulty_distribution.items():
        print(f"  {diff.capitalize()}: {cnt}")

    print(f"\nTotal Validated Files: {len(files)}")

    if schema_errors or runtime_failures:
        print("\n" + "!" * 70)
        print("VALIDATION FAILED WITH ERRORS:")
        for err in schema_errors:
            print(f"  [SCHEMA ERROR] {err}")
        for fail in runtime_failures:
            print(f"  [TEST FAILURE] {fail}")
        print("!" * 70)
        sys.exit(1)
    else:
        print("\n" + "*" * 70)
        print(f"SUCCESS: All {len(files)} problems verified with 100% test pass rate!")
        print("*" * 70)
        sys.exit(0)

if __name__ == "__main__":
    main()
