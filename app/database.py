# الملف: app/database.py (الإصدار النهائي والمحصّن)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import chromadb

# --- 1. إعداد قاعدة البيانات العلائقية (SQL) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. إعداد قاعدة البيانات المتجهة (Vector DB) - النسخة المحصّنة ---
# هذا هو "العقل الدائم" لذاكرة الكابتن.
# باستخدام PersistentClient، نضمن أن البيانات تُحفظ على القرص في مجلد "chroma_db"
client = chromadb.PersistentClient(path="./chroma_db")

# نستخدم الآن الدالة الهندسية الصحيحة: get_or_create_collection
# هذه الدالة تضمن بشكل قاطع أن المجموعة موجودة دائمًا قبل أي عملية.
# إنها الحل الأمثل لمشكلة "Collection does not exist".
vector_collection = client.get_or_create_collection("legal_knowledge_base")

