import os
import sys
import glob
import json
from datetime import datetime, timedelta, timezone

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine, SessionLocal, Base
from app.models.entities import (
    Topic, Problem, ProblemTag, ProblemTest, ProblemHint, Editorial,
    ProblemList, ListItem, StudyPlan, PlanDay, Contest, ContestProblem,
    ContestEntry, User, Discussion
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
        search_path = os.path.join(os.getcwd(), "content", "problems", "*.json")
        files = glob.glob(search_path)

    seeded_count = 0
    problem_cache = {}

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        validate_problem_dict(data, os.path.basename(fpath))

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

        problem_cache[prob.slug] = prob

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

    # --- Phase 2: Seed System Lists (Blind 75 & NeetCode 150) ---
    system_lists = [
        {
            "name": "Blind 75 High-Frequency Core",
            "description": "Essential foundational algorithmic patterns curated for top tech interviews.",
            "slugs": ["two-sum-sorted-offsets", "balanced-bracket-delimiter-validator", "container-with-bounded-walls", "equilibrium-pivot-index", "invert-singly-linked-chain", "number-of-connected-islands", "coin-change-fewest-coins", "merge-overlapping-intervals-timeline", "two-sum"]
        },
        {
            "name": "NeetCode 150 Essentials",
            "description": "Structured curriculum spanning arrays, linked lists, trees, graphs, and dynamic programming.",
            "slugs": ["two-sum-sorted-offsets", "balanced-bracket-delimiter-validator", "standard-binary-search-exact", "longest-substring-k-distinct-chars", "climbing-step-variations", "binary-tree-inorder-values", "two-sum"]
        }
    ]

    for sl in system_lists:
        pl = db.query(ProblemList).filter(ProblemList.name == sl["name"]).first()
        if not pl:
            pl = ProblemList(name=sl["name"], description=sl["description"], is_system=True, visibility="public")
            db.add(pl)
            db.commit()
            db.refresh(pl)

        db.query(ListItem).filter(ListItem.list_id == pl.id).delete()
        for idx, slug in enumerate(sl["slugs"]):
            p = problem_cache.get(slug) or db.query(Problem).filter(Problem.slug == slug).first()
            if p:
                db.add(ListItem(list_id=pl.id, problem_id=p.id, position=idx))
        db.commit()

    # --- Phase 2: Seed Study Plans (30/60/90 Days) ---
    plan = db.query(StudyPlan).filter(StudyPlan.name == "30-Day Interview Readiness Bootcamp").first()
    if not plan:
        plan = StudyPlan(
            name="30-Day Interview Readiness Bootcamp",
            description="Daily assigned algorithmic challenges progressing from arrays to dynamic programming.",
            duration_days=30
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)

        day_assignments = [
            (1, "two-sum-sorted-offsets"),
            (2, "container-with-bounded-walls"),
            (3, "balanced-bracket-delimiter-validator"),
            (4, "standard-binary-search-exact"),
            (5, "invert-singly-linked-chain"),
            (6, "equilibrium-pivot-index"),
            (7, "climbing-step-variations"),
            (8, "number-of-connected-islands"),
            (9, "merge-overlapping-intervals-timeline"),
            (10, "longest-substring-k-distinct-chars"),
            (11, "coin-change-fewest-coins"),
            (12, "binary-tree-inorder-values")
        ]
        for day_num, slug in day_assignments:
            p = problem_cache.get(slug) or db.query(Problem).filter(Problem.slug == slug).first()
            if p:
                db.add(PlanDay(plan_id=plan.id, day_number=day_num, problem_id=p.id))
        db.commit()

    # --- Phase 2: Seed Contests ---
    contest = db.query(Contest).filter(Contest.title == "Ready2Code Weekly Contest 101").first()
    if not contest:
        contest = Contest(
            title="Ready2Code Weekly Contest 101",
            starts_at=datetime.now(timezone.utc) - timedelta(hours=1),
            duration_min=90,
            type="weekly",
            status="live"
        )
        db.add(contest)
        db.commit()
        db.refresh(contest)

        c_probs = [("two-sum-sorted-offsets", 100, 1), ("equilibrium-pivot-index", 200, 2), ("number-of-connected-islands", 300, 3)]
        for slug, pts, pos in c_probs:
            p = problem_cache.get(slug) or db.query(Problem).filter(Problem.slug == slug).first()
            if p:
                db.add(ContestProblem(contest_id=contest.id, problem_id=p.id, points=pts, position=pos))

        # Add sample contestants
        u1 = db.query(User).filter(User.username == "algo_ninja").first()
        if not u1:
            u1 = User(id="user_ninja", username="algo_ninja", display_name="Ninja Coder", rating=1820)
            db.add(u1)
        u2 = db.query(User).filter(User.username == "byte_master").first()
        if not u2:
            u2 = User(id="user_byte", username="byte_master", display_name="Byte Master", rating=1750)
            db.add(u2)
        db.commit()

        db.add(ContestEntry(contest_id=contest.id, user_id=u1.id, score=300, penalty_s=180, rank=1))
        db.add(ContestEntry(contest_id=contest.id, user_id=u2.id, score=100, penalty_s=300, rank=2))
        db.commit()

    db.close()
    print(f"Successfully seeded {seeded_count} problems, lists, study plans, and live contests idempotently.")

if __name__ == "__main__":
    seed_database()
