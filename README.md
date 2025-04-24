# 🛍️ Customer Segmentation App

This interactive Streamlit app helps you explore customer purchasing behavior using real-world retail data. We perform customer segmentation using **K-Means Clustering** based on **Recency**, **Frequency**, and **Monetary (RFM)** values.

Whether you're curious about how loyal customers behave, how much different countries order, or you want to drill down into individual customer behavior — this app has got you covered!

---

## 📊 Key Features

- **RFM Feature Engineering** to capture customer value
- **KMeans Clustering** to segment customers into behavioral groups
- **Visualizations**:
  - Interactive scatter plots (e.g., Unit Price vs Quantity)
  - Country-wise heatmaps
  - Customer order tables and summaries
  - Histograms with adjustable filters
- **Two Main Pages**:
  1. **Exploratory Data Analysis (EDA)** – Understand general trends
  2. **Individual Customer Insights** – Dive deep into one customer's activity

---

## 🧾 Dataset

This app uses an online retail dataset with the following features:

| Feature      | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **InvoiceNo**  | Unique invoice number (invoices starting with 'C' indicate cancellations) |
| **StockCode**  | Product/item code                                                         |
| **Description**| Product name                                                              |
| **Quantity**   | Quantity of the item purchased                                            |
| **InvoiceDate**| Date and time of the transaction                                          |
| **UnitPrice**  | Price per unit (in Sterling)                                              |
| **CustomerID** | Unique identifier for each customer                                       |
| **Country**    | Customer's country of residence                                           |

---


### 🌐 Live App
👉 [Click here to try the app!](https://custmrsegment.streamlit.app/)



### 1. Clone the Repo
```bash
git clone https://github.com/ayushimandlik/customer_segmentation_app.git
cd customer_segmentation_app

