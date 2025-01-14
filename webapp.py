import streamlit as st
import pandas as pd
import matplotlib as plt

# Try to load the data from CSV, create an empty dataframe if it doesn't exist
try:
    dados = pd.read_csv("dados.csv")
except:
    dados = pd.DataFrame({"produtos": [], "preços": []})
    dados.to_csv("dados.csv", index=False)

# Title for the Streamlit app
st.title("Controlo de Compras")

# Input for the budget
orcamento = st.number_input("Orçamento", min_value=0.0)

# Calculate the total price of items in the data
total = dados["preços"].sum() if not dados.empty else 0

# Section to add items
with st.form("adicione_item"):
    produto = st.text_input("Adicione produto:")
    preco = st.number_input("Adicione preço:", min_value=0.0)

    # Button to submit the form
    submit_button = st.form_submit_button("Adicionar")

    if submit_button:
        # Check if the price is within the available budget
        if preco <= (orcamento - total):
            novo_produto = pd.DataFrame({"produtos": [produto], "preços": [preco]})
            dados = pd.concat([dados, novo_produto], ignore_index=True)
            dados.to_csv("dados.csv", index=False)
            st.success("Compra adicionada")
        else:
            st.error("Sem orçamento suficiente")
