import streamlit as st
import pandas as pd

st.title("🚀 TasteOfHome Web Crawler Dashboard")

#recipe_data
recipes = pd.read_csv("recipe_data.json")
st.dataframe(recipes.head())


st.bar_chart(recipes["cooking_time"].value_counts())