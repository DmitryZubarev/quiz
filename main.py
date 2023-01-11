from sqlalchemy.orm import registry
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import text
from fastapi import FastAPI, HTTPException
import pandas as pd

engine = create_engine("postgresql://postgres:1354228@localhost/quiz")
mapper_registry = registry()

session_table = Table(
    "session",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

app = FastAPI()


@app.get("/session/{session_id}")
def method(session_id, threshold=50):
    query = text("""with questions as
            (select count(*) over (partition by question.id) max_points, promt.id as prompt_id, match.id as match_id, question.id as id, option.id as option_id, option.correct as option_correct, binary_true.id as binary_true_id from question.question question
            left join question.option on question.option.id_question = question.id
            left join question.promt on question.promt.id_question = question.id
            left join question.binary_true on question.binary_true.id_question = question.id
            left join question.match on question.promt.id = question.match.id_promt),
            answers_inter as
        (select a.id, a.id_session_user, a.id_session, a.id_question, q.max_points, count(case
            when option_id is not null then
                nullif(option_correct = (session.selected_option.id is not null), false)
            when prompt_id is not null then
                nullif(session.selected_match.id_match = match_id, false)
            else
                nullif((binary_true_id is null) = (session.selected_binary_true.id is null), false)
            end) points from questions q join session.answer a on a.id_question = q.id
        left join session.selected_option on option_id = selected_option.id_option and a.id = selected_option.id_answer
        left join session.selected_match on prompt_id = selected_match.id_promt and a.id = selected_match.id_answer
        left join session.selected_binary_true on selected_binary_true.id_answer = a.id
        group by a.id, q.max_points),
        answers as (select (min_score + (max_score - min_score) * points / max_points) as score, (points = max_points) as correct, * from answers_inter inner join question.question on answers_inter.id_question = question.id)
        select  
            count(nullif(sum_score > :threshold / 100 * max_score, false)) as passed_threshold, count(*) participants, sum(correct_answers) as correct_answers,
            sum(wrong_answers) as wrong_answers, sum(sum_score) as sum_score, sum(max_score) as max_score, sum(min_score) as min_score,
            avg(sum_score) as avg_score
        from (select
            count(nullif(max_points = points, false)) correct_answers,
            count(nullif(max_points = points, true)) wrong_answers,
            sum(score) as sum_score,
            sum(max_score) as max_score,
            sum(min_score) as min_score
        from answers a where id_session = :session_id group by id_session_user) stat_inter;""")
    with engine.connect() as con:
        result = con.execute(query, session_id=session_id, threshold=threshold)
        return result.first()


@app.get("/session/{session_id}/question_times")
def avg_time(session_id):
    query = text(
        """select AVG(answer.response_time) average_time, id_question question from session.answer join question.question on answer.id_question = question.id where id_session = :session_id group by answer.id_question;""")
    with engine.connect() as con:
        result = con.execute(query, session_id=session_id)
        return result.fetchall()


@app.get("/group/{group_id}/quiz_participation/{session_id}")
def method(group_id, session_id):
    query = text(
        """select s_user.id_session as session, count(nullif(s_user.id_session IS NULL, false)) participated, count(nullif(s_user.id_session IS NULL, true)) ignored from account.user_group_email account left join session."session_user" s_user on s_user.email = account.email where account.id_user_group = :group_id and s_user.id_session = :session_id group by s_user.id_session;""")
    with engine.connect() as con:
        result = con.execute(query, group_id=group_id, session_id=session_id)
        a = result.first()
        if a == None:
            raise HTTPException(status_code=404, detail="Not found")
        return a


def participants_score(session_id):
    query = text("""with questions as
        (select count(*) over (partition by question.id) max_points, promt.id as prompt_id, match.id as match_id, question.id as id, option.id as option_id, option.correct as option_correct, binary_true.id as binary_true_id from question.question question
        left join question.option on question.option.id_question = question.id
        left join question.promt on question.promt.id_question = question.id
        left join question.binary_true on question.binary_true.id_question = question.id
        left join question.match on question.promt.id = question.match.id_promt),
        answers_inter as
    (select a.id, a.id_session_user, a.id_session, a.id_question, q.max_points, count(case
        when option_id is not null then
            nullif(option_correct = (session.selected_option.id is not null), false)
        when prompt_id is not null then
            nullif(session.selected_match.id_match = match_id, false)
        else
            nullif((binary_true_id is null) = (session.selected_binary_true.id is null), false)
        end) points from questions q join session.answer a on a.id_question = q.id
    left join session.selected_option on option_id = selected_option.id_option and a.id = selected_option.id_answer
    left join session.selected_match on prompt_id = selected_match.id_promt and a.id = selected_match.id_answer
    left join session.selected_binary_true on selected_binary_true.id_answer = a.id
    group by a.id, q.max_points),
    answers as (select (min_score + (max_score - min_score) * points / max_points) as score, (points = max_points) as correct, * from answers_inter inner join question.question on answers_inter.id_question = question.id)
    select
        email,
        count(nullif(max_points = points, false)) correct_answers,
        count(nullif(max_points = points, true)) wrong_answers,
        sum(score) as sum_score
    from answers a join session."session_user" on id_session_user = "session_user".id where a.id_session = :session_id group by email;""")

    with engine.connect() as con:
        result = con.execute(query, session_id=session_id)
        res = result.fetchall()
        return res


@app.get("/session/{session_id}/participants_score")
def method(session_id):
    res = participants_score(session_id)
    if res == None:
        raise HTTPException(status_code=404, detail="Not found")
    return res


@app.get("/session/{session_id}/participants_score/csv")
def method(session_id):
    import time

    res = participants_score(session_id)
    df = pd.DataFrame.from_records(res, columns=['email', 'correct_answers', 'wrong_answers', 'sum_score'])

    name = session_id + "_participants_score_" + str(int(time.time())) + ".csv"

    df.to_csv("docs/" + name)

    return {
        "file_name": name
    }

