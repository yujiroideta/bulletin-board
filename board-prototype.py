#  ミニ掲示板アプリの試作

import streamlit as st
import os
import json
from datetime import datetime

# 投稿データ保存ファイル
DATA_FILE = "posts.json"

# データ読み込み関数
def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# データ保存関数
def save_post(name, message):
    posts = load_posts()
    posts.insert(0, {
        "name": name,
        "message": message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

# 投稿処理 + フォームリセット
def post_message():
    name = st.session_state["name_input"]
    message = st.session_state["msg_input"]

    if name and message:
        save_post(name, message)
        st.success("投稿が保存されました！")
        # 入力フォームをクリア
        st.session_state["name_input"] = ""
        st.session_state["msg_input"] = ""
    else:
        st.warning("名前とメッセージを入力してください。")

# --- Streamlit UI ---
st.title("📋 ミニ掲示板アプリ")

# 投稿完了フラグがある場合はフォームをリセット

# 入力フォーム（session_stateで管理）
st.text_input("名前", key="name_input")
st.text_area("メッセージ", key="msg_input")

# 投稿ボタンにコールバック関数を設定
st.button("投稿する", on_click=post_message)

# 投稿表示
st.subheader("📝 みんなの投稿")

for post in load_posts():
    st.markdown(f"**{post['name']}**（{post['time']}）")
    st.write(post['message'])
    st.markdown("---")
