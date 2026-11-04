import os
import sys
import glob
import json

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine, SessionLocal, Base
from app.models.entities import (
    Topic, Problem, ProblemTag, ProblemTest, ProblemHint, Editorial
)

def validate_problem_dict(p_dict: dict, filename: str):
    required = ["slug", "title", "difficulty", "statement_md", "sample_tests", "hidden_tests"]
    for field in required:
        if field not in p_dict:
            raise ValueError(f"File {filename} missing required field '{field}'")
    if not p_dict.get("hidden_tests") or len(p_dict["hidden_tests"]) == 0:
        raise ValueError(f"File {filename} rejected: must have at least one hidden test!")

def seed_database(content_dir: str = "../content/problems"):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Pre-seed topics
    topics_data = [
        {"slug": "arrays", "name": "Arrays", "order_index": 1},
        {"slug": "strings", "name": "Strings", "order_index": 2},
        {"slug": "linked-list", "name": "Linked List", "order_index": 3},
        {"slug": "stack-and-queue", "name": "Stack and Queue", "order_index": 4},
        {"slug": "trees", "name": "Trees", "order_index": 5},
        {"slug": "graphs", "name": "Graphs", "order_index": 6},
        {"slug": "dp", "name": "Dynamic Programming", "order_index": 7},
        {"slug": "binary-search", "name": "Binary Search", "order_index": 8}
    ]

    topic_cache = {}
    for td in topics_data:
        t = db.query(Topic).filter(Topic.slug == td["slug"]).first()
        if not t:
            t = Topic(slug=td["slug"], name=td["name"], order_index=td["order_index"])
            db.add(t)
            db.commit()
            db.refresh(t)
        topic_cache[td["name"].lower()] = t
        topic_cache[td["slug"].lower()] = t

    search_path = os.path.join(os.path.dirname(__file__), content_dir, "*.json")
    files = glob.glob(search_path)
    if not files:
        # Try alternate path
        search_path = os.path.join(os.getcwd(), "content", "problems", "*.json")
        files = glob.glob(search_path)

    print(f"Found {len(files)} problem files to inspect.")
    seeded_count = 0

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        validate_problem_dict(data, os.path.basename(fpath))

        # Check idempotency
        prob = db.query(Problem).filter(Problem.slug == data["slug"]).first()
        topic_obj = topic_cache.get(data.get("topic", "Arrays").lower())
        topic_id = topic_obj.id if topic_obj else None

        if not prob:
            prob = Problem(
                slug=data["slug"],
                title=data["title"],
                statement_md=data["statement_md"],
                difficulty=data.get("difficulty", "easy").lower(),
                topic_id=topic_id,
                time_limit_ms=data.get("time_limit_ms", 1000),
                memory_limit_mb=data.get("memory_limit_mb", 128)
            )
            db.add(prob)
            db.commit()
            db.refresh(prob)
        else:
            prob.title = data["title"]
            prob.statement_md = data["statement_md"]
            prob.difficulty = data.get("difficulty", "easy").lower()
            prob.topic_id = topic_id
            db.commit()

        # Update Tags
        existing_tags = {t.tag for t in prob.tags}
        new_tags = set(data.get("tags", [])) | set(data.get("company_tags", []))
        for tag in new_tags:
            if tag not in existing_tags:
                db.add(ProblemTag(problem_id=prob.id, tag=tag))

        # Update Tests
        db.query(ProblemTest).filter(ProblemTest.problem_id == prob.id).delete()
        order_idx = 0
        for sample in data.get("sample_tests", []):
            db.add(ProblemTest(
                problem_id=prob.id,
                input_text=sample["input_text"],
                expected_output=sample["expected_output"],
                is_hidden=False,
                order_index=order_idx
            ))
            order_idx += 1

        for hidden in data.get("hidden_tests", []):
            db.add(ProblemTest(
                problem_id=prob.id,
                input_text=hidden["input_text"],
                expected_output=hidden["expected_output"],
                is_hidden=True,
                order_index=order_idx
            ))
            order_idx += 1

        # Hints
        db.query(ProblemHint).filter(ProblemHint.problem_id == prob.id).delete()
        for h in data.get("hints", []):
            db.add(ProblemHint(
                problem_id=prob.id,
                level=h["level"],
                text=h["text"],
                xp_cost=h.get("xp_cost", 0)
            ))

        # Editorial
        if data.get("editorial_md"):
            ed = db.query(Editorial).filter(Editorial.problem_id == prob.id).first()
            if not ed:
                ed = Editorial(
                    problem_id=prob.id,
                    body_md=data["editorial_md"],
                    approach=data.get("approach", "Optimal Solution"),
                    complexity_time=data.get("complexity_time", "O(n)"),
                    complexity_space=data.get("complexity_space", "O(1)")
                )
                db.add(ed)
            else:
                ed.body_md = data["editorial_md"]

        db.commit()
        seeded_count += 1

    db.close()
    print(f"Successfully seeded {seeded_count} problems idempotently.")

if __name__ == "__main__":
    seed_database()
