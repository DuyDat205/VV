import streamlit as st
import requests

# LINK RAW FILE JSON từ GitHub
PRODUCTS_URL = "https://raw.githubusercontent.com/username/repo/main/products.json"

# Load sản phẩm từ GitHub
@st.cache_data
def load_products():
    response = requests.get(PRODUCTS_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Khởi tạo session cho giỏ hàng
if "cart" not in st.session_state:
    st.session_state.cart = []

# Giao diện trang bán hàng
def main():
    st.set_page_config(page_title="🛒 Cửa hàng điện tử", layout="wide")
    st.title("🛍️ Cửa hàng điện tử trực tuyến")

    products = load_products()

    cols = st.columns(3)

    for i, product in enumerate(products):
        with cols[i % 3]:
            st.image(product["image"], use_column_width=True)
            st.subheader(product["name"])
            st.write(product["description"])
            st.write(f"💰 Giá: {product['price']:,} VND")
            if st.button(f"🛒 Thêm vào giỏ - {product['id']}", key=product["id"]):
                st.session_state.cart.append(product)
                st.success(f"Đã thêm {product['name']} vào giỏ hàng!")

    st.markdown("---")
    st.header("🧾 Giỏ hàng của bạn")

    total = 0
    for item in st.session_state.cart:
        st.write(f"- {item['name']} - {item['price']:,} VND")
        total += item["price"]

    st.subheader(f"🧮 Tổng cộng: {total:,} VND")

    if st.button("🧹 Xóa giỏ hàng"):
        st.session_state.cart = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
