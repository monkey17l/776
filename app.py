import streamlit as st
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-lite"

SYSTEM_PROMPT = """
너는 따뜻하고 현실적인 연애상담 챗봇이야.
사용자의 감정을 먼저 공감하고, 단정하지 말고, 구체적인 선택지를 제안해.
위험하거나 학대/스토킹/자해 가능성이 보이면 안전을 우선으로 안내해.
"""

st.set_page_config(page_title="연애상담 챗봇", page_icon="💬")
st.title("💬 연애상담 챗봇")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되어 있지 않습니다.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕. 무슨 일이 있었는지 편하게 말해줘 🙂"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("상황을 입력해 주세요...")

def to_gemini_contents(messages):
    contents = []
    for msg in messages:
        if msg["role"] == "user":
            role = "user"
        elif msg["role"] == "assistant":
            role = "model"
        else:
            continue

        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )
    return contents

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            contents = to_gemini_contents(st.session_state.messages)

            stream = client.models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.8,
                ),
            )

            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"오류가 발생했습니다: `{e}`"
            placeholder.error(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

with st.sidebar:
    st.header("설정")
    if st.button("대화 초기화"):
        st.session_state.messages = [
            {"role": "assistant", "content": "대화를 초기화했어요. 다시 이야기해줘 🙂"}
        ]
        st.rerun()
