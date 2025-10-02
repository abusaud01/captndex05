# اسم الملف: app/routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# --------------------------------------------------------------------------
# نستورد كل الأدوات التي سنحتاجها:
# - ورشة العمليات (crud)
# - عقود البيانات (schemas)
# - المخططات الهندسية (models)
# - العقل الرقمي (analysis_engine)
# - ومنشئ الجلسات (SessionLocal)
# --------------------------------------------------------------------------
from . import crud, schemas, models, analysis_engine
from .database import SessionLocal

# --------------------------------------------------------------------------
# هذه "التبعية" (Dependency) هي آلية هندسية رائعة.
# إنها تضمن أن كل مسار يحصل على جلسة قاعدة بيانات جديدة ومستقلة،
# ويتم إغلاقها بشكل آمن بعد انتهاء الطلب، مما يمنع تسرب الموارد.
# --------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------------------
# --- مسارات المستخدمين (User Endpoints) ---
# --------------------------------------------------------------------------
router_users = APIRouter(
    prefix="/users",
    tags=["Users"] # لتنظيم الواجهة التفاعلية (Swagger UI)
)

@router_users.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل مسبقاً")
    return crud.create_user(db=db, user=user)

@router_users.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return db_user

# --------------------------------------------------------------------------
# --- مسارات القضايا (Case Endpoints) ---
# --------------------------------------------------------------------------
router_cases = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)

@router_cases.post("/user/{user_id}", response_model=schemas.Case)
def create_case_for_user(user_id: int, case: schemas.CaseCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return crud.create_user_case(db=db, case=case, user_id=user_id)

# --------------------------------------------------------------------------
# --- مسار التحليل (Analysis Endpoint) ---
# --------------------------------------------------------------------------
router_analysis = APIRouter(
    prefix="/analysis",
    tags=["Analysis Engine"]
)

@router_analysis.post("/case/{case_id}", response_model=schemas.Report)
def analyze_case_and_create_report(case_id: int, db: Session = Depends(get_db)):
    db_case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="القضية غير موجودة")

    # لمنع إنشاء أكثر من تقرير لنفس القضية
    existing_report = crud.get_report_by_case_id(db, case_id=case_id)
    if existing_report:
        raise HTTPException(status_code=400, detail="تم إنشاء تقرير لهذه القضية مسبقاً")

    # استدعاء العقل الرقمي
    analysis_result = analysis_engine.get_ai_analysis(case_data=db_case)
    
    # حفظ نتيجة التحليل في قاعدة البيانات
    db_report = crud.create_case_report(db=db, report_data=analysis_result, case_id=case_id)
    
    return db_report
