import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Segmentation App", layout="wide")

st.markdown("""
## 🛍️ Customer Segmentation with K-Means Clustering

This project explores **customer segmentation** using transactional data from a UK-based online retailer. The dataset includes the features below:

| Feature      | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **InvoiceNo**  | Unique invoice number (invoices starting with 'C' indicate cancellations) |
| **StockCode**  | Product/item code                                                         |
| **Description**| Product name                                                              |
| **Quantity**   | Quantity of the item purchased                                            |
| **InvoiceDate**| Date and time of the transaction                                          |
| **UnitPrice**  | Price per unit (in Sterling)                                              |
| **CustomerID** | Unique identifier for each customer                                       |
| **Country**    | Customer's country of residence

The goal is to better understand purchasing patterns and group customers into meaningful segments using **unsupervised learning**.

To achieve this, I applied **K-Means clustering** on carefully engineered features derived from RFM (Recency, Frequency, Monetary) analysis. Each customer is assigned to one of four segments based on their behavior — such as VIPs, loyal regulars, occasional spenders, or bargain hunters.

This interactive app allows you to explore general purchasing trends, zoom into individual customer behavior, and visualize how each customer fits within the broader segmentation landscape.

🔗 [See full write-up and code on my portfolio site](https://ayushimandlik.github.io/Customer_seg.html)
""")


# Load the clustered RFM data
@st.cache_data
def load_data(file):
    return pd.read_csv(file)


df = load_data('rfm_clusters.csv')
df1 = load_data('Online_retail.csv')
df1.drop(columns=["Unnamed: 0"], inplace = True)
df1['Total_price'] = df1['UnitPrice'] * df1['Quantity']
df1 = df1.dropna()
df1 = df1[df1['Total_price']  >0]

cluster_labels = {
    0: "Bargain Shoppers",
    1: "High-Spenders",
    2: "Moderate Spenders",
    3: "Business Buyers"
}
df["Cluster_Label"] = df["Cluster"].map(cluster_labels)
cluster_summary = df.groupby("Cluster_Label").agg({
    "Recency": "mean",
    "Frequency": "mean",
    "Monetary": "mean",
    "CustomerID": "count"
}).rename(columns={"CustomerID": "Num Customers"}).reset_index()



grouped = df1.groupby("CustomerID").agg({
    "Quantity": "sum",
    "UnitPrice": "mean",
    "Country": "first"
}).reset_index()

# Merge with cluster data
viz_df = pd.merge(grouped, df[["CustomerID", "Cluster"]], on="CustomerID")
viz_df["Cluster_Label"] = viz_df["Cluster"].map(cluster_labels)


# App Title
#st.set_page_config(page_title="Customer Segmentation App", layout="wide")

st.markdown("### 📂 Explore the Dashboard")
st.markdown(
    "Use the tabs below to explore overall customer behavior through EDA, or dive into detailed views for individual customers."
    )

# Navigation
page = st.radio(
    "Choose a page:",
    ["📊 Summary & EDA", "👤 Individual Customer View"],
    horizontal=True
)

# PAGE 1: Summary & EDA
if page == "📊 Summary & EDA":

    st.markdown("### 📊 Cluster Summary")
    st.markdown("Explore customer behavior through RFM-based clustering.")
    # Show cluster summary

    st.dataframe(cluster_summary.style.format({
        "Recency": "{:.1f}", "Frequency": "{:.1f}", "Monetary": "${:.0f}"
        }))


	# --- Dropdown to select column ---
    st.subheader("🔍 Distribution Viewer")
    selected_column = st.selectbox(
        "Choose a feature to view its distribution",
        options=["Total_price", "Quantity", "UnitPrice"],
        index=0
    )

    # --- Slider to select percentile cutoff ---
    percentile_cutoff = st.slider(
        f"Select max percentile to display for {selected_column}",
        min_value=50,
        max_value=100,
        value=90,
        step=5
    )

    # --- Filter the data based on selected percentile ---
    cutoff_value = df1[selected_column].quantile(percentile_cutoff / 100)
    filtered_data = df1[df1[selected_column] <= cutoff_value]

    # --- Plot histogram ---
    fig = px.histogram(
        filtered_data,
        x=selected_column,
        nbins=100,
        title=f"📦 Distribution of {selected_column} (≤ {percentile_cutoff}th Percentile)"
    )

    fig.update_layout(
        xaxis_title=selected_column,
        yaxis_title="Count",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


    # First, aggregate by country
    country_order_df = df1.groupby("Country").agg({"InvoiceNo": "count"}).reset_index()
    country_order_df.rename(columns={"InvoiceNo": "OrderCount"}, inplace=True)
    country_order_df["Log10OrderCount"] = np.log10(country_order_df["OrderCount"].replace(0, 1))


    fig_country = px.choropleth(
        country_order_df,
        locations="Country",
        locationmode="country names",
        color="Log10OrderCount",
        color_continuous_scale="Turbo",
        hover_name="Country",
        hover_data={"OrderCount": True, "Log10OrderCount": False},
        title="🗺️ Orders by Country"
    )

    # Customize color bar
    fig_country.update_layout(coloraxis_colorbar=dict(
        title="Orders",
        tickvals=[0, 1, 2, 3, 4, 5],
        ticktext=["1+", "10+", "100+", "1K+", "10K+", "100K+"]
    ))

    st.plotly_chart(fig_country)

#df1['Total_price'] = df1['UnitPrice'] * df1['Quantity']
    #q1 = df1["Total_price"].quantile(0.30)
    #q3 = df1["Total_price"].quantile(0.70)
    #iqr = q3 - q1

    #upper_limit = q3 + (1.5 * iqr)
    #lower_limit = q1 - (1.5 * iqr)

#
    #fig = px.histogram(df1, x="Total_price", nbins=100, title="💰 Distribution of Order Values")
    ##fig.update_layout(
    #        #xaxis=dict(range=[q1, q3]))
    #        #xaxis=dict(range=[lower_limit, upper_limit]))
    #st.plotly_chart(fig, use_container_width=True)


    # Visualizations
    st.markdown("### 📈 RFM Distributions by Cluster")

    df["Cluster_Label"] = df["Cluster"].map(cluster_labels)

    color_map = {
            "Bargain Shoppers": "#636EFA",
            "High-Spenders" : "#EF553B",
            "Moderate Spenders" : "#00CC96",
            "Business Buyers" : "#AB63FA"
    }


    fig_m = px.box(df, x="Cluster_Label", y="Monetary", color="Cluster_Label",
               color_discrete_map=color_map,title="Monetary Value by Cluster")
    fig_m.update_traces(marker=dict(line=dict(width=1, color='black')))
    fig_m.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_m, use_container_width=True)


    fig_r = px.box(df, x="Cluster_Label", y="Recency", color="Cluster_Label",
               color_discrete_map=color_map,title="Recency by Cluster")
    fig_r.update_traces(marker=dict(line=dict(width=1, color='black')))
    fig_r.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_r, use_container_width=True)

    fig_f = px.box(df, x="Cluster_Label", y="Frequency", color="Cluster_Label",
               color_discrete_map=color_map,title="Frequency by Cluster")
    fig_f.update_traces(marker=dict(line=dict(width=1, color='black')))
    fig_f.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_f, use_container_width=True)


