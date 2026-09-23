import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Sơ Đồ Lớp Học", layout="wide", page_icon="🏫")

MAT_KHAU_QUAN_TRI = "12A1HIEN"
NGAY_BAT_DAU = datetime(2026, 9, 23)
FILE_DATA = "danh_sach_lop.csv"
FILE_BG = "bg_url.txt"

if os.path.exists(FILE_BG):
    with open(FILE_BG, "r") as f:
        bg_url = f.read().strip()
else:
    bg_url = ""

if bg_url:
    st.markdown(f"""
    
    """, unsafe_allow_html=True)

def tao_du_lieu_mau():
    danh_sach = []
    id_hs = 1
    for day in range(1, 5):         
        for hang in range(1, 7):    
            for cho in [1, 2]:      
                if id_hs <= 45:
                    ten = f"Học sinh {id_hs}"
                    avt = f"https://api.dicebear.com/7.x/avataaars/svg?seed={id_hs}"
                else:
                    ten = "Ghế Trống"
                    avt = "https://ui-avatars.com/api/?name=Trong&background=f0f0f0&color=a0a0a0"
                danh_sach.append({
                    "Ten": ten, "Day_Doc": day, "Hang_Ngang": hang,
                    "Cho_Ngoi": cho, "Avatar_URL": avt
                })
                id_hs += 1
    return pd.DataFrame(danh_sach)

if os.path.exists(FILE_DATA):
    df = pd.read_csv(FILE_DATA)
else:
    df = tao_du_lieu_mau()
    df.to_csv(FILE_DATA, index=False)

hom_nay = datetime.now()
so_lan_doi = (hom_nay - NGAY_BAT_DAU).days // 14
df_hien_tai = df.copy()

if so_lan_doi > 0:
    df_hien_tai['Hang_Ngang'] = (df_hien_tai['Hang_Ngang'] + so_lan_doi - 1) % 6 + 1

st.title("🏫 SƠ ĐỒ LỚP HỌC (45 THÀNH VIÊN)")
st.caption(f"📅 Trạng thái: Đã tự động đổi chỗ **{so_lan_doi}** lần. (Hàng cuối lên bục giảng, các hàng khác lùi 1 bước)")
st.write("---")

tab_sodo, tab_quanly = st.tabs(["🗺️ Hiển thị Sơ đồ Lớp", "⚙️ Quản lý & Chỉnh sửa"])

with tab_sodo:
    st.markdown("", unsafe_allow_html=True)

def ve_cum_4_hoc_sinh(hs_day_a, hs_day_b, title):
        with st.container(border=True):
            st.subheader(title)
            c1, c2, gap, c3, c4 = st.columns([1, 1, 0.3, 1, 1])

        def get_hs(hs_list, cho):
            hs = next((x for x in hs_list if x['Cho_Ngoi'] == cho), None)
            if hs and hs['Ten'] != "Ghế Trống":
                return hs['Ten'], hs['Avatar_URL']
            return "Trống", "https://ui-avatars.com/api/?name=Trong&background=f0f0f0&color=a0a0a0"

        t1, a1 = get_hs(hs_day_a, 1)
        t2, a2 = get_hs(hs_day_a, 2)
        t3, a3 = get_hs(hs_day_b, 1)
        t4, a4 = get_hs(hs_day_b, 2)

        with c1:
            st.image(a1, use_container_width=True)
            st.caption(f"**{t1}**")
        with c2:
            st.image(a2, use_container_width=True)
            st.caption(f"**{t2}**")
        with c3:
            st.image(a3, use_container_width=True)
            st.caption(f"**{t3}**")
        with c4:
            st.image(a4, use_container_width=True)
            st.caption(f"**{t4}**")

for h in range(1, 7):
    col_trai, col_phai = st.columns(2)
    hs_hang = df_hien_tai[df_hien_tai['Hang_Ngang'] == h]
    
    with col_trai:
        hs_d1 = hs_hang[hs_hang['Day_Doc'] == 1].to_dict('records')
        hs_d2 = hs_hang[hs_hang['Day_Doc'] == 2].to_dict('records')
        ve_cum_4_hoc_sinh(hs_d1, hs_d2, f"HÀNG {h} - CỤM TRÁI")
        
    with col_phai:
        hs_d3 = hs_hang[hs_hang['Day_Doc'] == 3].to_dict('records')
        hs_d4 = hs_hang[hs_hang['Day_Doc'] == 4].to_dict('records')
        ve_cum_4_hoc_sinh(hs_d3, hs_d4, f"HÀNG {h} - CỤM PHẢI")
mk = st.text_input("🔑 Nhập mật khẩu quản trị:", type="password")

if mk == MAT_KHAU_QUAN_TRI:
    st.success("✅ Đã mở khóa chỉnh sửa!")
    
    st.subheader("🖼️ 1. Cài đặt Hình Nền Web")
    link_bg_moi = st.text_input("Dán link ảnh nền:", value=bg_url)
    if st.button("Lưu Hình Nền"):
        with open(FILE_BG, "w") as f:
            f.write(link_bg_moi)
        st.success("Đã lưu ảnh nền! Hãy bấm F5 để xem thay đổi.")
        
    st.write("---")
    st.subheader("👤 2. Chỉnh sửa Danh sách & Avatar Học sinh")
    df_moi = st.data_editor(
        df,
        column_config={
            "Ten": st.column_config.TextColumn("👤 Tên Học Sinh", width="medium"),
            "Day_Doc": st.column_config.NumberColumn("🏢 Dãy dọc (1-4)", min_value=1, max_value=4),
            "Hang_Ngang": st.column_config.NumberColumn("🪑 Hàng/Bàn (1-6)", min_value=1, max_value=6),
            "Cho_Ngoi": st.column_config.NumberColumn("Vị trí (1=Trái, 2=Phải)", min_value=1, max_value=2),
            "Avatar_URL": st.column_config.TextColumn("🖼️ Link Avatar", width="large"),
        },
        hide_index=True, num_rows="fixed", height=600
    )
    if st.button("💾 LƯU MỌI THAY ĐỔI VỀ HỌC SINH"):
        df_moi.to_csv(FILE_DATA, index=False)
        st.success("🎉 Đã lưu sơ đồ! Hãy bấm F5 để xem thay đổi.")
elif mk != "":
    st.error("❌ Sai mật khẩu!")
