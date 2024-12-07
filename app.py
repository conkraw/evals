import streamlit as st
import openai

# Access the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Function to call OpenAI API for comment generation
def generate_narrative_comment(user_comment, pronoun):
    # Construct the messages for the chat model
    messages = [
        {"role": "system", "content": "You are an experienced educator providing constructive feedback for medical students."},
        {"role": "user", "content": f"Please take the following comment: '{user_comment}' and write a concise, honest narrative comment for the student's evaluation. The comment should be specific and focus on concrete examples of the student's strengths, behaviors, and actions. Highlight areas where the student excels, as well as specific areas where they need to improve. Provide actionable suggestions for improvement, particularly around their performance in clinical settings, teamwork, communication, or professional behavior. Use the pronoun '{pronoun}' for the student. Avoid generalities and be as specific as possible in your feedback."}
    ]

    # Call OpenAI's GPT-3.5-turbo model (Chat API)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  # Using the turbo model with 16k token capacity
        messages=messages,
        max_tokens=500,  # Increased max_tokens to allow for longer responses
        temperature=0.7  # Adjust temperature for creativity
    )

    # Get the generated response from OpenAI API
    return response['choices'][0]['message']['content'].strip()

# Streamlit App Layout
st.title("Narrative Comment Tool")

# Input section for user comment
user_comment = st.text_area("Enter your comment:", height=150)

# Select pronoun for the student
pronoun = st.selectbox("Select student's pronoun:", options=["he", "she", "they"])

# Generate narrative comment when the user presses a button
if st.button("Generate Narrative Comment"):
    if user_comment.strip():
        with st.spinner('Generating narrative comment...'):
            generated_comment = generate_narrative_comment(user_comment, pronoun)
            st.subheader("Generated Narrative Comment")
            st.write(generated_comment)
    else:
        st.error("Please enter a comment before generating!")

