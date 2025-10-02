# اسم الملف: app/crud.py

from sqlalchemy.orm import Session

# --------------------------------------------------------------------------
# نستورد المخططات الهندسية (models) وعقود البيانات (schemas)
# النقطة تعني "من نفس الحزمة (app)"
# --------------------------------------------------------------------------
from . import models, schemas

# --------------------------------------------------------------------------
# --- عمليات المستخدمين (User CRUD) ---
# --------------------------------------------------------------------------

def get_user(db: Session, user_id: int):
    """قراءة مستخدم واحد عن طريق الـ ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """قراءة مستخدم واحد عن طريق البريد الإلكتروني."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """قراءة قائمة من المستخدمين مع إمكانية التخطي والتحديد."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """إنشاء مستخدم جديد."""
    # ملاحظة: في تطبيق حقيقي، يجب تشفير كلمة المرور هنا.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        full_name=user.full_name, 
        email=user.email, 
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------------------------------------------------------------------------
# --- عمليات القضايا (Case CRUD) ---
# --------------------------------------------------------------------------

def get_cases(db: Session, skip: int = 0, limit: int = 100):
    """قراءة قائمة من القضايا."""
    return db.query(models.Case).offset(skip).limit(limit).all()

def create_user_case(db: Session, case: schemas.CaseCreate, user_id: int):
    """إنشاء قضية جديدة وربطها بمالك (مستخدم)."""
    db_case = models.Case(**case.model_dump(), owner_id=user_id)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

# --------------------------------------------------------------------------
# --- عمليات التقارير (Report CRUD) ---
# --------------------------------------------------------------------------

def create_case_report(db: Session, report_data: schemas.ReportCreate, case_id: int):
    """إنشاء تقرير جديد وربطه بقضية."""
    db_report = models.Report(**report_data.model_dump(), case_id=case_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_report_by_case_id(db: Session, case_id: int):
    """قراءة تقرير مرتبط بقضية معينة."""
    return db.query(models.Report).filter(models.Report.case_id == case_id).first()
