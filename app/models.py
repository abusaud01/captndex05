# اسم الملف: app/models.py

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

# --------------------------------------------------------------------------
# نستورد "الفئة الأم" (Base) من ملفنا الأساسي.
# هذا هو السلك الذي يربط مخططاتنا بمحطة الطاقة.
# --------------------------------------------------------------------------
from .database import Base

# --------------------------------------------------------------------------
# المخطط الهندسي لجدول "المستخدمين"
# --------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # هذا يربط المستخدم بقضاياه (علاقة واحد إلى متعدد)
    cases = relationship("Case", back_populates="owner")

# --------------------------------------------------------------------------
# المخطط الهندسي لجدول "القضايا"
# --------------------------------------------------------------------------
class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # هذا يربط القضية بمالكها
    owner = relationship("User", back_populates="cases")
    # هذا يربط القضية بتقريرها (علاقة واحد إلى واحد)
    report = relationship("Report", back_populates="case", uselist=False)

# --------------------------------------------------------------------------
# المخطط الهندسي لجدول "التقارير"
# --------------------------------------------------------------------------
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_content = Column(Text)
    case_id = Column(Integer, ForeignKey("cases.id"))

    # هذا يربط التقرير بالقضية التابع لها
    case = relationship("Case", back_populates="report")
