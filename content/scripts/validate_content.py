"""Judge-style check for content/problems/*.json.
Runs each reference_python against sample_tests and hidden_tests, the same way the judge will.
Usage: python scripts/validate_content.py   (run from the repo root)
Exit code 1 if any problem fails or has fewer than 8 hidden tests."""
import glob, json, copy, sys

failures, total, min_hidden = [], 0, 10**9
for path in sorted(glob.glob("content/problems/*.json")):
    d = json.load(open(path))
    ns = {}
    exec(d["reference_python"], ns)
    fn = ns[d["function_name"]]
    min_hidden = min(min_hidden, len(d["hidden_tests"]))
    if len(d["hidden_tests"]) < 8:
        failures.append((d["slug"], "fewer than 8 hidden tests"))
    for t in d["sample_tests"] + d["hidden_tests"]:
        total += 1
        got = json.loads(json.dumps(fn(*copy.deepcopy(t["input"]))))
        if got != t["output"]:
            failures.append((d["slug"], t["input"], got, t["output"]))
            break
print(f"problems checked, tests run: {total}, min hidden per problem: {min_hidden}, failures: {len(failures)}")
for f in failures:
    print("FAIL", f)
sys.exit(1 if failures else 0)
