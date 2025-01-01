from datetime import datetime, UTC, timedelta
from typing import Dict, List
import streamlit as st
from sqlalchemy.orm.exc import NoResultFound
import os
from sqlalchemy import ARRAY, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import pandas as pd


# 声明基础类
Base = declarative_base()


# 定义用户模型
class User(Base):
    __tablename__ = "exam_users"
    id = Column(Integer, primary_key=True)
    user_code = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    notes = Column(String)


class CheckinRecord(Base):
    __tablename__ = "checkin_records"
    id = Column(Integer, primary_key=True)
    user_code = Column(String, nullable=False)
    category = Column(String, nullable=False)
    keywords = Column(ARRAY(String))
    difficulty = Column(String)
    degree = Column(String)
    question_id = Column(String, nullable=False)
    submitted_at = Column(DateTime, nullable=False)


class ExamRecord(Base):
    __tablename__ = "exam_records"
    id = Column(Integer, primary_key=True)
    user_code = Column(String, nullable=False)
    category = Column(String, nullable=False)
    keywords = Column(ARRAY(String))
    difficulty = Column(String)
    question_id = Column(String, nullable=False)
    user_answer = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    submitted_at = Column(DateTime, nullable=False)


@st.cache_resource
def get_conn():
    from sqlalchemy import create_engine

    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    Session = sessionmaker(bind=engine)
    return Session


from contextlib import contextmanager


@contextmanager
def get_db_session():
    conn = get_conn()
    session = conn()  # 新建会话
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_by_usercode(session, user_code: str):
    try:
        user = (
            session.query(User).filter(User.user_code == user_code).one()
        )  # 查询单个结果
        return user
    except NoResultFound:
        return None  # 没有找到用户


def add_exam_record(
    question_id: str,
    category: str,
    user_code: str,
    user_answer: str,
    correct_answer: str,
    difficulty: str,
    keywords: List[str],
):
    with get_db_session() as session:
        record = ExamRecord(
            user_code=user_code,
            category=category,
            difficulty=difficulty,
            keywords=keywords,
            question_id=question_id,
            user_answer=user_answer,
            correct_answer=correct_answer,
            is_correct=user_answer == correct_answer,
            submitted_at=datetime.now(UTC),
        )
        session.add(record)
        session.flush()
        sql = """UPDATE public.checkin_records
        SET degree = '模糊'
        WHERE keywords && :keywords 
        and user_code = :user_code 
        and category = :category
        and submitted_at >= NOW() - INTERVAL '30 day'"""
        session.execute(
            text(sql),
            {"keywords": keywords, "user_code": user_code, "category": category},
        )


def add_checkin_record(
    question_id: str,
    category: str,
    user_code: str,
    difficulty: str,
    degree: str,
    keywords: List[str],
):
    with get_db_session() as session:
        record = CheckinRecord(
            user_code=user_code,
            category=category,
            difficulty=difficulty,
            keywords=keywords,
            degree=degree,
            question_id=question_id,
            submitted_at=datetime.now(UTC),
        )
        session.add(record)
        session.flush()


def get_checkin_degree_24h(user_code: str) -> Dict[str, str]:
    """获取用户最近 24 小时内的打卡签到记录"""
    with get_db_session() as session:
        query = text(
            """
            SELECT
                question_id,
                MAX(degree) AS degree
            FROM public.checkin_records
            WHERE user_code = :user_code
                AND submitted_at >= :start_time
            GROUP BY question_id
            ORDER BY question_id
            """
        )
        result = session.execute(
            query,
            {
                "user_code": user_code,
                "start_time": datetime.now(UTC) - timedelta(days=1),
            },
        ).fetchall()
        return {row.question_id: row.degree for row in result}


def get_exam_statistics_by_time_range(
    user_code: str, start_time: datetime, end_time: datetime
) -> Dict[str, int]:
    with get_db_session() as session:
        query = text(
            """
            SELECT
                COUNT(*) AS total_answers,
                COUNT(*) FILTER (WHERE is_correct) AS correct_answers,
                COUNT(*) FILTER (WHERE NOT is_correct) AS incorrect_answers,
                COALESCE(
                    ROUND(
                        (SUM(CASE WHEN is_correct THEN 1 ELSE 0 END)::DECIMAL / NULLIF(COUNT(*), 0)) * 100,
                        2
                    ),  0
                ) AS accuracy_rate
            FROM public.exam_records
            WHERE submitted_at >= :start_time
                AND submitted_at <= :end_time
                AND user_code = :user_code
        """
        )
        result = session.execute(
            query,
            {"start_time": start_time, "end_time": end_time, "user_code": user_code},
        ).fetchone()
        return {
            "total_answers": result.total_answers,
            "correct_answers": result.correct_answers,
            "incorrect_answers": result.incorrect_answers,
            "accuracy_rate": result.accuracy_rate,
        }


def get_exam_statistics_today(
    user_code: str,
) -> Dict[str, int]:
    """invoke get_exam_statistics_by_time_range"""
    return get_exam_statistics_by_time_range(
        user_code,
        datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0),
        datetime.now(UTC),
    )


def get_exam_statistics_month(
    user_code: str,
) -> Dict[str, int]:
    """invoke get_exam_statistics_by_time_range"""
    return get_exam_statistics_by_time_range(
        user_code,
        datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        datetime.now(UTC),
    )