elif page == "👤 Individual Customer View":
    st.header("👤 Explore a Customer")

    st.markdown("### 🔍 Search Customer")
    customer_ids = df["CustomerID"].dropna().astype(int).unique()
    selected_id = st.selectbox("🔍 Select a Customer ID", customer_ids)
    if selected_id:
        customer_data = df[df["CustomerID"] == selected_id]
        if not customer_data.empty:
            st.subheader(f"📇 Customer ID: {selected_id}")
            st.write(customer_data)
            cluster_id = customer_data["Cluster"].values[0]
            cluster_label = cluster_labels.get(cluster_id, "Unknown Cluster")
            cluster_label = cluster_labels.get(cluster_id, "Unknown Cluster")
            st.info(f"🧠 This customer belongs to **Cluster {cluster_id}: {cluster_label}**.")




    # Step 2: Create the scatter plot with color by label
    fig_scatter = px.scatter(
        viz_df,
        x="UnitPrice",
        y="Quantity",
        color="Cluster_Label",  # use the descriptive label, not the number
        hover_data=["CustomerID", "Country"],
        title="📦 Unit Price vs Quantity by Cluster",
        color_discrete_sequence=px.colors.qualitative.Set2  # Or Set1, Dark2, etc.
    )

    fig_scatter.update_traces(marker=dict(opacity=0.5), selector=dict(mode='markers'))

    selected_row = viz_df[viz_df["CustomerID"] == selected_id]
    fig_scatter.add_trace(go.Scatter(
        x=selected_row["UnitPrice"],
        y=selected_row["Quantity"],
        mode="markers+text",
        marker=dict(size=18, color="black", symbol="star"),
        name="Selected Customer",
        text=[f"Customer {selected_id}"],
        textposition="top center",
        showlegend=True
    ))

    fig_scatter.update_layout(
        xaxis=dict(range=[viz_df["UnitPrice"].min() - 20, viz_df["UnitPrice"].max() + 5]),
        yaxis=dict(range=[viz_df["Quantity"].min() - 50000, viz_df["Quantity"].max() + 10])
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


    st.markdown("### 📋 Customer Order History")
    customer_cluster = df[df['CustomerID'] == selected_id]['Cluster'].item()

    customer_orders = df1[df1["CustomerID"] == selected_id]
    total_orders = customer_orders["InvoiceNo"].nunique()
    total_items = customer_orders["Quantity"].sum()
    total_spent = (customer_orders["Quantity"] * customer_orders["UnitPrice"]).sum()
    avg_unit_price = customer_orders["UnitPrice"].mean()
    first_purchase = pd.to_datetime(customer_orders["InvoiceDate"]).min().strftime("%b %Y")
    last_purchase = pd.to_datetime(customer_orders["InvoiceDate"]).max().strftime("%b %Y")
    customer_country = customer_orders["Country"].iloc[0]
    cluster_name = cluster_labels[customer_cluster]

    # Build summary
    summary_text = f"""
    🧾 **Customer Summary**

    - This customer is classified as a **{cluster_name}**.
    - They are based in **{customer_country}**, and have placed **{total_orders} orders**.
    - In total, they purchased **{total_items} items** and spent approximately **£{total_spent:,.2f}**.
    - Their average unit price is **£{avg_unit_price:.2f}** per item.
    - Their purchases span from **{first_purchase} to {last_purchase}**.
    """

    # Display it
    st.markdown(summary_text)
    st.dataframe(customer_orders)



# Download section
#st.markdown("### 💾 Download Segmentation Results")
#csv = df.to_csv(index=False)
#st.download_button(
#    label="Download full dataset as CSV",
#    data=csv,
#    file_name='rfm_clusters.csv',
#    mime='text/csv',
#)
#
