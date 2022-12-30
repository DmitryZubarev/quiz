from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Interval, Boolean, VARCHAR, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship

"""https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many"""

engine = create_engine("postgresql+psycopg2://postgres:Dc028ed7_@localhost/quiz")
db = declarative_base()


# session
class Session(db):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    date_start = Column(TIMESTAMP)
    date_end = Column(TIMESTAMP)

    answer = relationship("Answer", back_populates="session")
    session_user = relationship("SessionUser", back_populates="session")


class SelectedOption(db):
    __tablename__ = "selected_option"
    id = Column(Integer, primary_key=True)
    id_option = Column(Integer, ForeignKey("option.id"))
    id_answer = Column(Integer, ForeignKey("answer.id"))

    option = relationship("Option", back_populates="selected_option")
    answer = relationship("Answer", back_populates="selected_option")


class SelectedMatch(db):
    __tablename__ = "selected_match"
    id = Column(Integer, primary_key=True)
    id_promt = Column(Integer, ForeignKey("promt.id"))
    id_match = Column(Integer, ForeignKey("match.id"))
    id_answer = Column(Integer, ForeignKey("answer.id"))

    promt = relationship("Promt", back_populates="selected_match")
    match = relationship("Match", back_populates="selected_match")
    answer = relationship("Answer", back_populates="selected_match")


class SelectedBinaryTrue(db):
    __tablename__ = "selected_binary_true"
    id = Column(Integer, primary_key=True)
    id_answer = Column(Integer, ForeignKey("answer.id"))

    answer = relationship("Answer", back_populates="selected_binary_true")


class SessionUser(db):
    __tablename__ = "session_user"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    picture = Column(VARCHAR(255))
    id_session = Column(Integer, ForeignKey("session.id"))
    email = Column(VARCHAR(255))

    session = relationship("Session", back_populates="session_user")
    answer = relationship("Answer", back_populates="session_user")


class Answer(db):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    response_time = Column(Interval)
    id_session = Column(Integer, ForeignKey("session.id"))
    id_question = Column(Integer, ForeignKey("question.id"))
    id_session_user = Column(Integer, ForeignKey("session_user.id"))

    session = relationship("Session", back_populates="answer")
    question = relationship("Qeustion", back_populates="answer")
    session_user = relationship("SessionUser", back_populates="answer")
    selected_option = relationship("SelectedOption", back_populates="answer")
    selected_match = relationship("SelectedMatch", back_populates="answer")
    selected_binary_true = relationship("SelectedBinaryTrue", back_populates="answer")


# session


# question
class Question(db):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    duration = Column(Interval)
    response_rate = Column(Boolean)
    random_answers = Column(Boolean)
    min_score = Column(Integer)
    max_score = Column(Integer)

    answer = relationship("Answer", back_populates="question")
    option = relationship("Option", back_populates="question")
    promt = relationship("Promt", back_populates="question")
    binary_true = relationship("BinaryTrue", back_populates="question")


class Option(db):
    __tablename__ = "option"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    correct = Column(Boolean)
    priority = Column(Integer)
    id_question = Column(Integer, ForeignKey("question.id"))

    selected_option = relationship("SelectedOption", back_populates="option")
    question = relationship("Question", back_populates="option")


class Promt(db):
    __tablename__ = "promt"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    priority = Column(Integer)
    id_question = Column(Integer, ForeignKey("question.id"))

    selected_match = relationship("SelectedMatch", back_populates="promt")
    question = relationship("Question", back_populates="promt")
    match = relationship("Match", back_populates="promt")


class Match(db):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    id_promt = Column(Integer, ForeignKey("promt.id"))

    selected_match = relationship("SelectedMatch", back_populates="match")
    promt = relationship("Promt", back_populates="match")


class BinaryTrue(db):
    __tablename__ = "binary_true"
    id = Column(Integer, primary_key=True)
    id_question = Column(Integer, ForeignKey("question.id"))

    question = relationship("Question", back_populates="binary_true")


# question


# account
class UserAccount(db):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(500))
    email = Column(VARCHAR(500))
    password = Column(VARCHAR(500))
    activate = Column(Boolean)
    activate_code = Column(VARCHAR(500))
    date_reg = Column(TIMESTAMP)
    id_role = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="user_account")
    user_config = relationship("UserConfig", back_populates="user_account")


class Role(db):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    user_account = relationship("UserAccount", back_populates="role")


class UserGroup(db):
    __tablename__ = "user_group"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)

    # надо ли добавлять поля для отношения UserGroup - UserAccount?????????


class UserConfig(db):
    __tablename__ = "user_config"
    id = Column(Integer, primary_key=True)
    language = Column(VARCHAR(255))
    id_user_account = Column(Integer, ForeignKey("user_account.id"))
    usage_format = Column(VARCHAR(255))

    user_account = relationship("UserAccount", back_populates="user_config")


# account


# presentation
class Presentation(db):
    __tablename__ = "presentation"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    visible = Column(Boolean)
    code = Column(VARCHAR(255))
    date_creation = Column(TIMESTAMP)
    image = Column(VARCHAR(500))
    description = Column(Text)
    emoji = Column(Boolean)
    timer = Column(Boolean)
    connection_moderation = Column(Boolean)
    music = Column(Boolean)
    random_slide = Column(Boolean)
    id_category = Column(Integer, ForeignKey("category.id"))
    id_theme = Column(Integer, ForeignKey("theme.id"))
    id_music = Column(Integer, ForeignKey("music.id"))
    id_presentation_logo = Column(Integer, ForeignKey("presentation_logo.id"))
    max_scale = Column(Integer)
    min_scale = Column(Integer)

    category = relationship("Category", back_populates="presentation")
    theme = relationship("Theme", back_populates="presentation")
    music = relationship("Music", back_populates="presentation")
    presentation_logo = relationship("PresentationLogo", back_populates="presentation")
    slide = relationship("Slide", back_populates="presentation")


class Slide(db):
    __tablename__ = "slide"
    id = Column(Integer, primary_key=True)
    color_text = Column(VARCHAR(255))
    priority = Column(Integer)
    id_presentation = Column(Integer, ForeignKey("presentation.id"))
    id_slide_type = Column(Integer, ForeignKey("slide_type.id"))

    presentation = relationship("Presentation", back_populates="slide")
    slide_type = relationship("SlideType", back_populates="slide")


class Category(db):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    presentation = relationship("Presentation", back_populates="category")


class Theme(db):
    __tablename__ = "theme"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(String)

    presentation = relationship("Presentation", back_populates="theme")


class Music(db):
    __tablename__ = "music"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(String)

    presentation = relationship("Presentation", back_populates="music")


class SlideType(db):
    __tablename__ = "slide_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    slide = relationship("Slide", back_populates="slide_type")


class PresentationLogo(db):
    __tablename__ = "presentation_logo"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(String)

    presentation = relationship("Presentation", back_populates="presentation_logo")

# presentation


db.metadata.create_all(engine)
