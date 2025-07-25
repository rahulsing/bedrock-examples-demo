#!/usr/bin/env python3
"""
Streamlit App: AgentCore Long-Term Memory Demo
Run with: streamlit run long_term_memory_demo.py
"""

import streamlit as st
from datetime import datetime
from strands import Agent
from strands.hooks import AfterInvocationEvent, HookProvider, HookRegistry, MessageAddedEvent
from strands_tools import calculator
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.constants import StrategyType

class LongTermMemoryHookProvider(HookProvider):
    def __init__(self, memory_id: str, client: MemoryClient, actor_id: str, session_id: str):
        self.memory_id = memory_id
        self.client = client
        self.actor_id = actor_id
        self.session_id = session_id
        self.namespace = f"/students/math/{self.actor_id}"
    
    def retrieve_memories(self, event: MessageAddedEvent):
        messages = event.agent.messages
        if messages[-1]["role"] == "user" and "toolResult" not in messages[-1]["content"][0]:
            user_message = messages[-1]["content"][0].get("text", "")
            
            try:
                memories = self.client.retrieve_memories(
                    memory_id=self.memory_id,
                    namespace=self.namespace,
                    query=user_message
                )
                
                memory_context = []
                for memory in memories:
                    if isinstance(memory, dict):
                        content = memory.get('content', {})
                        if isinstance(content, dict):
                            text = content.get('text', '').strip()
                            if text:
                                memory_context.append(text)
                
                if memory_context:
                    context_text = "\n".join(memory_context)
                    original_text = messages[-1]["content"][0].get("text", "")
                    messages[-1]["content"][0]["text"] = (
                        f"{original_text}\n\nPrevious context: {context_text}"
                    )
                    st.info(f"🧠 Retrieved {len(memory_context)} memories")
                    
            except Exception as e:
                st.error(f"Memory retrieval error: {e}")
    
    def save_memories(self, event: AfterInvocationEvent):
        try:
            messages = event.agent.messages
            if len(messages) >= 2 and messages[-1]["role"] == "assistant":
                user_msg = None
                assistant_msg = None
                
                for msg in reversed(messages):
                    if msg["role"] == "assistant" and not assistant_msg:
                        assistant_msg = msg["content"][0]["text"]
                    elif msg["role"] == "user" and not user_msg and "toolResult" not in msg["content"][0]:
                        user_msg = msg["content"][0]["text"]
                        break
                
                if user_msg and assistant_msg:
                    self.client.create_event(
                        memory_id=self.memory_id,
                        actor_id=self.actor_id,
                        session_id=self.session_id,
                        messages=[(user_msg, "USER"), (assistant_msg, "ASSISTANT")]
                    )
                    st.success("💾 Saved to long-term memory")
                    
        except Exception as e:
            st.error(f"Memory save error: {e}")
    
    def register_hooks(self, registry: HookRegistry):
        registry.add_callback(MessageAddedEvent, self.retrieve_memories)
        registry.add_callback(AfterInvocationEvent, self.save_memories)

def create_memory():
    """Create or get existing long-term memory with semantic strategy"""
    client = MemoryClient()
    
    # Get existing memories
    memories = client.list_memories()
    
    # If any memory exists, use the first one
    if memories:
        memory_id = memories[0]['id']
        return memory_id, client
    
    # Create new memory with unique name to avoid conflicts
    unique_name = f"MathAssistant_{datetime.now().strftime('%Y%m%d_%H%M')}"
    
    strategies = [{
        StrategyType.SEMANTIC.value: {
            "name": "MathLearningMemory",
            "description": "Captures math learning patterns",
            "namespaces": ["/students/math/{actorId}"]
        }
    }]
    
    memory = client.create_memory_and_wait(
        name=unique_name,
        strategies=strategies,
        description="Long-term memory for math learning",
        event_expiry_days=30
    )
    return memory['id'], client

def main():
    st.set_page_config(page_title="Long-Term Memory Demo", page_icon="🧮")
    
    st.title("🧮 Math Assistant - Long-Term Memory Demo")
    st.markdown("**A math tutor that remembers your learning progress across sessions!**")
    
    # Initialize memory
    if "memory_setup" not in st.session_state:
        with st.spinner("Setting up long-term memory..."):
            try:
                memory_id, client = create_memory()
                st.session_state.memory_id = memory_id
                st.session_state.client = client
                st.session_state.memory_setup = True
                st.success(f"✅ Memory initialized: {memory_id[:8]}...")
            except Exception as e:
                st.error(f"❌ Memory setup failed: {e}")
                return
    
    # Persistent identifiers for memory continuity across browser refreshes
    actor_id = "demo_student"
    session_id = f"{actor_id}_{st.session_state.memory_id[:8]}_session"
    
    # Create agent with long-term memory
    if "agent" not in st.session_state:
        memory_hooks = LongTermMemoryHookProvider(
            memory_id=st.session_state.memory_id,
            client=st.session_state.client,
            actor_id=actor_id,
            session_id=session_id
        )
        
        st.session_state.agent = Agent(
            hooks=[memory_hooks],
            tools=[calculator],
            system_prompt="You are a helpful math tutor. Use your memory to provide personalized assistance based on the student's learning history."
        )
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me a math question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.agent(prompt)
                    response = result.message['content'][0]['text']
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Sidebar
    with st.sidebar:
        st.header("🧠 Memory Status")
        st.write(f"**Memory ID:** {st.session_state.memory_id[:8]}...")
        st.write(f"**Student ID:** {actor_id}")
        st.write(f"**Session ID:** {session_id}")
        st.write(f"**Memory Type:** Long-term (30 days)")
        
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
