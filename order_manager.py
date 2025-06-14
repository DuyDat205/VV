import pandas as pd
from datetime import datetime
import os

ORDER_FILE = "orders.xlsx"

def save_order(cart, buyer_name):
    if not cart:
        return False

    data = []
    for item in cart:
        data.append({
            "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Khách hàng": buyer_name,
            "Tên sản phẩm": item["name"],
            "Giá": item["price"]
        })

    df_new = pd.DataFrame(data)

    if os.path.exists(ORDER_FILE):
        df_old = pd.read_excel(ORDER_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_excel(ORDER_FILE, index=False)
    return True

def load_orders():
    if os.path.exists(ORDER_FILE):
        return pd.read_excel(ORDER_FILE)
    else:
        return pd.DataFrame()
