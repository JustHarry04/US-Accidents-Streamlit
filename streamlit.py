import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.write("# My First App")

df = pd.read_csv("Tvshows.csv", encoding='ISO-8859-1')
st.dataframe(df)

def convert(vote_count):
    vote_count = vote_count.strip('()')  
    if 'M' in vote_count:
        return int(float(vote_count.replace('M', '')) * 1_000_000)
    elif 'K' in vote_count:
        return int(float(vote_count.replace('K', '')) * 1_000)
    else:
        return int(vote_count)

df['Vote_count'] = df['Vote_count'].apply(convert)

def convert_episodes(episodes):
    return int(episodes.replace(' eps', ''))

df['Total_episodes'] = df['Total_episodes'].apply(convert_episodes)

def convert_age(age):
    try:
        return int(age)
    except ValueError:
        return 0  

df['Age'] = df['Age'].apply(convert_age)

def clean_year_string(year):
    # Replace unwanted characters and strip whitespaces
    year = year.replace('\x96', '–').replace('ï¿½', '–').strip()
    return year

def split_year(year):
    year = clean_year_string(year)
    if '–' in year:
        start_year, end_year = year.split('–')
        try:
            start_year = int(start_year)
        except ValueError:
            start_year = None
        try:
            end_year = int(end_year)
        except ValueError:
            end_year = None
        return start_year, end_year
    else:
        try:
            start_year = int(year)
            end_year = start_year
        except ValueError:
            start_year = None
            end_year = None
        return start_year, end_year

df[['start_year', 'end_year']] = df['Year'].apply(split_year).apply(pd.Series)

df["start_year"] = df["start_year"].fillna(0).astype(int)
df['end_year'] = df['end_year'].fillna(0).astype(int)

df = df.drop(columns=['Year'])

df['Titile'] = df['Titile'].str.replace(r'^\d+\.\s+', '', regex=True)
df = df.rename(columns={'Titile': 'Title'})

st.title('TV Shows Analysis')

df.columns = df.columns.str.strip()
df = df[df['start_year'] >= 1990]

st.write("### Dataset")
st.dataframe(df)

st.sidebar.write("### Basic Statistics")
st.sidebar.write(df.describe())

st.sidebar.write("### Columns in the Dataset")
st.sidebar.write(df.columns)

st.write("### Visualizations")

st.write("#### Distribution of Ratings")
plt.figure(figsize=(10, 6))
sns.histplot(df['Rating'], kde=True)
plt.title('Distribution of Ratings')
st.pyplot(plt)

st.write("#### Countplot of Categories")
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Category')
plt.xticks(rotation=45)
plt.title('Countplot of Categories')
st.pyplot(plt)

st.write("#### Average Rating by Category")
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Category', y='Rating')
plt.xticks(rotation=45)
plt.title('Average Rating by Category')
st.pyplot(plt)

st.write("#### Scatter Plot of Rating vs. Total Episodes")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Total_episodes', y='Rating')
plt.title('Scatter Plot of Rating vs. Total Episodes')
st.pyplot(plt)

st.write("#### Ratings Over the Years")
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='start_year', y='Rating')
plt.title('Ratings Over the Years')
st.pyplot(plt)

st.write("#### Count of TV Shows by Year")
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='start_year')
plt.xticks(rotation=45)
plt.title('Count of TV Shows by Year')
st.pyplot(plt)

st.write("#### Correlation Matrix")
selected_columns = st.multiselect("Select columns for correlation matrix", df.columns, default=['Rating', 'Total_episodes', 'Age'])

if selected_columns:
    corr_matrix = df[selected_columns].corr()
    st.write(corr_matrix)
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    st.pyplot(plt)
