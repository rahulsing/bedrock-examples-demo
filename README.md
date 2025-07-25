# bedrock-examples-demo

## Prerequsite 
- Python 3.10
- AWS Account
- Bedrock Model Access

## Bedrock AgentCore

### Bedrock AgentCore Memory
To demo each of this feature we will be using Streamlit app. 

#### 1. No Memory Agent
To demo the problem of Simple Agent without memory.

##### 📚 [`Memory/01-NoMemory/`](./Memory/01-NoMemory)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 2. Agent with Short Term Memory

##### 📚 [`Memory/02-ShortTerm/`](./Memory/02-ShortTerm)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 3. Agent with Long Term Memory

##### 📚 [`Memory/03-LongTerm/`](./Memory/02-LongTerm)
The conversation will be stored after apply the different stragey like summerization the stored in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the user preference or historical information. 

- User-preference (built-in)
- Semantic (built-in)
- Summarization (built-in)
- Or you build your own strategy. 


