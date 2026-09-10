import streamlit as st
from groq import Groq

# Page layout configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# App Header
st.title("✍️ AI Content Assistant")
st.markdown("Generate platform-optimized posts, captions, and hashtags instantly using **Groq**.")

# Sidebar for API Key & Settings
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Secure API Key input (Users can enter their own or pull from Streamlit secrets)
    api_key_input = st.text_input(
        "Enter Groq API Key", 
        type="password", 
        help="Get a free key from https://console.groq.com"
    )
    
    st.markdown("---")
    st.markdown("### Model Selection")
    model_choice = st.selectbox(
        "Choose Groq Model",
        ["openai/gpt-oss-120b"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This app leverages lightning-fast inference from Groq to craft target-tailored social media copy.")

# Determine API Key source (Sidebar input or Streamlit Secrets)
api_key = api_key_input if api_key_input else st.secrets.get("GROQ_API_KEY", "")

# Main Form Interface
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type", 
            ["Promotional Post", "Educational Thread", "Thought Leadership", "Engagement Question", "Product Launch"]
        )
        platform = st.selectbox(
            "Platform", 
            ["LinkedIn", "X (Twitter)", "Instagram", "Facebook"]
        )
        
    with col2:
        target_audience = st.text_input(
            "Target Audience", 
            placeholder="e.g., Tech Founders, Gen-Z, Fitness Beginners"
        )
        tone = st.selectbox(
            "Tone of Voice", 
            ["Professional & Authoritative", "Casual & Friendly", "Witty & Humorous", "Inspirational & Motivational", "Direct & Urgent"]
        )
        
    topic = st.text_area(
        "Topic / Core Message", 
        placeholder="Briefly describe what you want to share..."
    )
    
    submitted = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Logic execution on form submission
if submitted:
    if not api_key:
        st.error("⚠️ Please enter your Groq API Key in the sidebar or configure it in Streamlit Secrets.")
    elif not topic.strip():
        st.warning("⚠️ Please provide a topic or core message.")
    elif not target_audience.strip():
        st.warning("⚠️ Please specify a target audience.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Construct clear prompt instructions for the LLM
            prompt = f"""
            You are an expert social media manager and copywriter.
            Create a complete, ready-to-publish social media post based on the parameters below:
            
            - Content Type: {content_type}
            - Platform: {platform}
            - Target Audience: {target_audience}
            - Tone: {tone}
            - Topic/Core Message: {topic}
            
            Format your output strictly using these headers:
            ### 📝 Caption / Post Body
            [The main body of the post optimized for the platform, formatting, and character style]
            
            ### #️⃣ Hashtags
            [5 to 8 targeted, highly relevant hashtags separated by spaces]
            """
            
            with st.spinner("🤖 Crafting your content..."):
                chat_completion = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": "You are a professional content creator helper."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_completion_tokens=1024,
                )
                
                result = chat_completion.choices[0].message.content
                
            # Display Success and Output
            st.success("✨ Content generated successfully!")
            st.markdown("---")
            st.markdown(result)
            
            # Actionable helper
            st.markdown("---")
            st.caption("Tip: You can highlight and copy the text block above directly, or use it for your upcoming calendar.")
            
        except Exception as e:
            st.error(f"❌ An error occurred during generation: {e}")
