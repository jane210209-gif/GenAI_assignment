import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Professional Message Writer",
    page_icon="✉️",
    layout="centered"
)

# Application Heading
st.title("AI Professional Email & LinkedIn Message Writer")

st.write(
    "Create professional emails and LinkedIn messages "
    "quickly using Artificial Intelligence."
)

st.divider()

# API Configuration
api_key = st.secrets.get("GROQ_API_KEY", "")

# User Input Section
st.subheader("Enter Your Message Details")

message_type = st.selectbox(
    "Choose Message Type",
    ["Professional Email", "LinkedIn Message"]
)

purpose = st.text_input(
    "Purpose",
    placeholder="Example: Internship application"
)

recipient = st.text_input(
    "Recipient Name (Optional)",
    placeholder="Example: HR Manager"
)

details = st.text_area(
    "Message Details",
    placeholder="Enter the details you want to include..."
)

tone = st.selectbox(
    "Choose Message Tone",
    ["Formal", "Friendly", "Polite", "Professional"]
)

# Generate Message
if st.button("Generate Message"):

    if not api_key:
        st.error("Please configure your Groq API key.")

    elif not purpose or not details:
        st.warning("Please enter the purpose and message details.")

    else:
        try:
            client = Groq(api_key=api_key)

            prompt = f"""
            Generate a well-written {message_type}.

            Purpose: {purpose}
            Recipient: {recipient if recipient else "Not specified"}
            Details: {details}
            Tone: {tone}

            Requirements:
            - Use correct grammar.
            - Maintain a professional style.
            - Keep the message clear and meaningful.
            - Make it suitable for real-world communication.
            - Return only the generated message.
            """

            with st.spinner("Generating your message..."):

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            generated_message = response.choices[0].message.content

            st.success("Message generated successfully!")

            st.subheader("Generated Message")

            st.text_area(
                "Your Message",
                value=generated_message,
                height=300
            )

            st.download_button(
                label="Download Message",
                data=generated_message,
                file_name="professional_message.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error generating message: {e}")

st.divider()

st.caption(
    "AI Professional Message Writer | "
    "Developed using Python, Streamlit and Groq"
)
