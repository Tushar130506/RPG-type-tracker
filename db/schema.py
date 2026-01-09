from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text
from db.database import Base

#---Daily Log

class DailyLogTable(Base):
    __tablename__ = "daily_log"

    id = Column(Integer, primary_key=True)
    log_date = Column(Date, unique=True, nullable=False)
    raw_text = Column(Text, nullable=False)
    journaled_text = Column(Text)

#---Task

class TaskTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    planned = Column(Boolean, default=True)
    completed = Column(Boolean, default=False)
    log_date = Column(Date)

#----XP Event

class XPEventTable(Base):
    __tablename__ = "xp_events"

    id = Column(Integer, primary_key=True)
    stat = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    reason = Column(String)
    log_date = Column(Date, nullable=False)

#---Stat Snapshot

class StatSnapshotTable(Base):
    __tablename__ = "stat_snapshots"

    id = Column(Integer, primary_key=True)
    log_date = Column(Date, unique=True)

    strength = Column(Integer)
    intelligence = Column(Integer)
    lifestyle = Column(Integer)
    mental_health = Column(Integer)
    financial_health = Column(Integer)
    ovr = Column(Integer)

       