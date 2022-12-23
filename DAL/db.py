import sqlalchemy as db
from classes import *


engine = db.create_engine("postgresql+psycopg2://postgres:Dc028ed7_@localhost/quiz")
mapper_registry = db.orm.registry()

# has only pk
session_table = db.Table(
    "session",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("date_start", db.TIMESTAMP),
    db.Column("date_end", db.TIMESTAMP)
)

question_table = db.Table(
    "question",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("content", db.Text),
    db.Column("duration", db.Interval),
    db.Column("response_rate", db.Boolean),
    db.Column("random_answers", db.Boolean),
    db.Column("min_score", db.Integer),
    db.Column("max_score", db.Integer)
)

presentation_logo_table = db.Table(
    "presentation_logo",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR(255)),
    db.Column("file", db.VARCHAR(500))
)

slide_type_table = db.Table(
    "slide_type",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR)
)

music_table = db.Table(
    "music",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR(500)),
    db.Column("file", db.VARCHAR(500))
)

theme_table = db.Table(
    "theme",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR(500)),
    db.Column("file", db.VARCHAR(500))
)

category_table = db.Table(
    "category",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR(500))
)

user_group_table = db.Table(
    "user_group",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR(500)),
    db.Column("code", db.VARCHAR(255))
)

role_table = db.Table(
    "role",
    mapper_registry.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.VARCHAR(255))
)

mapper_registry.map_imperatively(Session, session_table)
mapper_registry.map_imperatively(Question, question_table)
mapper_registry.map_imperatively(PresentationLogo, presentation_logo_table)
mapper_registry.map_imperatively(SlideType, slide_type_table)
mapper_registry.map_imperatively(Music, music_table)
mapper_registry.map_imperatively(Theme, theme_table)
mapper_registry.map_imperatively(Category, category_table)
mapper_registry.map_imperatively(UserGroup, user_group_table)
mapper_registry.map_imperatively(Role, role_table)
# has only pk


# has one to many

# has one to many

# has fk

# has fk

