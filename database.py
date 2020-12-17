from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    UnicodeText,
    String,
    ForeignKey,
    UniqueConstraint,
    func,
    create_engine,
)
import threading
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = "sqlite:///college.db"


def start() -> scoped_session:
    engine = create_engine(DB_URI, encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()


class Students(BASE):
    __tablename__ = "Students"
    roll_num = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText)
    
    def __init__(self, roll_num, name):
        self.roll_num = roll_num
        self.name = name

    def __repr__(self):
        return f"<Student {self.roll_num} {self.name}>"

class Course(BASE):
    __tablename__ = "Course"
    code = Column(UnicodeText(5), primary_key=True, nullable=False)
    name = Column(UnicodeText)
    
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return f"<course {self.code} {self.name}>"

class Attendance(BASE):
    __tablename__ = "Attendance"
    date = Column(UnicodeText(10), primary_key=True, nullable=False)
    course = Column(UnicodeText(5),ForeignKey('Course.code'),primary_key = True,nullable=False)
    slot = Column(Integer,primary_key=True,nullable=False)
    student_id = Column(Integer,ForeignKey('Students.roll_num'),primary_key=True,nullable=False)
    present = Column(Integer,default=0)
    
    def __init__(self, date, course,slot,student_id,present):
        self.date = date
        self.course = course
        self.slot = slot
        self.student_id = student_id
        self.present = present

    def __repr__(self):
        return f"<attendance {self.date} {self.course} {self.slot} {self.student_id} {self.present}>"



Students.__table__.create(checkfirst=True)
Attendance.__table__.create(checkfirst=True)
Course.__table__.create(checkfirst=True)


INSERTION_LOCK = threading.RLock()

def get_all_students():
    return SESSION.query(Students)

def get_all_courses():
    return SESSION.query(Course)

def get_all_attendance():
    return SESSION.query(Attendance)


def add_attendance(student_id: int , date: str, course: str, slot: int):
    obj = SESSION.query(Attendance).filter(Attendance.date==date,Attendance.course==course,Attendance.slot==slot,Attendance.student_id==student_id).first()
    
    # checking if such entry already exists
    if obj == None:
        # new entry

        obj = Attendance(date=date,course=course,slot=slot,student_id=student_id,present=1)

        with INSERTION_LOCK:
            SESSION.add(obj)
            SESSION.flush()
            SESSION.commit()

    else:
        # update
        obj.present+=1
        SESSION.flush()
        SESSION.commit()


def get_student(roll_num: int):
    obj = SESSION.query(Students).filter(Students.roll_num==roll_num).first()

    return {"Roll_num":roll_num,"Name":obj.name}