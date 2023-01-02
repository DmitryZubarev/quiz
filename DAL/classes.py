from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Interval, Boolean, VARCHAR, Text
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, relationship, Session as Sess
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql+pg8000://postgres:Dc028ed7_@localhost/exports", echo=True)
engine.connect()
db = declarative_base()


class Question(db):
    __tablename__ = "question"
    __table_args__ = {'schema': 'question'}
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
    __table_args__ = {'schema': 'question'}
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    correct = Column(Boolean)
    priority = Column(Integer)
    id_question = Column(Integer, ForeignKey("question.question.id"))

    selected_option = relationship("SelectedOption", back_populates="option")
    question = relationship("Question", back_populates="option")


class Promt(db):
    __tablename__ = "promt"
    __table_args__ = {'schema': 'question'}
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    priority = Column(Integer)
    id_question = Column(Integer, ForeignKey("question.question.id"))

    selected_match = relationship("SelectedMatch", back_populates="promt")
    question = relationship("Question", back_populates="promt")
    match = relationship("Match", back_populates="promt")


class Match(db):
    __tablename__ = "match"
    __table_args__ = {'schema': 'question'}
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    id_promt = Column(Integer, ForeignKey("question.promt.id"))

    selected_match = relationship("SelectedMatch", back_populates="match")
    promt = relationship("Promt", back_populates="match")


class BinaryTrue(db):
    __tablename__ = "binary_true"
    __table_args__ = {'schema': 'question'}
    id = Column(Integer, primary_key=True)
    id_question = Column(Integer, ForeignKey("question.question.id"))

    question = relationship("Question", back_populates="binary_true")


class Session(db):
    __tablename__ = "session"
    __table_args__ = {'schema': 'session'}
    id = Column(Integer, primary_key=True)
    date_start = Column(TIMESTAMP)
    date_end = Column(TIMESTAMP)

    answer = relationship("Answer", back_populates="session")
    session_user = relationship("SessionUser", back_populates="session")


class SessionUser(db):
    __tablename__ = "session_user"
    __table_args__ = {'schema': 'session'}
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    picture = Column(VARCHAR(255))
    id_session = Column(Integer, ForeignKey("session.session.id"))
    email = Column(VARCHAR(255))

    session = relationship("Session", back_populates="session_user")
    answer = relationship("Answer", back_populates="session_user")


class Answer(db):
    __tablename__ = "answer"
    __table_args__ = {'schema': 'session'}
    id = Column(Integer, primary_key=True)
    response_time = Column(Interval)
    id_session = Column(Integer, ForeignKey("session.session.id"))
    id_question = Column(Integer, ForeignKey("question.question.id"))
    id_session_user = Column(Integer, ForeignKey("session.session_user.id"))

    session = relationship("Session", back_populates="answer")
    question = relationship("Question", back_populates="answer")
    session_user = relationship("SessionUser", back_populates="answer")
    selected_option = relationship("SelectedOption", back_populates="answer")
    selected_match = relationship("SelectedMatch", back_populates="answer")
    selected_binary_true = relationship("SelectedBinaryTrue", back_populates="answer")


class SelectedOption(db):
    __tablename__ = "selected_option"
    __table_args__ = {'schema': 'session'}
    id = Column(Integer, primary_key=True)
    id_option = Column(Integer, ForeignKey("question.option.id"))
    id_answer = Column(Integer, ForeignKey("session.answer.id"))

    option = relationship("Option", back_populates="selected_option")
    answer = relationship("Answer", back_populates="selected_option")


class SelectedMatch(db):
    __tablename__ = "selected_match"
    __table_args__ = {'schema': 'session'}
    id = Column(Integer, primary_key=True)
    id_promt = Column(Integer, ForeignKey("question.promt.id"))
    id_match = Column(Integer, ForeignKey("question.match.id"))
    id_answer = Column(Integer, ForeignKey("session.answer.id"))

    promt = relationship("Promt", back_populates="selected_match")
    match = relationship("Match", back_populates="selected_match")
    answer = relationship("Answer", back_populates="selected_match")


