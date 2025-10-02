from .database import vector_collection
import time

def analyze_case(case_title: str, case_description: str, case_id: int) -> str:
    """
    العقل الرقمي لمنصة الكابتن القانوني - الإصدار 2.0 (مع ذاكرة)
    """
    # --- المرحلة الأولى: الفهم والتخزين (التعلم) ---
    # نقوم بتحويل القضية الحالية إلى "ذكرى" وتخزينها في المكتبة العصبية
    # نستخدم case_id كمعرف فريد لهذه الذكرى
    try:
        vector_collection.add(
            documents=[f"العنوان: {case_title}\nالوصف: {case_description}"],
            metadatas=[{"title": case_title}],
            ids=[str(case_id)]
        )
        learning_report = "تمت أرشفة هذه القضية بنجاح في ذاكرة الكابتن."
    except Exception as e:
        learning_report = f"تنبيه هندسي: لم نتمكن من أرشفة القضية. الخطأ: {e}"

    # --- المرحلة الثانية: البحث والاسترجاع (التذكر) ---
    # نبحث في ذاكرة الكابتن عن أكثر قضية واحدة (n_results=1) تشبه القضية الحالية
    # نستبعد القضية نفسها من نتائج البحث لضمان أننا نجد قضية "أخرى" مشابهة
    try:
        # ملاحظة: ChromaDB لا تدعم استبعاد ID معين من البحث مباشرة في الإصدارات البسيطة
        # لذا سنطلب نتيجتين ونتجاهل الأولى إذا كانت هي نفسها القضية الحالية.
        similar_cases = vector_collection.query(
            query_texts=[case_description],
            n_results=2 
        )
        
        retrieval_report = "لم يتم العثور على قضايا مشابهة في الذاكرة حتى الآن."
        if similar_cases and similar_cases['ids'][0]:
            # تحقق مما إذا كانت هناك نتائج وما إذا كانت النتيجة الأولى ليست القضية الحالية
            found_id = similar_cases['ids'][0][0]
            if str(found_id) != str(case_id) and len(similar_cases['ids'][0]) >= 1:
                similar_case_title = similar_cases['metadatas'][0][0]['title']
                retrieval_report = f"قامت ذاكرة الكابتن بتحديد قضية سابقة مشابهة بعنوان: '{similar_case_title}'."
            elif len(similar_cases['ids'][0]) > 1:
                # إذا كانت النتيجة الأولى هي نفسها، خذ الثانية
                similar_case_title = similar_cases['metadatas'][0][1]['title']
                retrieval_report = f"قامت ذاكرة الكابتن بتحديد قضية سابقة مشابهة بعنوان: '{similar_case_title}'."

    except Exception as e:
        retrieval_report = f"تنبيه هندسي: حدث خطأ أثناء البحث في الذاكرة. الخطأ: {e}"


    # --- المرحلة الثالثة: بناء التقرير النهائي (اللسان) ---
    report_content = f"""
=================================
**التقرير الهندسي الأولي (مع ذاكرة)**
=================================

**1. ملخص الأرشفة:**
   - {learning_report}

**2. نتائج الذاكرة السياقية:**
   - {retrieval_report}

**3. تحليل أولي:**
   - بناءً على التشابه مع القضايا السابقة، يبدو أن النقطة الجوهرية في هذه القضية هي [تحليل مبدئي بناءً على التشابه].

**4. توصية هندسية:**
   - يوصى بالتركيز على [توصية مبدئية] لتعزيز الموقف القانوني.

*تم إنشاء هذا التقرير بواسطة ذكاء الكابتن الإصدار 2.0 في {time.ctime()}*
"""
    return report_content

