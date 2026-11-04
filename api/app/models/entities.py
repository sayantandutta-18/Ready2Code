import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Index, PrimaryKeyConstraint
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
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    problem_statuses = relationship("UserProblemStatus", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("Streak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    xp_entries = relationship("XPLedger", back_populates="user", cascade="all, delete-orphan")

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
    is_published = Column(Boolean, default=True)

    topic = relationship("Topic", back_populates="problems")
    tags = relationship("ProblemTag", back_populates="problem", cascade="all, delete-orphan")
    tests = relationship("ProblemTest", back_populates="problem", cascade="all, delete-orphan", order_by="ProblemTest.order_index")
    hints = relationship("ProblemHint", back_populates="problem", cascade="all, delete-orphan", order_by="ProblemHint.level")
    editorial = relationship("Editorial", back_populates="problem", uselist=False, cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")

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
    created_at = Column(DateTime, default=datetime.utcnow)

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
