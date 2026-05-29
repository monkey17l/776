import streamlit as st
import random

# 웃긴 말 리스트
jokes = [
    "배고픈데 다이어트 중이면 그건 정신력 RPG",
    "월요일은 버그처럼 갑자기 찾아온다",
    "커피를 마셨더니 사람이 된 기분이다",
    "5분만 쉰다 = 2시간 순삭",
    "내 통장도 다이어트 중",
    "코딩은 원인을 찾으면 새로운 오류가 나온다"
]

st.title("🤣 웃긴 말 생성기")

st.write("버튼을 누르면 웃긴 말을 해줍니다!")

if st.button("웃긴 말 보기"):
    st.success(random.choice(jokes))
