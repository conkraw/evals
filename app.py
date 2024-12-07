import streamlit as st
import openai


# Set your OpenAI API key here
openai.api_key = st.secrets["openai"]["api_key"]

# Function to call OpenAI API for comment generation
def generate_narrative_comment(user_comment):
    prompt = f"Assume you are an experienced educator. Please take the following comment: '{user_comment}' and create an honest comment that highlights the student's strengths and where they need to improve on."

    # Call OpenAI GPT-3 to generate a response
    response = openai.Completion.create(
        #model="text-davinci-003",  # You can choose another model if preferred
        model="gpt-3.5-turbo-16k"
        prompt=prompt,
        max_tokens=150,  # Adjust the number of tokens based on your requirements
        temperature=0.7  # Adjust temperature for creativity
    )

    # Get the generated response from OpenAI API
    return response.choices[0].text.strip()

# Streamlit App Layout
st.title("Narrative Comment Tool")

# Input section for user comment
user_comment = st.text_area("Enter your comment:", height=150)

# Generate narrative comment when the user presses a button
if st.button("Generate Narrative Comment"):
    if user_comment.strip():
        with st.spinner('Generating narrative comment...'):
            generated_comment = generate_narrative_comment(user_comment)
            st.subheader("Generated Narrative Comment")
            st.write(generated_comment)
    else:
        st.error("Please enter a comment before generating!")
