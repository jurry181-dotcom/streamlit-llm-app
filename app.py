from dotenv import load_dotenv
load_dotenv()


import streamlit as st
st.title("2つの領域の専門家に質問するWebアプリ")
input_message = st.text_input(label="下記のどちらかの専門家への質問を入力してください。")

selected_item = st.radio(
    "相談したい専門家を選択してください。",
    ["ITエンジニア", "医者"]
)

st.divider()

# --- LLM応答取得部分を関数化 ---
def get_llm_response(input_message: str, selected_item: str):
    from langchain_openai import ChatOpenAI
    from langchain.schema import SystemMessage, HumanMessage

#目的: input_messageが空、または未入力の場合に、関数の処理を中断し、何も返さずに終了するためです。
#これにより、無効な入力で無駄にLLMへ問い合わせをしないようにしています。
    if not input_message:
        return None

    if selected_item == "ITエンジニア":
        system_content = "あなたはITエンジニアです。"
    elif selected_item == "医者":
        system_content = "あなたは医者です。"
    else:
        return None#安全策（想定外のエラー防止）

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=input_message),
    ]
    result = llm(messages)
    return result.content if result else None#安全策（想定外のエラー防止）
# --- ここまで関数化部分 ---

if st.button("実行"):
    st.divider()
    if input_message:
        result = get_llm_response(input_message, selected_item)
        if result:
            st.write(result)
        else:
            st.error("回答の生成に失敗しました。")
    else:
        st.error("質問を入力してから「実行」ボタンを押してください。")
