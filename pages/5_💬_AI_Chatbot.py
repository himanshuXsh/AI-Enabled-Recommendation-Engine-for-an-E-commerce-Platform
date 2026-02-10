import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

# --- Page Configuration ---
st.set_page_config(page_title="AI Assistant", page_icon="💬", layout="wide")

# --- Load Custom CSS ---
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- Header ---
st.title("💬 AI Shopping Assistant")
st.markdown("Main aapka personal shopping assistant hu. Puchiye kuch bhi!")

# ---------------------------------------------------------
# 👇 API KEY SECTION
# ---------------------------------------------------------
hf_api_key = "himm"  # <--- APNI KEY WAPIS YAHA DALEIN
# ---------------------------------------------------------

# --- Sidebar ---
with st.sidebar:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Main DeepSeek AI hu. Main aapki kya madad kar sakta hu?"}
    ]

# --- Display Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Logic ---
if prompt := st.chat_input("Apna sawal yaha likhein..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if hf_api_key.startswith("hf_xxxx"):
                    st.error("⚠️ Please code mein apni asli API Key paste karein!")
                    st.stop()

                repo_id = "deepseek-ai/deepseek-coder-1.3b-instruct"

                llm = HuggingFaceEndpoint(
                    repo_id=repo_id,
                    max_new_tokens=200,
                    temperature=0.5,  # Maine Temperature kam kiya (0.7 -> 0.5) taaki wo creative na bane
                    top_p=0.9,
                    huggingfacehub_api_token=hf_api_key,
                    task="text-generation",
                    stop_sequences=["\nUser:", "<|endoftext|>"] # IMP: Ye usse rokega taaki wo khud se baat na kare
                )

                # --- FIX: PROMPT STRUCTURE ---
                # Chote models ko "ChatML" format pasand hota hai.
                # Humne structure change kiya hai taaki wo confuse na ho.
                template = """<|im_start|>system
You are a helpful AI E-commerce Assistant.
Answer the user's question directly and concisely in Hindi or English.
Do NOT repeat the prompt.
<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
"""
                
                prompt_template = PromptTemplate(template=template, input_variables=["question"])
                chain = prompt_template | llm
                response = chain.invoke({"question": prompt})
                
                # Cleaning the response
                clean_response = response.strip()
                
                # Kabhi kabhi model prompt repeat kar deta hai, usse hatane ke liye:
                if "<|im_start|>assistant" in clean_response:
                    clean_response = clean_response.split("<|im_start|>assistant")[-1].strip()

                st.markdown(clean_response)
                st.session_state.messages.append({"role": "assistant", "content": clean_response})
                
            except Exception as e:
                st.error("Error connecting to AI Model.")
                st.caption(str(e))