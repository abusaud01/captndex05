# اسم الملف: app/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# --------------------------------------------------------------------------
# هذه النماذج لا تتحدث مع قاعدة البيانات مباشرة.
# وظيفتها هي تحديد شكل البيانات التي يتم تبادلها عبر الـ API.
# --------------------------------------------------------------------------

# --- نماذج التقارير ---

# النموذج الأساسي للتقرير
class ReportBase(BaseModel):
    report_content: str

# نموذج لإنشاء تقرير جديد
class ReportCreate(ReportBase):
    pass

# نموذج لعرض التقرير (مع البيانات التي تأتي من قاعدة البيانات)
class Report(ReportBase):
    id: int
    case_id: int

    # هذا السطر السحري يخبر Pydantic بقراءة البيانات من كائنات SQLAlchemy
    class Config:
        from_attributes = True

# --- نماذج القضايا ---

class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CaseCreate(CaseBase):
    pass

class Case(CaseBase):
    id: int
    owner_id: int
    # القضية قد تحتوي على تقرير أو لا (اختياري)
    report: Optional[Report] = None

    class Config:
        from_attributes = True

# --- نماذج المستخدمين ---

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str # كلمة المرور مطلوبة عند الإنشاء فقط

class User(UserBase):
    id: int
    # القيمة الافتراضية للمستخدم هي أنه نشط
    is_active: bool = True 
    # المستخدم قد يملك قائمة من القضايا
    cases: List[Case] = []

    class Config:
        from_attributes = True
