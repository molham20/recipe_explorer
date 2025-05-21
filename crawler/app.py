import streamlit as st
import backend
import os
from PIL import Image
import requests
from io import BytesIO

# إعداد الصفحة
st.set_page_config(
    page_title="🍲 مستكشف الوصفات",
    page_icon="🍳",
    layout="wide"
)

# تحسينات التصميم
st.markdown("""
<style>
.st-emotion-cache-1y4p8pa {padding: 2rem 1rem;}
.recipe-card {border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);}
.st-emotion-cache-1v0mbdj img {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# الواجهة الرئيسية
def main():
    st.title("🍲 مستكشف الوصفات الغذائية")
    st.markdown("---")
    
    # قسم إضافة وصفات جديدة
    with st.expander("➕ إضافة وصفات جديدة", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_url = st.text_input("أدخل رابط الوصفة:")
        with col2:
            if st.button("استخراج الوصفة"):
                if new_url:
                    with st.spinner("جاري استخراج الوصفة..."):
                        recipe = backend.scrape_recipe(new_url)
                        if recipe:
                            st.success(f"تم استخراج وصفة: {recipe['title']}")
                            st.rerun()
                        else:
                            st.error("حدث خطأ أثناء استخراج الوصفة")
                else:
                    st.warning("يجب إدخال رابط الوصفة أولاً")
    
    # قسم عرض الوصفات
    st.header("📚 الوصفات المحفوظة")
    recipes = backend.get_saved_recipes()
    
    if not recipes:
        st.warning("لا توجد وصفات مخزنة بعد. أضف وصفات جديدة باستخدام الحقل أعلاه.")
    else:
        for recipe in recipes:
            with st.container():
                st.markdown(f"<div class='recipe-card'>", unsafe_allow_html=True)
                
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    if recipe.get('image'):
                        try:
                            response = requests.get(recipe['image'], timeout=5)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, width=250)
                        except:
                            st.image("https://via.placeholder.com/250x150?text=No+Image", width=250)
                
                with col_info:
                    st.subheader(recipe['title'])
                    st.caption(f"⏱️ وقت التحضير: {recipe.get('prep_time', 'غير معروف')} | 🍳 وقت الطهي: {recipe.get('cook_time', 'غير معروف')}")
                    
                    with st.expander("المكونات"):
                        for ing in recipe['ingredients']:
                            st.markdown(f"- {ing}")
                    
                    with st.expander("طريقة التحضير"):
                        for i, step in enumerate(recipe['instructions'], 1):
                            st.markdown(f"{i}. {step}")
                    
                    st.markdown(f"[رابط الوصفة الأصلي]({recipe['url']})")
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")

if __name__ == "__main__":
    main()