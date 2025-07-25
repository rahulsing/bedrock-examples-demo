## Bedrock AgentCore Memory
To demo each of this feature we will be using Streamlit app. 

#### 1. No Memory Agent
To demo the problem of Simple Agent without memory.

##### 📚 [`BedrockAgentCore-Demo/Memory/01-NoMemory`](./BedrockAgentCore-Demo/Memory/01-NoMemory/no-memory-demo.py)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 2. Agent with Short Term Memory

##### 📚 [`BedrockAgentCore-Demo/Memory/02-ShortTerm/`](./BedrockAgentCore-Demo/Memory/02-ShortTerm/short-term-memory_demo.py)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 3. Agent with Long Term Memory

##### 📚 [`BedrockAgentCore-Demo/Memory/03-LongTerm/`](./BedrockAgentCore-Demo/Memory/02-LongTerm/long-term-memory-demo.py)
The conversation will be stored after apply the different stragey like summerization the stored in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the user preference or historical information. 

- User-preference (built-in)
- Semantic (built-in)
- Summarization (built-in)
- Or you build your own strategy.