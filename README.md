[readme.md](https://github.com/user-attachments/files/21939292/readme.md)
# 🌍 Supply Risk Assessment App (Odoo-ERP + NewsAPI + LLM)

A demo application to assess supply chain risks using live data from **Odoo ERP**, **NewsAPI**, and a **LLM (Gemini)** powered Retrieval-Augmented Generation (RAG) pipeline.

## 🔧 Features

- 📦 Fetch open Purchase Orders from Odoo
- 📰 Query global news data using NewsAPI
- 🧠 Use vector-based RAG to retrieve relevant news context
- 🤖 Leverage Gemini LLM to infer potential risks (geopolitical, weather, financial, etc.)
- ⚠️ Categorize risk and assign severity scores
- 📊 Download structured results as CSV

---

## 🛠️ Tech Stack

| Component | Description |
|----------|-------------|
| **Odoo ERP** | Source for open purchase order data |
| **NewsAPI** | Real-time news for context |
| **qdrant VectorDB** | RAG - Embedding + vector search | 
| **Gemini LLM** | Risk analysis and inference |
| **Streamlit** | Interactive UI |
| **Python** | Core programming language |

---

## 🚀 Setup Instructions

### 1. Clone this Repo

```bash
git clone https://github.com/yourusername/supply-risk-llm-demo.git
cd supply-risk-llm-demo

2. Install Requirements

pip install -r requirements.txt

Make sure you also have access credentials for:
Odoo ERP
NewsAPI key
Gemini / LLM access token
qdant vectorDB



3. Set Up Configuration

Update API keys and paths in the respective modules:
api_newsapi_news.py
api_gemini_llm.py
query_odoo_xmlrpc_v2.py
rag_embedd_query_vectorDB.py

--Purchase order data in Odoo ERP


4. Run the App
streamlit run supply_risk_app.py


📂 Directory Structure

supply-risk-llm-demo/
│
├── modules/
│   ├── query_odoo_xmlrpc_v2.py
│   ├── api_newsapi_news.py
│   ├── api_gemini_llm.py
│   └── rag_embedd_query_vectorDB.py
│---.streamlit/
|    |--- config.toml #for UI settings	
├── company_logo.png
├── supply_risk_app.py
└── README.md


📃 License

MIT License © [Prasanm@outlook.com]


Future Enhancements:

Add weather & climate APIs
Integrate map-based supplier location view
Integrate with transportation and route details for in-transit risk
Historical PO risk trends
Use LocalLLM


Acknowledgements:

Odoo
NewsAPI
OpenAI
Google-Gemini
