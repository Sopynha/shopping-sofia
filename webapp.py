import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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



# Check if the budget is greater than 0
if orcamento > 0:
    # Create the donut chart
    fig, ax = plt.subplots(figsize=(8, 8))

    if not dados.empty:
        produtos = dados["produtos"].tolist()
        valores = dados["preços"].tolist()
        restante = orcamento - total
        
        # Add "Disponível" to the chart if there is remaining budget
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)

        # Create pie chart (donut style)
        ax.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)

        # Add a circle at the center to create the "donut" effect
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)

    ax.set_title(f"Orçamento: {orcamento}€")

    # Display the plot in Streamlit
    st.pyplot(fig)

# Display the data and budget information
st.dataframe(dados)
st.write(f"Total gasto: {total}€")
st.write(f"Restante: {orcamento - total}€")
