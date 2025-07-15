import streamlit as st
import openai

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="SOC Code Reviewer", layout="wide")
st.title("🤖 AI-Powered SOC Code Reviewer")

st.markdown("""
Paste an internal job description below and the AI will:
- Suggest the most relevant SOC code
- Justify the match
- Suggest wage level (L1-L4)
- Flag red flags and mismatches
""")

jd_input = st.text_area("Paste Internal Job Description:", height=300)
submit = st.button("Analyze JD")

if submit and jd_input:
    with st.spinner("Reviewing JD and matching with SOC codes..."):
        prompt = f"""
You are an immigration compliance reviewer for U.S. job roles. Your task is to review the internal job description and match it to the most appropriate SOC code based on O*NET.

Instructions:
- Compare the internal JD with O*NET duties and examples
- Output the most suitable SOC code and title
- Provide justification for why it fits
- If there’s a mismatch, flag it and suggest better alternatives
- Suggest SVP range and appropriate wage level (L1 to L4)
- Output everything in a structured format

Internal JD:
{jd_input}
"""

        client = openai.OpenAI()
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a highly accurate immigration compliance analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            st.success("Analysis complete.")
            st.markdown("### Review Result:")
            st.markdown(response.choices[0].message.content)
        except openai.RateLimitError:
            st.error("Rate limit reached. Please wait and try again.")
else:
    if submit:
        st.warning("Please paste a job description to begin.")
