import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
# from dotenv import load_dotenv  <- この行は不要なので削除、またはコメントアウト

# .envファイルから環境変数を読み込む <- この行も不要なので削除
# load_dotenv()

def get_llm_response(user_input, expert_choice):
    """
    LLMからの回答を取得する関数

    引数:
    - user_input (str): ユーザーが入力したテキスト
    - expert_choice (str): ユーザーが選択した専門家

    戻り値:
    - str: LLMからの回答
    """
    # ★★★ ここが変更点 ★★★
    # StreamlitのシークレットからAPIキーを読み込んで渡す
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=st.secrets["OPENAI_API_KEY"] # この行を追加
    )

    # 専門家の選択に応じて、システムメッセージ（AIへの指示）を変更する
    if expert_choice == "マーケティングの専門家":
        system_message_content = "あなたは優秀なマーケティングの専門家です。ユーザーの質問に対して、マーケティング戦略や顧客インサイトの観点から、具体的で実践的なアドバイスをしてください。"
    elif expert_choice == "フィットネストレーナー":
        system_message_content = "あなたは経験豊富なフィットネストレーナーです。ユーザーの質問に対して、科学的根拠に基づいた、安全で効果的なトレーニング方法や栄養指導をしてください。"
    elif expert_choice == "料理研究家":
        system_message_content = "あなたは創造性あふれる料理研究家です。ユーザーの質問に対して、手軽に作れる美味しいレシピや、料理がもっと楽しくなるコツを提案してください。"
    else:
        # デフォルトの指示
        system_message_content = "あなたは親切なアシスタントです。"

    # LLMに渡すメッセージを作成
    messages = [
        SystemMessage(content=system_message_content),
        HumanMessage(content=user_input),
    ]

    # LLMから回答を取得
    response = llm.invoke(messages)
    return response.content


# --- Streamlit アプリの画面構成 ---

# 1. アプリのタイトルと説明
st.title("🤖 AI専門家 なりきりチャット")
st.write("AIが様々な分野の専門家になりきって、あなたの質問に答えます。")
st.write("---")


# 2. 専門家を選択するラジオボタン
expert_option = st.radio(
    label="どの専門家に相談しますか？",
    options=("マーケティングの専門家", "フィットネストレーナー", "料理研究家"),
    index=0, # デフォルトの選択
    horizontal=True,
)


# 3. ユーザーからの質問を入力するフォーム
user_question = st.text_area("質問を入力してください...", height=150)


# 4. 送信ボタン
if st.button("質問する"):
    if user_question:
        # 質問があれば、関数を呼び出して回答を取得
        with st.spinner("AIが考え中です..."):
            answer = get_llm_response(user_question, expert_option)
            st.write("---")
            st.write(f"**{expert_option}からの回答:**")
            st.write(answer)
    else:
        # 質問がなければ、メッセージを表示
        st.warning("質問を入力してください。")