from dotenv import load_dotenv
import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ロジック部分
def llm_function(mode, input_prompt):
    modes = {
        "医療の専門家": ("あなたは医療の専門家です。専門用語を使って丁寧に説明してください。", 0),
        "コメディアン": ("あなたはベテランコメディアンです。砕けた表現でユーモアを交えて説明してください。", 1),
        "フレンドリーな先輩": ("あなたはフレンドリーな先輩です。簡潔に分かりやすく説明してください。", 0.5),
    }
    system_message, temperature = modes.get(mode, modes["フレンドリーな先輩"])
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=temperature)
    messages = [SystemMessage(content=system_message), HumanMessage(content=input_prompt)]
    return llm(messages).content

# 表示部分
st.title("LLM Simple App")
st.write("Welcome to the LLM Simple App!")

selected_item = st.radio("動作モードを選択してください。", ["医療の専門家", "コメディアン"])
st.divider()
st.write(f"{selected_item}が選択されました。")

input_message = st.text_input(label="質問内容", placeholder="質問内容を入力してください。")
if st.button("実行"):
    result = llm_function(selected_item, input_message)
    st.write("結果:", result)
st.divider()
