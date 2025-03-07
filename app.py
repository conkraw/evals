import streamlit as st
import openai
import random

# Access the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Function to call OpenAI API for comment generation
def generate_narrative_comment(user_comment, pronoun):
    # Construct the messages for the chat model
    messages = [
        {"role": "system", "content": "You are an experienced educator providing constructive feedback for medical students."},
        {"role": "user", "content": f"Please take the following comment: '{user_comment}' and write a concise, honest narrative comment for the student's evaluation. The comment should be specific and focus on concrete examples of the student's strengths, behaviors, and actions. Highlight areas where the student excels, as well as specific areas where they need to improve. Provide actionable suggestions for improvement, particularly around their performance in clinical settings, teamwork, communication, or professional behavior. Use the pronoun '{pronoun}' for the student. Avoid generalities and be as specific as possible in your feedback. Do not use the letter 'e' when writing the comment."}
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
    
def generate_narrative_comment(user_comment, pronoun):
    # Define prompt variations
    prompt_variations = [
        f"Please take the following comment: '{user_comment}' and write a concise, honest narrative comment for the student's evaluation. The comment should be specific and focus on concrete examples of the student's strengths, behaviors, and actions. Highlight areas where the student excels, as well as specific areas where they need to improve. Provide actionable suggestions for improvement, particularly around their performance in clinical settings, teamwork, communication, or professional behavior. Use the pronoun '{pronoun}' for the student. Avoid generalities and be as specific as possible in your feedback.",
        f"Take this provided remark: '{user_comment}' and craft a brief, authentic narrative evaluation for the student. The evaluation should emphasize concrete illustrations of the student’s strengths, conduct, and actions. Highlight domains where the student thrives, alongside particular areas needing improvement. Offer actionable recommendations for growth, especially regarding their clinical skills, collaboration, interaction, or professionalism. Use the pronoun '{pronoun}' for the student. Steer clear of generalities and remain as precise as feasible.",
        f"Using the following comment: '{user_comment}', compose a concise and sincere narrative for the student's assessment. Focus on specific examples of the student's capabilities, behaviors, and achievements. Point out where the student performs exceptionally, as well as areas that require attention for improvement. Share concrete suggestions for betterment, particularly in clinical tasks, teamwork, communication skills, or professional demeanor. Use the pronoun '{pronoun}' for the student. Be detailed and avoid general statements.",
        f"Take this input: '{user_comment}' and formulate a succinct, genuine narrative comment for evaluating the student. The feedback should prioritize tangible examples of the student’s positive attributes, actions, and areas for growth. Highlight their standout qualities and provide specific, actionable advice on improving in clinical settings, team interactions, communication, or professionalism. Use '{pronoun}' as the student’s pronoun. Stay precise and avoid broad statements.",
        f"Given the comment: '{user_comment}', draft a clear and honest narrative for the student’s evaluation. Ensure the comment includes specific instances of their strengths, behaviors, and skills. Identify where they excel and where targeted improvement is needed. Provide practical advice for advancing their abilities in clinical work, collaboration, communication, or professionalism. Use the pronoun '{pronoun}' for the student. Avoid vague feedback."
    ]

    # Randomly select a prompt variation
    selected_prompt = random.choice(prompt_variations)

    # Construct the messages for the chat model
    messages = [
        {"role": "system", "content": "You are an experienced educator providing constructive feedback for medical students."},
        {"role": "user", "content": selected_prompt}
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

st.write("""
Welcome to the **Narrative Comment Generator**! This tool will assist you in creating thoughtful, constructive feedback for medical students based on a few sentences you provide. Please follow these steps:

### 1. Input Your Comment
In the text box below, type a few sentences describing the student's performance, behavior, or actions. Focus on **specific examples**. What did the student do well, and where can they improve?

### 2. Specify the Pronoun
Choose the pronoun that best reflects the student (e.g., "he," "she," or "they"). This will ensure that the generated comment is personalized to your input.

### 3. Guidelines for Your Comment
The generated comment will serve as a **guide** to help you structure your feedback. However, please review and adjust the generated text to fit your own observations and the context of the evaluation.

### 4. Feedback Focus
The tool will help generate a comment that:
- Highlights the student's **strengths** and areas where they excel.
- Provides **specific examples** of behaviors or actions that demonstrate these strengths.
- Suggests areas for **improvement**, particularly in clinical performance, teamwork, communication, or professionalism.

**Important Note**: Please do not use the generated comment verbatim in your official evaluation. It is just a starting point, and you should personalize it with your own insights and context.
""")


# Input section for user comment
st.subheader("Provide the student's performance or behavior description:")
user_comment = st.text_area("Describe the student's performance here...", height=150)

# Select pronoun for the student
pronoun = st.selectbox("Select student's pronoun:", options=["he", "she", "they"])

import io
from docx import Document
import streamlit as st

# Let the user enter a student's name (or any identifier) to be used in the filename
student_name = st.text_input("Enter Student's Name (optional):")

# Your existing user comment input
#user_comment = st.text_area("Enter comment:")

# Generate narrative comment when the user presses a button
if st.button("Generate Narrative Comment"):
    if user_comment.strip():
        with st.spinner('Generating narrative comment...'):
            generated_comment = generate_narrative_comment(user_comment, pronoun)
            st.subheader("Generated Narrative Comment")
            st.write(generated_comment)
            
            # Create a Word document using python-docx
            doc = Document()
            doc.add_paragraph(generated_comment)
            
            # Save the document to an in-memory bytes buffer
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            # Create a filename based on the student's name if provided
            filename = f"{student_name}_narrative_comment.docx" if student_name.strip() else "narrative_comment.docx"
            
            # Provide a download button for the Word document
            st.download_button(
                label="Download Comment as Word File",
                data=buffer,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.error("Please enter a comment before generating!")


