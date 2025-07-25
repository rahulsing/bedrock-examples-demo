#!/usr/bin/env python3
"""
Simplified AgentCore Memory Demo
Shows how short-term memory persists across browser sessions
"""

import streamlit as st
from datetime import datetime
from strands import Agent
from strands.hooks import AgentInitializedEvent, HookProvider, HookRegistry, MessageAddedEvent
from bedrock_agentcore.memory import MemoryClient


class MemoryHookProvider(HookProvider):
    """Handles loading and saving messages to AgentCore Memory"""
    def __init__(self, memory_client, memory_id, actor_id, session_id):
        self.memory_client = memory_client
        self.memory_id = memory_id
        self.actor_id = actor_id
        self.session_id = session_id

    def on_agent_initialized(self, event: AgentInitializedEvent):
        """Load recent conversation when agent starts"""
        try:
            # Get last 5 conversation turns from memory
            history = self.memory_client.get_last_k_turns(
                memory_id=self.memory_id, actor_id=self.actor_id, 
                session_id=self.session_id, k=5
            )
            
            if history:
                # Convert to agent message format
                context_messages = []
                for turn in history:
                    for message in turn:
                        role = "assistant" if message["role"] == "ASSISTANT" else "user"
                        content = message["content"]["text"]
                        context_messages.append({"role": role, "content": [{"text": content}]})
                
                event.agent.messages = context_messages
                st.info(f"🔄 Loaded {len(context_messages)} messages from memory")
        except Exception as e:
            st.error(f"Memory load error: {e}")

    def on_message_added(self, event: MessageAddedEvent):
        """Save new message to memory"""
        messages = event.agent.messages
        self.memory_client.create_event(
            memory_id=self.memory_id, actor_id=self.actor_id, session_id=self.session_id,
            messages=[(messages[-1]["content"][0]["text"], messages[-1]["role"])]
        )

    def register_hooks(self, registry: HookRegistry):
        registry.add_callback(AgentInitializedEvent, self.on_agent_initialized)
        registry.add_callback(MessageAddedEvent, self.on_message_added)

def get_memories():
    """Get available memories from AgentCore"""
    try:
        client = MemoryClient()
        memories = client.list_memories()
        result = {}
        for m in memories:
            memory_id = m['id']
            name = m.get('name', f'Memory-{memory_id[:8]}')
            display_name = f"{name} ({memory_id[:8]}...)"
            result[display_name] = memory_id
        return result
    except Exception as e:
        st.error(f"Failed to load memories: {e}")
        return {}

def create_memory(name: str):
    """Create short-term memory (no strategies = raw events only)"""
    client = MemoryClient()
    memory = client.create_memory_and_wait(
        name=name, strategies=[], description="Short-term memory", event_expiry_days=7
    )
    return memory['id']


def main():
    st.set_page_config(page_title="AgentCore Memory Demo", page_icon="🧠")
    st.title("🧠 AgentCore Short-Term Memory Demo")
    st.markdown("**Memory persists across browser refreshes for 7 days!**")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Memory selection
        memories = get_memories()
        if memories:
            memory_option = st.selectbox("Select Memory:", [""] + list(memories.keys()))
            memory_id = memories.get(memory_option, "")
        else:
            st.warning("No memories found")
            memory_id = ""
        
        # Create new memory
        with st.expander("➕ Create Memory"):
            new_name = st.text_input("Name", value="MyMemory")
            if st.button("Create") and new_name:
                create_memory(new_name)
                st.rerun()
        
        # Settings
        actor_id = st.text_input("Actor ID", value="demo_user")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main logic
    if not memory_id:
        st.warning("Please select or create a memory")
        return
    
    # Key insight: session_id based on memory ensures persistence across browser refreshes
    session_id = f"{actor_id}_{memory_id[:8]}_session"
    
    # Initialize agent with memory
    if "agent" not in st.session_state or st.session_state.get("current_memory") != memory_id:
        client = MemoryClient()
        hook = MemoryHookProvider(client, memory_id, actor_id, session_id)
        st.session_state.agent = Agent(
            name="Assistant", 
            system_prompt="You are a helpful assistant with memory.",
            hooks=[hook]
        )
        st.session_state.current_memory = memory_id
        st.success(f"✅ Connected to memory: {memory_id[:8]}...")
    
    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.agent(prompt)
                    response = result.message['content'][0]['text']
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Memory info
    with st.expander("Memory Info"):
        st.write(f"**Memory ID:** {memory_id}")
        st.write(f"**Session ID:** {session_id}")
        st.write(f"**Current messages:** {len(st.session_state.messages)}")


if __name__ == "__main__":
    main()
