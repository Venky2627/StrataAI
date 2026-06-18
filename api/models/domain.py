from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from api.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class MasteryStatus(str, enum.Enum):
    NEW = "NEW"
    LEARNING = "LEARNING"
    FAMILIAR = "FAMILIAR"
    MASTERED = "MASTERED"
    DECAYING = "DECAYING"

# ---------------------------------------------------------
# Core Architecture
# ---------------------------------------------------------

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.utcnow)

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True)

# ---------------------------------------------------------
# Ingestion & Concept Engine
# ---------------------------------------------------------

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    status = Column(String, default="PROCESSING") # PROCESSING, READY, FAILED
    created_at = Column(DateTime, default=datetime.utcnow)

class Concept(Base):
    __tablename__ = "concepts"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    definition = Column(Text)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class ConceptRelationship(Base):
    __tablename__ = "concept_relationships"
    id = Column(String, primary_key=True, default=generate_uuid)
    source_concept_id = Column(String, ForeignKey("concepts.id"))
    target_concept_id = Column(String, ForeignKey("concepts.id"))
    relationship_type = Column(String, nullable=False) # e.g., 'depends_on', 'prerequisite_of'

class DocumentConcept(Base):
    __tablename__ = "document_concepts"
    document_id = Column(String, ForeignKey("documents.id"), primary_key=True)
    concept_id = Column(String, ForeignKey("concepts.id"), primary_key=True)

class ConceptOccurrence(Base):
    __tablename__ = "concept_occurrences"
    id = Column(String, primary_key=True, default=generate_uuid)
    concept_id = Column(String, ForeignKey("concepts.id"))
    document_id = Column(String, ForeignKey("documents.id"))
    page_number = Column(Integer, nullable=True)
    chunk_id = Column(String, nullable=True)

# ---------------------------------------------------------
# Mastery & Telemetry
# ---------------------------------------------------------

class UserConceptMastery(Base):
    __tablename__ = "user_concept_mastery"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    concept_id = Column(String, ForeignKey("concepts.id"), primary_key=True)
    
    status = Column(Enum(MasteryStatus), default=MasteryStatus.NEW)
    
    mastery_score = Column(Float, default=0.0)
    retention_score = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    
    review_count = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    
    last_reviewed = Column(DateTime, nullable=True)
    next_review_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ---------------------------------------------------------
# Event Logging
# ---------------------------------------------------------

class ReviewEvent(Base):
    __tablename__ = "review_events"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    concept_id = Column(String, ForeignKey("concepts.id"))
    score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    topics_covered = Column(Integer, default=0)
    questions_asked = Column(Integer, default=0)
