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
    "Heap and Intervals",
    "Heap, Intervals and Greedy"
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
    """Validates problem schema against all requirements."""
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

    # 5. statement_md
    stmt = data.get("statement_md", "")
    if len(stmt.strip()) < 30:
        errors.append(f"{fname}: 'statement_md' is missing or too brief")

    # 6. examples (if present)
    examples = data.get("examples")
    if examples and isinstance(examples, list):
        for idx, ex in enumerate(examples):
            if not ex.get("input") and ex.get("input") != 0 and ex.get("input") != [] and ex.get("input") != "":
                errors.append(f"{fname}: Example {idx + 1} missing input")

    # 7. sample_tests
    samples = data.get("sample_tests")
    if not samples or not isinstance(samples, list) or len(samples) < 1:
        errors.append(f"{fname}: Must have at least 1 sample_test (found {len(samples) if samples else 0})")

    # 8. hidden_tests
    hidden = data.get("hidden_tests")
    if not hidden or not isinstance(hidden, list) or len(hidden) < 8:
        errors.append(f"{fname}: Must have at least 8 hidden_tests (found {len(hidden) if hidden else 0})")

    # 9. hints
    hints = data.get("hints")
    if not hints or len(hints) != 3:
        errors.append(f"{fname}: Must contain exactly 3 hints (levels 1, 2, 3)")
    else:
        for idx, h in enumerate(hints):
            if isinstance(h, dict):
                if h.get("level") == 3 and "`" in h.get("text", ""):
                    errors.append(f"{fname}: Hint level 3 must not contain code blocks or backticks")
            elif isinstance(h, str):
                if idx == 2 and "def " in h:
                    errors.append(f"{fname}: Hint level 3 must not contain code solutions")

    # 10. verification mechanism
    has_ref_py = "reference_python" in data and bool(data["reference_python"].strip())
    has_ref_solutions = "reference_solutions" in data and isinstance(data["reference_solutions"], dict)
    if not has_ref_py and not has_ref_solutions:
        errors.append(f"{fname}: Missing reference implementation ('reference_python' or 'reference_solutions')")

    return errors

def run_tests_for_problem(data: dict, filepath: str) -> list[str]:
    """Runs reference solution against all tests."""
    failures = []
    fname = os.path.basename(filepath)

    # 1. Check if problem uses reference_python (launch problem bank format)
    if "reference_python" in data and data.get("function_name"):
        import copy
        ns = {}
        try:
            exec(data["reference_python"], ns)
            fn = ns[data["function_name"]]
            for category, tests in [("sample", data.get("sample_tests", [])), ("hidden", data.get("hidden_tests", []))]:
                for idx, t in enumerate(tests):
                    inp = t["input"]
                    exp = t["output"]
                    inp_copy = copy.deepcopy(inp)
                    if isinstance(inp_copy, list):
                        try:
                            got = fn(*inp_copy)
                        except TypeError:
                            got = fn(inp_copy)
                    else:
                        got = fn(inp_copy)
                    got_json = json.loads(json.dumps(got))
                    if got_json != exp:
                        failures.append(f"{fname} [{category} #{idx + 1}]: Output mismatch. Expected: {exp!r}, Actual: {got_json!r}")
                        break
        except Exception as exc:
            failures.append(f"{fname} execution error: {str(exc)}")
        return failures

    # 2. Check if problem uses reference_solutions dict
    ref = data.get("reference_solutions", {})
    optimal_py = ref.get("optimal_python")
    brute_py = ref.get("brute_python")

    all_tests = []
    for idx, t in enumerate(data.get("sample_tests", [])):
        all_tests.append(("sample", idx + 1, t))
    for idx, t in enumerate(data.get("hidden_tests", [])):
        all_tests.append(("hidden", idx + 1, t))

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
