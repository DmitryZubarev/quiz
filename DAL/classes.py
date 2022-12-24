from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Interval, Boolean
from sqlalchemy.orm import declarative_base

db = declarative_base()


# session
class Session(db):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    date_start = Column(TIMESTAMP)
    date_end = Column(TIMESTAMP)


class SelectedOption(db):
    __tablename__ = "selected_option"
    id = Column(Integer, primary_key=True)
    id_option = None
    id_answer = None


class SelectedMatch:
    __tablename__ = "selected_match"
    id = Column(Integer, primary_key=True)
    id_promt = None
    id_match = None
    id_answer = None


class SelectedBinaryTrue:
    __tablename__ = "selected_binary_true"
    id = Column(Integer, primary_key=True)
    id_answer = None


class SessionUser:
    __tablename__ = "session_user"
    id = Column(Integer, primary_key=True)
    name = None
    picture = None
    id_session = None
    email = None


class Answer:
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    response_time = None
    id_session = None
    id_question = None
    id_session_user = None


# session


# question
class Question:
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    content = Column(String),
    duration = Column(Interval),
    response_rate = Column(Boolean),
    random_answers = Column(Boolean),
    min_score = Column(Integer),
    max_score = Column(Integer)


class Option:
    __tablename__ = "option"
    id = Column(Integer, primary_key=True)
    content = None
    correct = None
    priority = None
    id_question = None


class Promt:
    __tablename__ = "promt"
    id = Column(Integer, primary_key=True)
    content = None
    priority = None
    id_question = None


class Match:
    __tablename__ = "match"
    id = Column(Integer, primary_key=True)
    content = None
    id_promt = None


class BinaryTrue:
    __tablename__ = "binary_true"
    id = Column(Integer, primary_key=True)
    id_question = None


# question


# account
class UserAccount:
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = None
    email = None
    password = None
    activate = None
    activate_code = None
    date_reg = None
    id_role = None


class Role:
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class UserGroup:
    __tablename__ = "user_group"
    id = Column(Integer, primary_key=True)
    name = Column(String),
    code = Column(String)


class UserConfig:
    __tablename__ = "user_config"
    id = Column(Integer, primary_key=True)
    language = None
    id_user_account = None
    usage_format = None


# account


# presentation
class Presentation:
    __tablename__ = "presentation"
    id = Column(Integer, primary_key=True)
    name = None
    visable = None
    code = None
    date_creation = None
    image = None
    description = None
    emoji = None
    timer = None
    connection_moderation = None
    music = None
    random_slide = None
    id_category = None
    id_theme = None
    id_music = None
    id_presentation_logo = None
    max_scale = None
    min_scale = None


class Slide:
    __tablename__ = "slide"
    id = Column(Integer, primary_key=True)
    color_text = None
    priority = None
    id_presentation = None
    id_slide_type = None


class Category:
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Theme:
    __tablename__ = "theme"
    id = Column(Integer, primary_key=True)
    name = Column(String),
    file = Column(String)


class Music:
    __tablename__ = "music"
    id = Column(Integer, primary_key=True)
    name = Column(String),
    file = Column(String)


class SlideType:
    __tablename__ = "slide_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class PresentationLogo:
    __tablename__ = "presentation_logo"
    id = Column(Integer, primary_key=True)
    name = Column(String),
    file = Column(String)

# presentation