def get_answer_trend_statistics(user_code: str, category: str) -> pd.DataFrame:
    with get_db_session() as session:
        query = text(
            """
            SELECT user_code,
                category,
                date,
                daily_total_answers,
                daily_correct_answers,
                daily_incorrect_answers,
                daily_correct_rate
            FROM date_exam_statistics
            WHERE user_code = :user_code
                AND category = :category
                AND date >= DATE_TRUNC('month', CURRENT_DATE)
                AND date < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
            ORDER BY date ASC
            """
        )

        # 打印查询 SQL 语句
        # print(query.compile(compile_kwargs={"literal_binds": True}))

        result = session.execute(
            query, {"user_code": user_code, "category": category}
        ).fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "user_code",
                "category",
                "date",
                "daily_total_answers",
                "daily_correct_answers",
                "daily_incorrect_answers",
                "daily_correct_rate",
            ],
        )
        return df


def get_answer_keywords(
    user_code: str, category: str, is_correct: bool, start_time, end_time
) -> pd.DataFrame:
    with get_db_session() as session:
        query = text(
            """
            SELECT 
                user_code,
                category,
                array_to_string(keywords, ' ') AS combined_keywords  
            FROM 
                public.exam_records
            WHERE 
                user_code = :user_code
                AND category = :category
                AND is_correct = :is_correct
                AND submitted_at >= :start_time
                AND submitted_at <= :end_time
            """
        )

        # 打印查询 SQL 语句
        # print(query.compile(compile_kwargs={"literal_binds": True}))

        result = session.execute(
            query,
            {
                "user_code": user_code,
                "category": category,
                "is_correct": is_correct,
                "start_time": start_time,
                "end_time": end_time,
            },
        ).fetchall()

        # 组合成字符串返回
        return " ".join([f"{row.combined_keywords}" for row in result])


def get_answer_keywords_today(user_code: str, category: str, is_correct: bool) -> str:
    """invoke get_answer_keywords"""
    return get_answer_keywords(
        user_code,
        category,
        is_correct,
        datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0),
        datetime.now(UTC),
    )


def get_answer_keywords_month(user_code: str, category: str, is_correct: bool) -> str:
    """invoke get_answer_keywords"""
    return get_answer_keywords(
        user_code,
        category,
        is_correct,
        datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        datetime.now(UTC),
    )


def get_checkin_keywords(
    user_code: str, category: str, degree:str,start_time, end_time
) -> pd.DataFrame:
    with get_db_session() as session:
        query = text(
            """
            SELECT 
                user_code,
                category,
                array_to_string(keywords, ' ') AS combined_keywords  
            FROM 
                public.checkin_records
            WHERE 
                user_code = :user_code
                AND category = :category
                AND degree = :degree
                AND submitted_at >= :start_time
                AND submitted_at <= :end_time
            """
        )

        # print(query.compile(compile_kwargs={"literal_binds": True}))

        result = session.execute(
            query,
            {
                "user_code": user_code,
                "category": category,
                "degree": degree,
                "start_time": start_time,
                "end_time": end_time,
            },
        ).fetchall()

        # 组合成字符串返回
        return " ".join([f"{row.combined_keywords}" for row in result])


def get_checkin_keywords_today(user_code: str, category: str, degree: str) -> str:
    """invoke get_checkin_keywords"""
    return get_checkin_keywords(
        user_code,
        category,
        degree,
        datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0),
        datetime.now(UTC),
    )


def get_checkin_keywords_month(user_code: str, category: str, degree: str) -> str:
    """invoke get_checkin_keywords"""
    return get_checkin_keywords(
        user_code,
        category,
        degree,
        datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        datetime.now(UTC),
    )


def get_checkin_ignore_ids(user_code: str, category: str) -> List[str]:
    """查询24小时 degree = 略懂和 7天内 degree=精通 的记录ID"""
    with get_db_session() as session:
        query = text(
            """
            SELECT question_id
            FROM public.checkin_records
            WHERE 
                (
                    (degree = '略懂' AND submitted_at >= NOW() - INTERVAL '1 day')
                    OR 
                    (degree = '精通' AND submitted_at >= NOW() - INTERVAL '7 days')
                )
                AND category = :category
                AND user_code = :user_code
            """
        )
        result = session.execute(
            query,
            {
                "user_code": user_code,
                "category": category,
            },
        ).fetchall()
        return [row.question_id for row in result]


def get_exam_ignore_ids(user_code: str, category: str) -> List[str]:
    """查询忽略的问题"""
    with get_db_session() as session:
        query = text(
            """
            WITH recent_correct AS (
                SELECT DISTINCT question_id
                FROM public.exam_records
                WHERE is_correct = true
                AND submitted_at >= NOW() - INTERVAL '1 day'
                AND category = :category  
                AND user_code = :user_code  
            ),
            correct_7days AS (
                SELECT question_id
                FROM public.exam_records
                WHERE is_correct = true
                AND submitted_at >= NOW() - INTERVAL '7 days'
                AND category = :category  
                AND user_code = :user_code 
                GROUP BY question_id
                HAVING COUNT(*) >= 2  
            ),
            correct_30days AS (
                SELECT question_id
                FROM public.exam_records
                WHERE is_correct = true
                AND submitted_at >= NOW() - INTERVAL '30 days'
                AND category = :category  
                AND user_code = :user_code  
                GROUP BY question_id
                HAVING COUNT(*) >= 5  
            )
            SELECT question_id
            FROM recent_correct
            UNION
            SELECT question_id
            FROM correct_7days
            UNION
            SELECT question_id
            FROM correct_30days
            """
        )
        result = session.execute(
            query,
            {
                "user_code": user_code,
                "category": category,
            },
        ).fetchall()
        return [row.question_id for row in result]
