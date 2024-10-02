import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_product_performance(df):
    product_performance = df.groupby(by="product_category_name").agg({
    "order_id": "nunique",
    "price": "sum",
    "review_score": "mean"
    })

    product_performance.rename(columns={
        "order_id": "qty_sold",
        "price": "revenue",
        "review_score": "average_score"
    }, inplace=True)

    return product_performance

def create_most_payment(df):
    most_payment_type = df.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False).reset_index()
    most_payment_type.rename(columns={
        "order_id": "counts"
    }, inplace=True)

    return most_payment_type

def create_customer_satisfaction(df):
    cust_satisfaction = df.groupby(by="review_score").order_id.nunique().reset_index()
    cust_satisfaction.rename(columns={
        "order_id": "counts"
    }, inplace=True)

    return cust_satisfaction

def create_bystate(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bystate_df

def create_bycity(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bycity_df

all_df = pd.read_csv("all_dataset.csv")

datetime_columns = ["order_delivered_carrier_date", "order_delivered_customer_date"]
all_df.sort_values(by="order_delivered_customer_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_delivered_customer_date"].min()
max_date = all_df["order_delivered_customer_date"].max()

with st.sidebar:
    st.image("https://fiverr-res.cloudinary.com/image/upload/t_profile_original,q_auto,f_auto/v1/attachments/profile/photo/c1151d1c5b312b5f7e43733a55eb17ec-1666925365905/3cf486a3-2c10-4be6-b561-bcb4b1958303.jpeg")


    start_date, end_date = st.date_input(
        label='Time Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_delivered_customer_date"] >= str(start_date)) & 
                (all_df["order_delivered_customer_date"] <= str(end_date))]

product_performance = create_product_performance(main_df)
most_payment_type = create_most_payment(main_df)
cust_satisfaction = create_customer_satisfaction(main_df)
bystate_df = create_bystate(main_df)
bycity_df = create_bycity(main_df)\

st.header('Kelly Collection Dashboard :sparkles:')

st.subheader('Products Performance')

col1, col2, col3 =st.columns(3)

with col1:
    avg_qty_sold = round(product_performance.qty_sold.mean(), 1)
    st.metric("Average Quantity Sold", value=avg_qty_sold)

with col2:
    avg_revenue = round(product_performance.revenue.mean(), 2)
    st.metric("Average Revenue", value=avg_revenue)

with col3:
    avg_rate = round(product_performance.average_score.mean(), 3)
    st.metric("Average Rating", value=avg_rate)

fig, ax = plt.subplots(ncols=3, nrows= 1, figsize=(40, 15))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="qty_sold", x="product_category_name", data=product_performance.sort_values(by="qty_sold", ascending=False).head(5), ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("By Quantity Sold")
ax[0].tick_params(axis='x', labelsize=15)

sns.barplot(y="revenue", x="product_category_name", data=product_performance.sort_values(by="revenue", ascending=False).head(5), ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("By Revenue")
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="average_score", x="product_category_name", data=product_performance.sort_values(by="average_score", ascending=False).head(5), ax=ax[2])
ax[2].set_xlabel(None)
ax[2].set_ylabel(None)
ax[2].set_title("By Rating")
ax[2].tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Customer Demography")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(35, 15))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="customer_state",
        x="customer_count",
        data=bystate_df.sort_values(by="customer_count", ascending=False).head(8),
        palette=colors
    )

    plt.title("Customer Demographics by State", loc="center", fontsize=50)
    plt.xlabel(None)
    plt.ylabel(None)


    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(35, 15))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="customer_city",
        x="customer_count",
        data=bycity_df.sort_values(by="customer_count", ascending=False).head(8),
        palette=colors
    )

    plt.title("Customer Demographics by City", loc="center", fontsize=50)
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(fig)


st.subheader("Customer Satisfaction")

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]

sns.barplot(
    y="counts",
    x="review_score",
    hue="review_score",
    legend=False,
    data = cust_satisfaction.sort_values(by="counts", ascending=False),
    palette=colors
)

plt.title("Customer Satisfaction Rating Overall", loc="center", fontsize=40)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Most Used Payment Type")

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="counts",
    y="payment_type",
    data=most_payment_type,
    palette=colors
)

plt.title("Most Used Payment Type", loc="center", fontsize=40)
plt.xlabel(None)
plt.ylabel(None)

st.pyplot(fig)

st.caption('Copyright (c) Kelly 2024')