class SelectedBinaryTrue(db):
    __tablename__ = "selected_binary_true"
    __table_args__ = {'schema': 'session'}
    id = Column(Integer, primary_key=True)
    id_answer = Column(Integer, ForeignKey("session.answer.id"))

    answer = relationship("Answer", back_populates="selected_binary_true")


class Role(db):
    __tablename__ = "role"
    __table_args__ = {'schema': 'account'}
    id = Column(Integer, primary_key=True)
    name = Column(String)

    user_account = relationship("UserAccount", back_populates="role")


class UserGroup(db):
    __tablename__ = "user_group"
    __table_args__ = {'schema': 'account'}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)


class UserAccount(db):
    __tablename__ = "user_account"
    __table_args__ = {'schema': 'account'}
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(500))
    email = Column(VARCHAR(500))
    password = Column(VARCHAR(500))
    activate = Column(Boolean)
    activate_code = Column(VARCHAR(500))
    date_reg = Column(TIMESTAMP)
    id_role = Column(Integer, ForeignKey("account.role.id"))

    role = relationship("Role", back_populates="user_account")
    user_config = relationship("UserConfig", back_populates="user_account")


class UserConfig(db):
    __tablename__ = "user_config"
    __table_args__ = {'schema': 'account'}
    id = Column(Integer, primary_key=True)
    language = Column(VARCHAR(255))
    id_user_account = Column(Integer, ForeignKey("account.user_account.id"))
    usage_format = Column(VARCHAR(255))

    user_account = relationship("UserAccount", back_populates="user_config")


class Category(db):
    __tablename__ = "category"
    __table_args__ = {'schema': 'presentation'}
    id = Column(Integer, primary_key=True)
    name = Column(String)

    presentation = relationship("Presentation", back_populates="category")


class Theme(db):
    __tablename__ = "theme"
    __table_args__ = {'schema': 'presentation'}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(String)

    presentation = relationship("Presentation", back_populates="theme")


class Music(db):
    __tablename__ = "music"
    __table_args__ = {'schema': 'presentation'}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(String)

    presentation = relationship("Presentation", back_populates="music")


class SlideType(db):
    __tablename__ = "slide_type"
    __table_args__ = {'schema': 'presentation'}
    id = Column(Integer, primary_key=True)
    name = Column(String)

    slide = relationship("Slide", back_populates="slide_type")


class PresentationLogo(db):
    __tablename__ = "presentation_logo"
    __table_args__ = {'schema': 'presentation'}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(String)

    presentation = relationship("Presentation", back_populates="presentation_logo")


class Presentation(db):
    __tablename__ = "presentation"
    __table_args__ = {'schema': 'presentation'}
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
    id_category = Column(Integer, ForeignKey("presentation.category.id"))
    id_theme = Column(Integer, ForeignKey("presentation.theme.id"))
    id_music = Column(Integer, ForeignKey("presentation.music.id"))
    id_presentation_logo = Column(Integer, ForeignKey("presentation.presentation_logo.id"))
    max_scale = Column(Integer)
    min_scale = Column(Integer)

    category = relationship("Category", back_populates="presentation")
    theme = relationship("Theme", back_populates="presentation")
    music = relationship("Music", back_populates="presentation")
    presentation_logo = relationship("PresentationLogo", back_populates="presentation")
    slide = relationship("Slide", back_populates="presentation")


class Slide(db):
    __tablename__ = "slide"
    __table_args__ = {'schema': 'presentation'}
    id = Column(Integer, primary_key=True)
    color_text = Column(VARCHAR(255))
    priority = Column(Integer)
    id_presentation = Column(Integer, ForeignKey("presentation.presentation.id"))
    id_slide_type = Column(Integer, ForeignKey("presentation.slide_type.id"))

    presentation = relationship("Presentation", back_populates="slide")
    slide_type = relationship("SlideType", back_populates="slide")


db.metadata.create_all(engine)

session = Sess(engine, future=True)
statement = select(Session.date_start)
result = session.execute(statement).all()
for i in result:
    print(i)


