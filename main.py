import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()

# Configuration for Langflow API
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fc56d784-6cf2-495d-860b-a215dd1fead2"
FLOW_ID = "e36e3f8d-eb1c-4f08-9bad-b471d618d86a"
APPLICATION_TOKEN = os.getenv("APP_TOKEN")  # Store your token in .env

# Load the CSV data
@st.cache_data
def load_data():
    return pd.read_csv("social_media_engagement_data.csv")

# Function to calculate average metrics
def calculate_average_metrics(df, post_type):
    filtered_df = df[df["post_type"] == post_type]
    return {
        "average_likes": filtered_df["likes"].mean(),
        "average_shares": filtered_df["shares"].mean(),
        "average_comments": filtered_df["comments"].mean(),
        "average_sentiment": filtered_df["avg_sentiment_score"].mean(),
    }

# Function to run the Langflow API
def run_flow(message):
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {},
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Main function for Streamlit
def main():
    # Set page config
    st.set_page_config(page_title="Social Media Performance Analysis", layout="wide", page_icon="📊")

    # Load data
    df = load_data()

    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stSelectbox {
        background-color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .fixed-header {
        position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    z-index: 1000;
    }
    .fixed-header h1 {
        margin: 0;
        font-size: 24px;
    }
    .fixed-header .logos {
        display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    }
    .fixed-header .logos img {
        height: 60px; /* Adjust logo size as needed */
    margin: 0 15px; /* Add spacing between logos */
    }
    .content {
        margin-top: 80px;
        padding: 20px;
    }
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #333;
        padding: 10px;
        border-radius: 30px;
        margin-bottom: 20px;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        padding: 10px 20px;
        margin: 0 10px;
        border-radius: 20px;
        transition: background-color 0.3s;
    }
    .navbar a:hover, .navbar a.active {
        background-color: #4CAF50;
    }
    .demo-button {
        background-color: #ff4500 !important;
    }
    .demo-button:hover {
        background-color: #ff5722 !important;
    }
    </style>
    """, unsafe_allow_html=True)

   
    # Content wrapper
    st.markdown('<div class="content">', unsafe_allow_html=True)


    # Navbar
    st.markdown("""
    <div class="navbar">
        <a href="/" class="nav-item">Home</a>
        <a href="/" class="nav-item">Analysis</a>
        <a href="/About" class="nav-item">About Us</a>
    </div>
    """, unsafe_allow_html=True)

    # Main content
    if st.session_state.get('page') == "Analysis":
        show_analysis_page(df)
    elif st.session_state.get('page') == "About":
        show_about_page()
    else:
        show_home_page()

    # Close content wrapper
    st.markdown('</div>', unsafe_allow_html=True)

def show_home_page():
    st.header("Welcome to Media Matrices")
    st.header("The Social Media Performance Analysis")
    st.write("This application allows you to analyze social media engagement data across different post types.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Key Features:")
        st.markdown("- 📈 Analyze engagement metrics")
        st.markdown("- 📊 Visualize data with interactive charts")
        st.markdown("- 🤖 Get AI-powered insights")
        st.markdown("- 📱 Compare performance across post types")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)
        if st.button("Get Started", key="get_started"):
            st.session_state.page = "Analysis"
        if st.button("Watch Demo", key="watch_demo", help="Watch a demo of the application"):
            st.markdown("[Watch Demo on YouTube](https://www.youtube.com)", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_analysis_page(df):
    st.header("Social Media Performance Analysis")
    
    # Post type selection
    post_types = df["post_type"].unique()
    post_type = st.selectbox("Select Post Type", post_types, key="post_type_select")
    
    # Calculate metrics
    metrics = calculate_average_metrics(df, post_type)
    
    # Display metrics in columns
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>Average Likes</h3><h2>{metrics['average_likes']:.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>Average Shares</h3><h2>{metrics['average_shares']:.2f}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>Average Comments</h3><h2>{metrics['average_comments']:.2f}</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><h3>Average Sentiment</h3><h2>{metrics['average_sentiment']:.2f}</h2></div>", unsafe_allow_html=True)
    
    # Visualizations
    st.markdown("---")
    st.subheader("Engagement Metrics Visualization")
    
    # Bar chart
    fig_bar = px.bar(df[df["post_type"] == post_type], x="post_id", y=["likes", "shares", "comments"], 
                     labels={"value": "Count", "variable": "Metric"},
                     title=f"Engagement Metrics for {post_type.capitalize()} Posts")
    fig_bar.update_layout(legend_title_text="Metric")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Scatter plot
    fig_scatter = px.scatter(df[df["post_type"] == post_type], x="likes", y="shares", size="comments", color="avg_sentiment_score",
                             labels={"likes": "Likes", "shares": "Shares", "comments": "Comments", "avg_sentiment_score": "Sentiment Score"},
                             title=f"Correlation between Likes, Shares, Comments, and Sentiment for {post_type.capitalize()} Posts")
    fig_scatter.update_layout(coloraxis_colorbar=dict(title="Sentiment Score"))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # AI Insights
    st.markdown("---")
    st.subheader("AI-Powered Insights")
    if st.button("Generate Insights", key="generate_insights"):
        with st.spinner("Generating insights..."):
            insights = run_flow(f"Analyze the performance of {post_type} posts based on the following metrics: Average Likes: {metrics['average_likes']:.2f}, Average Shares: {metrics['average_shares']:.2f}, Average Comments: {metrics['average_comments']:.2f}, Average Sentiment: {metrics['average_sentiment']:.2f}")
            
            # Extract the main message (assuming the structure)
            out = (
                insights.get("outputs", [{}])[0]  # Get the first item in 'outputs' (default to an empty dict)
                .get("outputs", [{}])[0]  # Access the first item in the nested 'outputs' list
                .get("results", {})  # Access the 'results' key (default to an empty dict)
                .get("message", {})  # Access the 'message' key (default to an empty dict)
                .get("text", "Message not found")  # Extract the 'text' field
            )
            
            st.info(out)

def show_about_page():
    st.header("About Us")
    st.write("This application was developed as part of the Supermind Hackathon.")
    st.write("Our goal is to provide actionable insights into social media performance, helping content creators and marketers optimize their strategies.")
    
    st.markdown("---")
    st.subheader("Our Team")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("https://via.placeholder.com/150", caption="Team Member 1")
        st.markdown("**John Doe**")
        st.markdown("Data Scientist")
    with col2:
        st.image("https://via.placeholder.com/150", caption="Team Member 2")
        st.markdown("**Jane Smith**")
        st.markdown("UX Designer")
    with col3:
        st.image("https://via.placeholder.com/150", caption="Team Member 3")
        st.markdown("**Mike Johnson**")
        st.markdown("Full Stack Developer")
    with col4:
        st.image("https://via.placeholder.com/150", caption="Team Member 4")
        st.markdown("**Sarah Williams**")
        st.markdown("AI Specialist")
    
    st.markdown("---")
    st.subheader("Contact Us")
    st.write("For more information or support, please reach out to us:")
    st.markdown("📧 Email: info@supermind-hackathon.com")
    st.markdown("🌐 Website: www.supermind-hackathon.com")
    st.markdown("📱 Phone: +1 (123) 456-7890")

if __name__ == "__main__":
    main()

