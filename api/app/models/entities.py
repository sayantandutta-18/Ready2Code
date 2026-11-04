import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Index, PrimaryKeyConstraint, Float
)
from sqlalchemy.orm import relationship
from ..database import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    clerk_id = Column(String(64), unique=True, nullable=True, index=True)
    username = Column(String(32), unique=True, nullable=False, index=True)
    display_name = Column(String(64), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    timezone = Column(String(64), default="UTC")
    rating = Column(Integer, default=1500)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    problem_statuses = relationship("UserProblemStatus", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("Streak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    xp_entries = relationship("XPLedger", back_populates="user", cascade="all, delete-orphan")
    discussions = relationship("Discussion", back_populates="author", cascade="all, delete-orphan")
    contest_entries = relationship("ContestEntry", back_populates="user", cascade="all, delete-orphan")
    review_items = relationship("ReviewQueue", back_populates="user", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(64), nullable=False)
    order_index = Column(Integer, default=0)
    unlock_rule = Column(String(64), nullable=True)

    problems = relationship("Problem", back_populates="topic")

class Problem(Base):
    __tablename__ = "problems"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    slug = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(128), nullable=False)
    statement_md = Column(Text, nullable=False)
    difficulty = Column(String(16), nullable=False, default="easy") # easy, medium, hard
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=True)
    time_limit_ms = Column(Integer, default=1000)
    memory_limit_mb = Column(Integer, default=128)
    problem_type = Column(String(32), default="standard") # standard, complexity, fix_bug, completion
    is_published = Column(Boolean, default=True)

    topic = relationship("Topic", back_populates="problems")
    tags = relationship("ProblemTag", back_populates="problem", cascade="all, delete-orphan")
    tests = relationship("ProblemTest", back_populates="problem", cascade="all, delete-orphan", order_by="ProblemTest.order_index")
    hints = relationship("ProblemHint", back_populates="problem", cascade="all, delete-orphan", order_by="ProblemHint.level")
    editorial = relationship("Editorial", back_populates="problem", uselist=False, cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")
    discussions = relationship("Discussion", back_populates="problem", cascade="all, delete-orphan")
    ladder_stages = relationship("LadderStage", back_populates="problem", cascade="all, delete-orphan")

class ProblemTag(Base):
    __tablename__ = "problem_tags"

    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    tag = Column(String(64), primary_key=True, index=True)

    problem = relationship("Problem", back_populates="tags")

class ProblemTest(Base):
    __tablename__ = "problem_tests"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    input_text = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)

    problem = relationship("Problem", back_populates="tests")

class ProblemHint(Base):
    __tablename__ = "problem_hints"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    level = Column(Integer, default=1) # 1, 2, 3
    text = Column(Text, nullable=False)
    xp_cost = Column(Integer, default=0)

    problem = relationship("Problem", back_populates="hints")

class Editorial(Base):
    __tablename__ = "editorials"

    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    body_md = Column(Text, nullable=False)
    approach = Column(String(128), nullable=True)
    complexity_time = Column(String(64), nullable=True)
    complexity_space = Column(String(64), nullable=True)

    problem = relationship("Problem", back_populates="editorial")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    language = Column(String(32), nullable=False)
    code = Column(Text, nullable=False)
    verdict = Column(String(16), nullable=False) # AC, WA, TLE, RE, CE
    runtime_ms = Column(Integer, default=0)
    memory_kb = Column(Integer, default=0)
    failed_test_index = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

class UserProblemStatus(Base):
    __tablename__ = "user_problem_status"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    status = Column(String(16), default="todo") # todo, attempted, solved
    best_runtime_ms = Column(Integer, nullable=True)
    solved_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="problem_statuses")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")

class Note(Base):
    __tablename__ = "notes"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    body_md = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="notes")

class DailyProblem(Base):
    __tablename__ = "daily_problems"

    date = Column(String(10), primary_key=True) # YYYY-MM-DD
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False)

class Streak(Base):
    __tablename__ = "streaks"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active_date = Column(String(10), nullable=True)
    freezes_left = Column(Integer, default=2)

    user = relationship("User", back_populates="streak")

class XPLedger(Base):
    __tablename__ = "xp_ledger"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    reason = Column(String(64), nullable=False)
    ref_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="xp_entries")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    slug = Column(String(64), unique=True, nullable=False)
    name = Column(String(64), nullable=False)
    rule_json = Column(Text, nullable=True)
    icon = Column(String(64), default="award")

class UserBadge(Base):
    __tablename__ = "user_badges"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    badge_id = Column(String(36), ForeignKey("badges.id"), primary_key=True)
    earned_at = Column(DateTime, default=datetime.utcnow)

# ================= PHASE 2 ENTITIES =================

class ProblemList(Base):
    __tablename__ = "lists"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    owner_id = Column(String(36), nullable=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False)
    visibility = Column(String(16), default="public")

    items = relationship("ListItem", back_populates="problem_list", cascade="all, delete-orphan", order_by="ListItem.position")

