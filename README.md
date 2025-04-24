🛍️ Customer Segmentation App
This interactive Streamlit app helps you explore customer purchasing behavior using real-world retail data. We perform customer segmentation using K-Means Clustering based on Recency, Frequency, and Monetary (RFM) values.

Whether you're curious about how loyal customers behave, how much different countries order, or you want to drill down into individual customer behavior — this app has got you covered!

📊 Key Features
RFM Feature Engineering to capture customer value

KMeans Clustering to segment customers into behavioral groups

Visualizations:

Interactive scatter plots (e.g., Unit Price vs Quantity)

Country-wise heatmaps

Customer order tables and summaries

Histograms with adjustable filters

Two Main Pages:

Exploratory Data Analysis (EDA) – Understand general trends

Individual Customer Insights – Dive deep into one customer's activity

🧾 Dataset
This app uses an online retail dataset with the following features:

Feature	Description
InvoiceNo	Unique invoice number (invoices starting with 'C' indicate cancellations)
StockCode	Product/item code
Description	Product name
Quantity	Quantity of the item purchased
InvoiceDate	Date and time of the transaction
UnitPrice	Price per unit (in Sterling)
CustomerID	Unique identifier for each customer
Country	Customer's country of residence
🚀 Getting Started
1. Clone the Repo
bash
Copy code
git clone https://github.com/yourusername/customer-segmentation-app.git
cd customer-segmentation-app
2. Install Requirements
bash
Copy code
pip install -r requirements.txt
3. Run the App
bash
Copy code
streamlit run app.py
📂 Folder Structure (Example)
bash
Copy code
customer-segmentation-app/
│
├── app.py                    # Streamlit app
├── requirements.txt
├── data/
│   ├── raw_data.csv
│   └── rfm_clustered.csv
├── utils/                    # Preprocessing or helper scripts
│   └── preprocess.py
└── README.md
🌐 Live App
👉 Click here to try the app!

✨ Future Improvements
- Add more clustering algorithms (DBSCAN, Hierarchical)
- Time-series analysis for seasonality
- Recommendation engine prototype

🧠 About
Created by Ayushi — data scientist, explorer, and builder of beautiful dashboards.
Got feedback or suggestions? Let’s connect!
