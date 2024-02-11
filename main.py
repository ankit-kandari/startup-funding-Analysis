import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout = "wide",page_title = "startup_analysis")

def overall_detail():
    st.title("overall analysis")

    #total invested amount
    total = round(df["amount"].sum())
    comp  = df.groupby("startup")["amount"].sum().sort_values(ascending = False).head(1).index[0]
    max = df.groupby("startup")["amount"].sum().sort_values(ascending = False).head(1)[0]
    mean = df.groupby("startup")["amount"].sum().mean()
    total_startups = df["startup"].nunique()
    col1,col2 = st.columns(2)
    with col1:
        st.metric("total", str(round(total)) + "Cr")
    with col2:
        st.metric("max", comp + " : " + str(round(max)) + "Cr")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("avg", str(round(mean)) + "Cr")
    with col4:
        st.metric("total startups", str(total_startups))

    st.header("month_wise")
    s_option = st.selectbox("select_type",["total","count"])
    if s_option == "total":
        t_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
    else:
        t_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    t_df["year_month"] = t_df["month"].astype("str") + "-" + t_df["year"].astype("str")
    fig3, ax3 = plt.subplots()
    ax3.plot(t_df["year_month"],t_df["amount"])
    st.pyplot(fig3)





def investor_detail(investor):
    #st.title(investor)
    #load latest investment of investor
    recent = df[df["investors"].str.contains(investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("recent investments")
    st.dataframe(recent)


    #largest investments
    col1,col2 = st.columns(2)
    with col1:
        large = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Largest investments")
        #st.dataframe(largest)
        largest  = pd.Series(large)
        fig, ax = plt.subplots()
        ax.bar(largest.index,largest.values)
        st.pyplot(fig)

    with col2:
        sectors = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum().sort_values(
            ascending=False).head(5)
        st.subheader("Largest sectors")
        fig1, ax1 = plt.subplots()
        ax1.pie(sectors,labels = sectors.index,autopct = "%0.01f%%")
        st.pyplot(fig1)

    df["year"] = df["date"].dt.year
    year_wise = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    st.subheader("year wise investment")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_wise.index,year_wise.values)
    st.pyplot(fig2)




df = pd.read_csv("startup_cleaned1.csv")
df["date"]=pd.to_datetime(df["date"],errors = "coerce")
df["month"]=df["date"].dt.month
df["year"]=df["date"].dt.month
st.sidebar.title("Indian startup funding")
option = st.sidebar.selectbox("select",["overall analysis","startup","investor"])

if option == "overall analysis":
    #st.title("overall analysis")
    #btn0 = st.sidebar.button("overall details")
    #if btn0:
    overall_detail()
elif option == "startup":
    st.sidebar.selectbox("select",sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("find startup details")
    st.title("startup analysis")
else:
    investor = st.sidebar.selectbox("select",set(df["investors"].str.split(",").explode()))
    btn2 = st.sidebar.button("find investors details")
    #st.title("investor analysis")
    if btn2:
        investor_detail(investor)
