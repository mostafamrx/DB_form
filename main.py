import streamlit as st
import requests
from datetime import datetime

# ضع الرابط الطويل الخاص بـ Apps Script هنا
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxme5zlHHabXtHxMVnM5_9-zj1PUC4qoAj48acu_sie8PweuKDgjLLGRPUvW6-JfW6G/exec"

# 1. إعدادات الصفحة
st.set_page_config(page_title="تسجيل العملاء المحتملين", page_icon="📝", layout="centered")

# 2. كود CSS المطور للتحكم الكامل في حجم واتجاه الخطوط
st.markdown("""
<style>
    /* تحويل الاتجاه العام لليمين */
    * {
        direction: rtl;
        text-align: right;
    }
    /* ضبط محاذاة النصوص داخل الحقول */
    .stTextInput>div>div>input {
        text-align: right;
    }
    .stTextArea>div>div>textarea {
        text-align: right;
    }
    /* تحسين شكل زر الحفظ */
    .stButton>button {
        float: left;
    }
    /* محاذاة الأعمدة العلوية في المنتصف تماماً عمودياً */
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    
    /* تنسيق العنوان الضخم الجديد ليكون ممتداً وواضحاً */
    .custom-main-title {
        font-size: 45px !important; /* يمكنك تكبيرها إلى 50px أو 55px إذا أردتها أضخم */
        font-weight: 800 !important;
        color: white;
        line-height: 1.2;
        white-space: nowrap; /* يمنع النص من النزول لسطر جديد ليظل ممتداً بعرض المساحة */
    }
</style>
""", unsafe_allow_html=True)

# 3. عرض اللوجو والعنوان بتنسيق HTML المباشر
col1, col2 = st.columns([1, 3])
with col1:
    try:
        st.image("logo.png", width=220) 
    except FileNotFoundError:
        st.warning("صورة اللوجو غير موجودة")
with col2:
    # هنا استخدمنا وسم HTML مباشر لتطبيق التنسيق الضخم الجديد بدلاً من st.header
    st.markdown('<h1 class="custom-main-title">منصة إدخال بيانات العملاء</h1>', unsafe_allow_html=True) 

st.markdown("سيتم حفظ هذه البيانات تلقائياً في قاعدة البيانات المركزية")
st.markdown("---")
# 4. بيانات المندوب (خارج النموذج)
registered_by = st.text_input("اسم المستخدم  *", placeholder="اكتب اسمك هنا...")

st.markdown("---")

# 5. واجهة إدخال بيانات العميل (Form المطور)
with st.form("customer_form", clear_on_submit=True):
    st.subheader("البيانات الأساسية للعميل")
    
    full_name = st.text_input("الاسم الكامل للعميل *")
    phone_number = st.text_input("رقم هاتف العميل (11 رقم) *", placeholder="مثال: 01xxxxxxxxx")
    city = st.text_input("المدينة *", placeholder="مثال: القاهرة، الجيزة...")
    location_area = st.text_input("المنطقة / الحي")
    notes = st.text_area("ملاحظات إضافية")
    
    # زر الإرسال
    submitted = st.form_submit_button("💾 حفظ بيانات العميل")

    # 6. معالجة البيانات والتحقق من الشروط عند الإرسال
    if submitted:
        # أ) التحقق من الحقول الإجبارية
        if not registered_by or not full_name or not phone_number or not city:
            st.error("⚠️ يرجى ملء جميع الحقول الإجبارية (*)اسم المستخدم، اسم العميل، رقم الهاتف، والمدينة!")
        
        # ب) التحقق من رقم الهاتف (أن يكون أرقام فقط وطوله بالضبط 11)
        elif not phone_number.isdigit() or len(phone_number) != 11:
            st.error("⚠️ خطأ في رقم الهاتف! يجب أن يتكون من 11 رقماً فقط، ولا يحتوي على أي أحرف أو رموز أو مسافات.")
            
        else:
            # جلب التاريخ والوقت الحالي تلقائياً بتنسيق واضح
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # تجهيز البيانات للإرسال
            payload = {
                "date": current_date,          # التاريخ التلقائي
                "registered_by": registered_by,
                "full_name": full_name,
                "phone_number": phone_number,
                "city": city,                  # الحقل الجديد
                "location_area": location_area,
                "notes": notes
            }
            
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                
                if response.status_code == 200:
                    st.success(f"✅ تم حفظ بيانات العميل: {full_name} بنجاح بتاريخ {current_date}")
                else:
                    st.error("❌ حدث خطأ في الاتصال بالشيت.")
            except Exception as e:
                st.error(f"❌ حدث خطأ: {e}")