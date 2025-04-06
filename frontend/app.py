import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender")

API_URL = "http://3.110.124.223:8000/recommend"  # deployed URL

st.title("🔍 SHL Assessment Recommender")

# Example query to guide the user
example_query = "Looking to hire mid-level professionals who are proficient in Python, SQL, and JavaScript. Need an assessment package that can test all skills with a max duration of 60 minutes."

query = st.text_area("Enter job description or query", height=150, placeholder=example_query)

if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Finding best assessments..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                response.raise_for_status()
                results = response.json().get("results", [])

                if results:
                    st.success(f"Showing top {len(results)} matches")
                    for res in results:
                        st.markdown(f"**[{res['Name']}]({res['URL']})**")
                        st.write(f"- Duration: {res['Duration']}")
                        st.write(f"- Remote: {res['Remote']}, Adaptive: {res['Adaptive']}")
                        st.write(f"- Type: {res['Type']}")
                        st.markdown("---")
                else:
                    st.warning("No matches found.")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the recommendation engine: {e}")
