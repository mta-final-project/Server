from enum import StrEnum


class Column(StrEnum):
    Group = "קבוצה"
    Subject = "תיאור נושא"
    GroupDescription = "מלל חופשי לתלמיד"
    LessonType = "סוג מקצוע"
    LessonTypeDesc = "תיאור סוג מקצוע"
    Semester = "סמסטר"
    Lecturer = "שם מרצה"
    Day = "יום בשבוע"
    StartTime = "שעת התחלה"
    EndTime = "שעת סיום"
    TotalHours = 'סה"כ שעות'
    Classroom = "תיאור כיתה"
    Credits = 'נ"ז'
    Department = "תיאור חוג"