class ListItem(Base):
    __tablename__ = "list_items"

    list_id = Column(String(36), ForeignKey("lists.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    position = Column(Integer, default=0)

    problem_list = relationship("ProblemList", back_populates="items")
    problem = relationship("Problem")

class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    duration_days = Column(Integer, default=30) # 30, 60, 90
    owner_id = Column(String(36), nullable=True)

    days = relationship("PlanDay", back_populates="study_plan", cascade="all, delete-orphan", order_by="PlanDay.day_number")

class PlanDay(Base):
    __tablename__ = "plan_days"

    plan_id = Column(String(36), ForeignKey("study_plans.id"), primary_key=True)
    day_number = Column(Integer, primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)

    study_plan = relationship("StudyPlan", back_populates="days")
    problem = relationship("Problem")

class Contest(Base):
    __tablename__ = "contests"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    title = Column(String(128), nullable=False)
    starts_at = Column(DateTime, nullable=False)
    duration_min = Column(Integer, default=90)
    type = Column(String(32), default="weekly") # weekly, biweekly
    status = Column(String(16), default="upcoming") # upcoming, live, past

    problems = relationship("ContestProblem", back_populates="contest", cascade="all, delete-orphan", order_by="ContestProblem.position")
    entries = relationship("ContestEntry", back_populates="contest", cascade="all, delete-orphan")

class ContestProblem(Base):
    __tablename__ = "contest_problems"

    contest_id = Column(String(36), ForeignKey("contests.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    points = Column(Integer, default=100)
    position = Column(Integer, default=1)

    contest = relationship("Contest", back_populates="problems")
    problem = relationship("Problem")

class ContestEntry(Base):
    __tablename__ = "contest_entries"

    contest_id = Column(String(36), ForeignKey("contests.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    score = Column(Integer, default=0)
    penalty_s = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    contest = relationship("Contest", back_populates="entries")
    user = relationship("User", back_populates="contest_entries")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    contest_id = Column(String(36), ForeignKey("contests.id"), nullable=False)
    rating_before = Column(Integer, nullable=False)
    rating_after = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    body_md = Column(Text, nullable=False)
    is_solution = Column(Boolean, default=False)
    votes = Column(Integer, default=0)
    is_hidden = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    problem = relationship("Problem", back_populates="discussions")
    author = relationship("User", back_populates="discussions")
    comments = relationship("Comment", back_populates="discussion", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    discussion_id = Column(String(36), ForeignKey("discussions.id"), nullable=False, index=True)
    parent_id = Column(String(36), ForeignKey("comments.id"), nullable=True)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    body_md = Column(Text, nullable=False)
    votes = Column(Integer, default=0)
    is_hidden = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    discussion = relationship("Discussion", back_populates="comments")
    author = relationship("User")

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    target_type = Column(String(16), primary_key=True) # discussion, comment
    target_id = Column(String(36), primary_key=True)
    value = Column(Integer, default=1) # +1 or -1

class ReviewQueue(Base):
    __tablename__ = "review_queue"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    due_date = Column(String(10), nullable=False, index=True) # YYYY-MM-DD
    interval_days = Column(Integer, default=1) # 1, 3, 7, 21
    ease = Column(Float, default=2.5)

    user = relationship("User", back_populates="review_items")
    problem = relationship("Problem")

# ================= PHASE 3 ENTITIES =================

class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(64), nullable=False)
    lesson_md = Column(Text, nullable=False)
    template_code = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    quizzes = relationship("PatternQuiz", back_populates="pattern", cascade="all, delete-orphan")

class PatternQuiz(Base):
    __tablename__ = "pattern_quizzes"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    pattern_id = Column(String(36), ForeignKey("patterns.id"), nullable=False)
    problem_slug = Column(String(128), nullable=False)
    question_md = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False) # JSON array of options
    correct_option_index = Column(Integer, default=0)

    pattern = relationship("Pattern", back_populates="quizzes")

class LadderStage(Base):
    __tablename__ = "ladder_stages"

    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    stage = Column(String(16), primary_key=True) # brute, better, optimal
    solution_hint_md = Column(Text, nullable=False)
    max_runtime_ratio = Column(Float, default=2.0)

    problem = relationship("Problem", back_populates="ladder_stages")

class UserLadder(Base):
    __tablename__ = "user_ladder"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    stage_reached = Column(String(16), default="brute") # brute, better, optimal, mastered

class CSQuestion(Base):
    __tablename__ = "cs_questions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    track = Column(String(32), nullable=False, index=True) # os, dbms, networks, oop, lld, aptitude
    title = Column(String(255), nullable=False)
    question_md = Column(Text, nullable=False)
    answer_md = Column(Text, nullable=False)
    hindi_summary = Column(Text, nullable=True)
    bengali_summary = Column(Text, nullable=True)
    company_tags = Column(String(255), default="")

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    skill = Column(String(64), nullable=False)
    score = Column(Integer, default=100)
    verify_code = Column(String(32), unique=True, nullable=False, index=True)
    issued_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
