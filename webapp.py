import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Assuming 'dados' DataFrame already exists
orcamento = st.number_input("Orçamento", min_value=0.0)

# Calculate the total of the prices
total = dados["preços"].sum() if not dados.empty else 0

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
