# -*- coding: utf-8 -*-

"""
Supply Risk Assessment Demo App using Odoo, NewsAPI, RAG, and Gemini LLM
"""

import sys
import streamlit as st
import pandas as pd
import json
import base64

# Append custom module path
sys.path.append(r'C:\Users\USER\Documents\ERP_Projects\Supply_Risk\modules')

# Custom modules
import query_odoo_xmlrpc_v2 as query_odoo
import api_newsapi_news as news_api
import api_gemini_llm as llm
import rag_embedd_query_vectorDB as rag

# --- Constants ---
EMBEDD_COLLECTION = "supplier_risks"
LOGO_PATH = "company_logo.png"

# --- Helper Functions ---

def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

def combine_data(po_data, supplier_name, news_data):
    combined_text = []
    for po in po_data:
        supplier = po['partner_id'][1]
        total_amount = po['amount_total']
        order_date = po['date_order']
        city = po.get("supplier_ship_from", {}).get("city", "")
        country = po.get("supplier_ship_from", {}).get("country_id", ["", ""])[1]

        combined_text.append(f"""Supplier: {supplier}
Supply_city: {city}
Supply_country: {country}
PO Number: {po['name']}
Order Date: {order_date}
Total Amount: {total_amount}
News Articles:
{news_data}

""")
    return "\n".join(combined_text)

# --- UI ---

# Display company logo
logo_base64 = get_image_base64(LOGO_PATH)
if logo_base64:
    st.markdown(
        f"""
        <style>
        .logo-container {{
            position: absolute;
            top: 1px;
            right: 10px;
        }}
        .logo-container img {{
            height: 80px;
        }}
        </style>
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="Company Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("📦 Outstanding Supply Risk Assessment")
st.markdown("""
### 🔄 Process Flow Overview  
📦 **ERP (Odoo)** → 📰 **NewsAPI** → 🤖 **Gemini LLM** → ⚠️ **Risk Categorization** → 📊 **Result**
""")

# Refresh cache
if st.button("🔁 Refresh ERP Data"):
    st.cache_data.clear()
    st.rerun()

# Fetch POs with caching
@st.cache_data(show_spinner=False)
def get_open_purchase_orders():
    return query_odoo.get_open_pos()

# --- Step 1: Get Open POs ---
with st.spinner("🔄 Fetching open purchase orders from Odoo..."):
    po_data = get_open_purchase_orders()

if not po_data:
    st.error("No open purchase orders found.")
    st.stop()

# --- Step 2: PO Selection ---
st.subheader("🧾 Open Purchase Orders (select the PO(s) for analysis)")
selected_po_indices = []

with st.form("po_selection_form"):
    for idx, po in enumerate(po_data):
        supplier = po['partner_id'][1]
        city = po.get("supplier_ship_from", {}).get("city", "")
        country = po.get("supplier_ship_from", {}).get("country_id", ["", ""])[1]

        label = f"[{po['name']}] {supplier} | Amount: {po['amount_total']} | Date: {po['date_order']} | Location: {city}, {country}"
        if st.checkbox(label, key=f"po_{idx}"):
            selected_po_indices.append(idx)

    submitted = st.form_submit_button("🔍 Run Risk Analysis")

# --- Step 3: Risk Analysis ---
if submitted:
    if not selected_po_indices:
        st.warning("Please select at least one PO to assess.")
    else:
        risk_profiles = []

        for idx in selected_po_indices:
            po = po_data[idx]
            supplier_name = po['partner_id'][1]
            city = po.get("supplier_ship_from", {}).get("city", "")
            country = po.get("supplier_ship_from", {}).get("country_id", ["", ""])[1]
            search_query = f"{supplier_name}+{city}+{country}"

            # News search
            with st.spinner(f"🌐 Fetching news for {supplier_name} in {city}, {country}..."):
                news_data = news_api.get_news(search_query)

            # RAG: Embed and retrieve
            with st.spinner(f"🧠 Embedding and retrieving context for {supplier_name}..."):
                combined = combine_data([po], supplier_name, news_data)
                rag.embed_and_store_data(EMBEDD_COLLECTION, combined)
                articles = rag.retrieve_similar_articles(EMBEDD_COLLECTION, search_query, k=5)

            # LLM Risk Inference
            with st.spinner(f"🔎 Analyzing risk with Gemini LLM for {supplier_name}..."):
                prompt = f"""
You are a supply chain risk analyst AI. Analyze the following news for the supplier from the city and the country "{search_query}".
- Summarize the content in one sentence.
- Classify the risk as one of: Operational, Financial, Geopolitical, None.
- Assign a risk score from 1 (low) to 5 (high).

News:
{articles}

Output your answer as a JSON with keys: supplier, summary, risk_type, risk_score.
"""
                response = llm.process_with_gemini(prompt)

            try:
                result_json = json.loads(response.text)
                risk_profiles.append({
                    "PO Number": po["name"],
                    "Supplier": supplier_name,
                    "Summary": result_json.get("summary", ""),
                    "RiskType": result_json.get("risk_type", ""),
                    "RiskScore": result_json.get("risk_score", "")
                })
            except Exception as e:
                st.error(f"❌ Error processing PO {po['name']}: {e}")

        # --- Step 4: Display Results ---
        if risk_profiles:
            st.success("✅ Risk analysis completed.")
            result_df = pd.DataFrame(risk_profiles)
            st.dataframe(result_df)

            csv_data = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Results as CSV", data=csv_data, file_name="supplier_risk_analysis.csv", mime="text/csv")
        else:
            st.warning("⚠️ No risk results could be generated.")

