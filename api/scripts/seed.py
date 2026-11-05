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

TOPIC_CONFIG = [
    ("Arrays and Hashing", "arrays", 1),
    ("Two Pointers and Sliding Window", "two_pointers", 2),
    ("Strings", "strings", 3),
    ("Stack and Queue", "stack", 4),
    ("Linked List", "linked_list", 5),
    ("Trees", "trees", 6),
    ("Graphs", "graphs", 7),
    ("Binary Search", "binary_search", 8),
    ("Dynamic Programming", "dp", 9),
    ("Heap, Intervals and Greedy", "heap_greedy", 10),
]

def validate_problem_dict(p_dict: dict, filename: str):
    required = ["slug", "title", "difficulty", "statement_md", "sample_tests", "hidden_tests"]
    for field in required:
        if field not in p_dict:
            raise ValueError(f"File {filename} missing required field '{field}'")
    if not p_dict.get("hidden_tests") or len(p_dict["hidden_tests"]) == 0:
        raise ValueError(f"File {filename} rejected: must have at least one hidden test!")

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Pre-seed standard 10 topics in exact order
        topic_cache = {}
        for name, slug, order_idx in TOPIC_CONFIG:
            t = db.query(Topic).filter((Topic.name == name) | (Topic.slug == slug)).first()
            if not t:
                t = Topic(name=name, slug=slug, order_index=order_idx)
                db.add(t)
                db.commit()
                db.refresh(t)
            else:
                t.name = name
                t.slug = slug
                t.order_index = order_idx
                db.commit()

            topic_cache[name.lower()] = t
            topic_cache[slug.lower()] = t
            topic_cache[slug.replace("_", "-").lower()] = t

        # Also map alternative aliases for robust lookup
        if "arrays and hashing" in topic_cache:
            topic_cache["arrays"] = topic_cache["arrays and hashing"]
        if "dynamic programming" in topic_cache:
            topic_cache["dp"] = topic_cache["dynamic programming"]
        if "heap, intervals and greedy" in topic_cache:
            topic_cache["heap"] = topic_cache["heap, intervals and greedy"]
            topic_cache["intervals"] = topic_cache["heap, intervals and greedy"]
            topic_cache["greedy"] = topic_cache["heap, intervals and greedy"]

        # 2. Locate problem JSON files
        candidate_paths = [
            os.path.join(os.getcwd(), "content", "problems", "*.json"),
            os.path.join(os.path.dirname(__file__), "..", "..", "content", "problems", "*.json"),
            os.path.join(os.path.dirname(__file__), "..", "content", "problems", "*.json"),
        ]
        files = []
        for p in candidate_paths:
            found = glob.glob(p)
            if found:
                files = found
                break

        if not files:
            print("No problem files found under content/problems/")
            return 0, 0

        # Sort files for deterministic processing
        files.sort()

        new_problems_count = 0
        updated_problems_count = 0

        for fpath in files:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            validate_problem_dict(data, os.path.basename(fpath))

            prob = db.query(Problem).filter(Problem.slug == data["slug"]).first()
            topic_val = (data.get("topic") or data.get("topic_key") or "arrays").lower()
            topic_obj = topic_cache.get(topic_val) or topic_cache.get(data.get("topic_key", "").lower())
            topic_id = topic_obj.id if topic_obj else None

            starter_code = data.get("starter_code")
            starter_code_str = json.dumps(starter_code) if isinstance(starter_code, (dict, list)) else (starter_code or "")
            scene_val = data.get("scene", "array")

            if not prob:
                prob = Problem(
                    slug=data["slug"],
                    title=data["title"],
                    statement_md=data["statement_md"],
                    difficulty=data.get("difficulty", "easy").lower(),
                    topic_id=topic_id,
                    time_limit_ms=data.get("time_limit_ms", 1000),
                    memory_limit_mb=data.get("memory_limit_mb", 128),
                    problem_type="standard",
                    scene=scene_val,
                    starter_code=starter_code_str,
                    is_published=True
                )
                db.add(prob)
                db.commit()
                db.refresh(prob)
                new_problems_count += 1
            else:
                prob.title = data["title"]
                prob.statement_md = data["statement_md"]
                prob.difficulty = data.get("difficulty", "easy").lower()
                prob.topic_id = topic_id
                prob.time_limit_ms = data.get("time_limit_ms", 1000)
                prob.memory_limit_mb = data.get("memory_limit_mb", 128)
                prob.scene = scene_val
                prob.starter_code = starter_code_str
                db.commit()
                updated_problems_count += 1

            # Update Problem Tests (idempotent: replace with exact tests)
            db.query(ProblemTest).filter(ProblemTest.problem_id == prob.id).delete()
            test_records = []
            
            # Sample tests (is_hidden = False)
            for idx, test in enumerate(data.get("sample_tests", [])):
                in_str = json.dumps(test["input"]) if not isinstance(test["input"], str) else test["input"]
                out_str = json.dumps(test["output"]) if not isinstance(test["output"], str) else test["output"]
                test_records.append(
                    ProblemTest(
                        problem_id=prob.id,
                        input_text=in_str,
                        expected_output=out_str,
                        is_hidden=False,
                        order_index=idx
                    )
                )

            # Hidden tests (is_hidden = True)
            offset = len(test_records)
            for idx, test in enumerate(data.get("hidden_tests", [])):
                in_str = json.dumps(test["input"]) if not isinstance(test["input"], str) else test["input"]
                out_str = json.dumps(test["output"]) if not isinstance(test["output"], str) else test["output"]
                test_records.append(
                    ProblemTest(
                        problem_id=prob.id,
                        input_text=in_str,
                        expected_output=out_str,
                        is_hidden=True,
                        order_index=offset + idx
                    )
                )
            db.bulk_save_objects(test_records)

            # Update Problem Hints (idempotent: replace with exact 3 hints)
            db.query(ProblemHint).filter(ProblemHint.problem_id == prob.id).delete()
            hints_list = data.get("hints", [])
            hint_records = []
            for h_idx, hint_text in enumerate(hints_list):
                level = h_idx + 1
                xp_cost = 2 if level == 1 else (5 if level == 2 else 10)
                hint_records.append(
                    ProblemHint(
                        problem_id=prob.id,
                        level=level,
                        text=hint_text,
                        xp_cost=xp_cost
                    )
                )
            db.bulk_save_objects(hint_records)

            # Update Tags (topic + pattern / tags)
            db.query(ProblemTag).filter(ProblemTag.problem_id == prob.id).delete()
            tags = set(data.get("tags", []))
            if topic_obj:
                tags.add(topic_obj.slug)
                tags.add(topic_obj.name.lower())
            if data.get("topic_key"):
                tags.add(data["topic_key"])
            tag_records = [ProblemTag(problem_id=prob.id, tag=t) for t in tags if t]
            db.bulk_save_objects(tag_records)

            # Ensure Editorial exists for problem
            existing_editorial = db.query(Editorial).filter(Editorial.problem_id == prob.id).first()
            if not existing_editorial:
                topic_str = topic_obj.name if topic_obj else "Algorithm"
                db.add(Editorial(
                    problem_id=prob.id,
                    body_md=f"### Optimal Strategy for {prob.title}\n\nLeverage the standard {topic_str} paradigm to process elements systematically while maintaining state in optimal complexity.",
                    approach=f"Optimal {topic_str} Pattern",
                    complexity_time="O(n)",
                    complexity_space="O(1)"
                ))

            db.commit()

        # 3. Seed Mock Users for Development and Tests
        mock_users = [
            {"id": "usr_algo_ninja", "username": "algo_ninja", "display_name": "Algo Ninja", "rating": 1650},
            {"id": "usr_byte_master", "username": "byte_master", "display_name": "Byte Master", "rating": 1780},
        ]
        for u in mock_users:
            existing = db.query(User).filter(User.username == u["username"]).first()
            if not existing:
                db.add(User(
                    id=u["id"],
                    username=u["username"],
                    display_name=u["display_name"],
                    rating=u["rating"]
                ))
                db.commit()

        # 4. Seed Standard Lists (Blind 75, NeetCode 150)
        system_lists = [
            ("Blind 75", "Core 75 high-frequency questions essential for tech interviews."),
            ("NeetCode 150", "Structured 150-problem mastery syllabus covering all major DSA patterns.")
        ]
        all_problems = db.query(Problem).filter(Problem.is_published == True).all()
        for list_name, list_desc in system_lists:
            plist = db.query(ProblemList).filter(ProblemList.name == list_name).first()
            if not plist:
                plist = ProblemList(
                    name=list_name,
                    description=list_desc,
                    is_system=True,
                    visibility="public"
                )
                db.add(plist)
                db.commit()
                db.refresh(plist)
                # Attach up to 25 seeded problems as items
                for pos, p in enumerate(all_problems[:25]):
                    db.add(ListItem(list_id=plist.id, problem_id=p.id, position=pos))
                db.commit()

        # 5. Seed Standard Study Plans
        plan = db.query(StudyPlan).filter(StudyPlan.id == "plan-30-day").first()
        if not plan:
            plan = StudyPlan(
                id="plan-30-day",
                name="30-Day Interview Preparation Bootcamp",
                description="Comprehensive 30-day algorithmic study plan covering foundational data structures and advanced patterns.",
                duration_days=30
            )
            db.add(plan)
            db.commit()
            if all_problems:
                for day in range(1, 31):
                    prob_idx = (day - 1) % len(all_problems)
                    db.add(PlanDay(plan_id=plan.id, day_number=day, problem_id=all_problems[prob_idx].id))
                db.commit()

        # 6. Seed Live/Upcoming Contests
        contest = db.query(Contest).filter(Contest.id == "contest-1").first()
        if not contest:
            now = datetime.now(timezone.utc)
            contest = Contest(
                id="contest-1",
                title="Weekly Bi-Virtual Arena #1",
                starts_at=now - timedelta(minutes=10),
                duration_min=90,
                type="Standard DSA",
                status="live"
            )
            db.add(contest)
            db.commit()
            if len(all_problems) >= 3:
                for idx, p in enumerate(all_problems[:3]):
                    db.add(ContestProblem(contest_id=contest.id, problem_id=p.id, points=(idx+1)*100, position=idx))
                db.commit()

        # Ensure at least one contest entry exists for standings
        entry = db.query(ContestEntry).filter(ContestEntry.contest_id == "contest-1").first()
        if not entry:
            db.add(ContestEntry(
                contest_id="contest-1",
                user_id="usr_algo_ninja",
                score=200,
                penalty_s=120
            ))
            db.commit()

        # Total counts verification
        total_problems = db.query(Problem).filter(Problem.is_published == True).count()
        total_topics = db.query(Topic).count()

        if new_problems_count > 0:
            print(f"Loaded {new_problems_count} problems.")
        else:
            print("Loaded 0 new problems (all problems already present in database).")
        print(f"Total problems in database: {total_problems}")
        print(f"Total topics in database: {total_topics}")

        return new_problems_count, total_problems

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
