#!/usr/bin/env python3
"""
Streamlit App: Agent WITHOUT Memory Demo
Run with: streamlit run no_memory_demo.py
"""

import streamlit as st
from strands import Agent


def create_agent():
    """Create agent WITHOUT memory"""
    agent = Agent(
        name="TravelAssistant",
        system_prompt="You are a helpful travel assistant. Provide travel recommendations.",
        hooks=[],
        tools=[]
    )
    return agent


def main():
    st.set_page_config(page_title="Agent WITHOUT Memory Demo", page_icon="🤖")
    
    st.title("🤖 Agent WITHOUT Memory Demo")
    st.markdown("Chat with an AI agent that **does NOT remember** previous conversations!")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.info("💡 **No Memory**: Each message is independent!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()
        st.success("✅ Agent initialized WITHOUT memory")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about travel..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.agent(prompt)
                    response = result.message['content'][0]['text']
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Info
    with st.expander("ℹ️ Agent Info"):
        st.write("**Memory:** None")
        st.write(f"**Messages in UI:** {len(st.session_state.messages)}")
        st.warning("⚠️ Agent cannot access previous conversation context!")


if __name__ == "__main__":
    main()
