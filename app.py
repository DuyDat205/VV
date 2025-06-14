import streamlit as st
import requests
from order_manager import save_order, load_orders

PRODUCTS_URL = "https://raw.githubusercontent.com/DuyDat205/VV/main/products.json"

@st.cache_data
def load_products():
    try:
        response = requests.get(PRODUCTS_URL)
        return response.json() if response.status_code == 200 else []
    except:
        return []

if "cart" not in st.session_state:
    st.session_state.cart = []

def add_to_cart(product):
    st.session_state.cart.append(product)

def main():
    st.set_page_config("🛒 Shop Điện Tử", layout="wide")
    menu = ["🏠 Trang chủ", "🧾 Giỏ hàng", "📋 Quản lý đơn hàng"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "🏠 Trang chủ":
        st.title("🛍️ Cửa hàng Điện tử Trực tuyến")
        products = load_products()
        cols = st.columns(3)
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.image(product["image"], use_column_width=True)
                st.subheader(product["name"])
                st.write(product["description"])
                st.write(f"💰 Giá: {product['price']:,} VND")
                if st.button(f"🛒 Mua {product['id']}", key=product['id']):
                    add_to_cart(product)
                    st.success(f"Đã thêm {product['name']} vào giỏ hàng.")

    elif choice == "🧾 Giỏ hàng":
        st.title("🛒 Giỏ hàng của bạn")
        if st.session_state.cart:
            total = sum(item["price"] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"- {item['name']} ({item['price']:,} VND)")
            st.subheader(f"🧮 Tổng cộng: {total:,} VND")
            buyer_name = st.text_input("👤 Tên khách hàng:")
            if st.button("✅ Thanh toán"):
                if buyer_name:
                    save_order(st.session_state.cart, buyer_name)
                    st.success("✅ Thanh toán thành công! Đơn hàng đã được lưu.")
                    st.session_state.cart = []
                else:
                    st.warning("❗ Vui lòng nhập tên khách hàng.")
            if st.button("🧹 Xoá giỏ hàng"):
                st.session_state.cart = []
                st.experimental_rerun()
        else:
            st.info("🛒 Giỏ hàng trống.")

    elif choice == "📋 Quản lý đơn hàng":
        st.title("📦 Danh sách đơn hàng")
        df = load_orders()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Chưa có đơn hàng nào.")

if __name__ == "__main__":
    main()
