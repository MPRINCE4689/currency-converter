import streamlit as st
import pandas as pd
from io import StringIO

# Page config
st.set_page_config(page_title="Currency Converter", layout="centered")

# --- Exchange rates ---
exchange_rates = {
    "USD": 1.0,
    "EUR": 0.8654,
    "GBP": 0.76,
    "INR": 86.09,
    "JPY": 144.17,
    "CAD": 1.35,
    "AUD": 1.48,
    "CHF": 0.90,
    "CNY": 7.25,
    "SGD": 1.36
}

currencies = list(exchange_rates.keys())

# Custom styles
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 15px;
    }
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .fixed-title {
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 999;
        padding: 10px 0;
    }
    .convert-btn > button {
        background-color: #20B2AA !important;
        color: white !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("<h3 class='fixed-title' style='color: teal; text-align:center;'>Currency Converter</h3>", unsafe_allow_html=True)

# --- Centered Amount Input ---
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="amt")
st.markdown("</div>", unsafe_allow_html=True)

# --- Currency Dropdowns ---
col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From Currency", currencies)
with col2:
    to_currency = st.selectbox("To Currency", currencies)

# --- Result Placeholder ---
result_placeholder = st.empty()

# --- History Storage ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Convert Button ---
with st.container():
    st.markdown("<div class='convert-btn'>", unsafe_allow_html=True)
    if st.button("Convert Currency"):
        if from_currency == to_currency:
            result_amount = amount
            rate_used = 1.0
        else:
            rate_from = exchange_rates[from_currency]
            rate_to = exchange_rates[to_currency]
            rate_used = rate_to / rate_from
            result_amount = amount * rate_used

        
        result_text = f"💱 {amount:.2f} {from_currency} = {result_amount:.2f} {to_currency}"
        result_placeholder.markdown(f"<p style='color:green;text-align:center;font-size:17px'>{result_text}</p>", unsafe_allow_html=True)

        st.session_state.history.append({
            "Amount": f"{amount:.2f}",
            "From": from_currency,
            "To": to_currency,
            "Result": f"{result_amount:.2f}",
            "Rate": f"{rate_used:.4f}",
            
        })
    st.markdown("</div>", unsafe_allow_html=True)

# --- Conversion History Table ---
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.markdown("### Conversion History")
    st.dataframe(df, use_container_width=True)

    # --- Export Button (Downloads instantly) ---
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Export CSV", data=csv, file_name="conversion_history.csv", mime="text/csv")

    # --- Clear History Button ---
    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("No history yet. Convert some currencies to see your history here.")

