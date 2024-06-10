import streamlit as st
st.set_page_config(
    page_title="DocInsight",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items=None
)
import io
from openai import OpenAI
import pdfplumber
import docx2txt

# Function to get answer from GPT
def get_answer_from_text(text, question, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-Turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that goes through text files and answers questions."
            },
            {
                "role": "user",
                "content": f'\n\n TEXT: {text} \n\n QUESTION: {question}'
            }
        ],
        temperature=0.64,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

def main():
    # Your OpenAI API key
    api_key = "<Insert API KEY here>"
    # Streamlit UI
    title_template="""
    <div style="background-color:#333333;padding:5px;">
    <h1 style="color:cyan">DocInsight</h1>
    </div>
    """
    st.markdown(title_template, unsafe_allow_html=True)
    st.sidebar.image("logo.jpeg",use_column_width=True)
    menu=["Dropfiles","About"]
    choice=st.sidebar.selectbox("Menu",menu)
    if choice=="Dropfiles":
        st.subheader("Drop Files Here")
        raw_files=st.file_uploader('Upload your files', type=['txt','docx','pdf'], accept_multiple_files=True)
        #Reading File Data
        if raw_files is not None:
            raw_text = ""  # Initialize an empty string to accumulate text from all documents
            for uploaded_file in raw_files:  # Loop through each uploaded file
                if uploaded_file.type == "text/plain":
                    try:
                        text = str(uploaded_file.read(), "utf-8")
                        raw_text += text  # Concatenate the text from the current document
                    except:
                        st.error(".txt file fetching problem!\ncheck your file again and try re-uploading")
                elif uploaded_file.type == "application/pdf":
                    try:
                        pdf_reader = pdfplumber.open(uploaded_file)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            raw_text += page.extract_text()  # Concatenate the text from the current page
                    except:
                        st.error(".pdf file fetching problem!\ncheck your file again and try re-uploading")
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    try:
                        raw_text += docx2txt.process(uploaded_file)  # Concatenate the text from the current document
                    except:
                        st.error(".docx file fetching problem!\ncheck your file again and try re-uploading")
        else:
            st.error("You have not uploaded any File!\nPlease Upload a File to continue")

        #getting question from the User
        question = st.text_input('Enter your question')
        #checking if files and question are both there
        if st.button('Get Answer'):
            if raw_files and question:
                with st.spinner('Processing...'):
                    try:
                        answer = get_answer_from_text(raw_text, question, api_key)
                        st.write('### Answer')
                        st.write(answer)
                    except Exception as e:
                        st.error('Error in Fetching answers... \n\n Please Try again Later')
            else:
                st.error('Please provide all the required inputs.')

    if choice=="About":
        st.subheader("About")
        st.write("""
        Welcome to DocQuery!
        
        DocQuery is a powerful app that allows you to upload various document types such as TXT, DOCX, and PDF files, and ask questions about the content. Our app leverages advanced language models to provide accurate and insightful answers based on the uploaded documents.
        
        How it works:
        1. Navigate to the "Dropfiles" section.
        2. Upload your documents.
        3. Enter your question.
        4. Get precise answers based on the document content.
        
        Enjoy exploring and getting answers with ease!
        
        For any issues, feature requests, or collaboration opportunities, please contact us at: 
        abhirupbasu30@gmail.com\n
        +91 8235026220
        """)

if __name__ == "__main__":
    main()
