import io

import pandas as pd

from src.models import Column, Course, Group, Lesson

LECTURE = "שיעור"
EXERCISE = "תרגיל"

DAY_OF_WEEK_MAP = {"א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6}


async def list_courses() -> list[Course]:
    return await Course.find_all().to_list()


async def delete_courses() -> None:
    await Course.delete_all()


async def upload_courses(data: bytes):
    df = _read_excel(io.BytesIO(data))
    courses = [
        _create_courses(course)
        for _, course in df.groupby([Column.Semester, Column.Subject])
    ]

    await _save_courses(courses)


def _read_excel(bytes_io: io.BytesIO) -> pd.DataFrame:
    courses_df = pd.read_excel(bytes_io)

    courses_df[Column.GroupDescription] = courses_df[Column.GroupDescription].fillna("")
    courses_df[Column.Lecturer] = courses_df[Column.Lecturer].fillna("")
    courses_df[Column.Day] = courses_df[Column.Day].apply(DAY_OF_WEEK_MAP.get)
    courses_df[Column.Classroom] = courses_df[Column.Classroom].fillna("")
    courses_df[Column.Credits] = courses_df[Column.Credits].fillna(0)
    # TODO check why there are NaNs

    courses_df = courses_df.drop_duplicates(
        subset=[
            Column.Semester,
            Column.Group,
            Column.Day,
            Column.StartTime,
            Column.EndTime,
        ],
        keep="first",
    ).reset_index(drop=True)

    return courses_df


def _create_courses(course_df: pd.DataFrame) -> Course:
    lectures = course_df[course_df[Column.LessonTypeDesc] == LECTURE]
    exercises = course_df[course_df[Column.LessonTypeDesc] == EXERCISE]

    course = Course.from_row(course_df.iloc[0])
    course.lectures = [
        _create_group(group) for _, group in lectures.groupby(Column.Group)
    ]
    course.exercises = [
        _create_group(group) for _, group in exercises.groupby(Column.Group)
    ]

    return course


def _create_group(group_df: pd.DataFrame) -> Group:
    group = Group.from_row(group_df.iloc[0])
    group.lessons = [Lesson.from_row(row) for _, row in group_df.iterrows()]

    return group


async def _save_courses(courses: list[Course]) -> None:
    await Course.delete_all()

    for course in courses:
        await course.save()
