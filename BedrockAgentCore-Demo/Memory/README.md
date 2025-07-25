## Bedrock AgentCore Memory
To demo each of this feature we will be using Streamlit app. 

## To run the demo: 
Navigate to the folder and run the below : 
```
streamlit run appy.py
``` 
#### 1. No Memory Agent
To demo the problem of Simple Agent without memory.

##### 📚 [`BedrockAgentCore-Demo/Memory/01-NoMemory`](./BedrockAgentCore-Demo/Memory/01-NoMemory/no-memory-demo.py)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 2. Agent with Short Term Memory

##### 📚 [`BedrockAgentCore-Demo/Memory/02-ShortTerm/`](./BedrockAgentCore-Demo/Memory/02-ShortTerm/short-term-memory_demo.py)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

For demo: 
A. Create Memory named "TravelPersona" 
B. Create Memory named "PersonalPersona" 
C. Select "TravelPersona" Memory, then type prompt "I need to travel to London"
C. Select "PersonalPersona" Memory, then type prompt "I love to eat to Pasta"
E. Then try below question by switching the Persona to understand the Memory usage and behvior: 
Do you know where I need to travel ?
Do you know what I like to eat?

#### 3. Agent with Long Term Memory

##### 📚 [`BedrockAgentCore-Demo/Memory/03-LongTerm/`](./BedrockAgentCore-Demo/Memory/02-LongTerm/long-term-memory-demo.py)

The conversation will be stored after apply the different stragey like summerization the stored in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the user preference or historical information. 

- User-preference (built-in)
- Semantic (built-in)
- Summarization (built-in)
- Or you build your own strategy.

###### Session 1: Initial Learning Profile"
```
Hi, I'm Mark, a 10th grade student. I'm struggling with algebra and prefer step-by-step explanations with examples. Can you help me solve: 2x + 5 = 13?
```
```
I learn better when you show me similar problems. Can you give me another equation like that one?
```
```
That's helpful! I notice I make mistakes with negative numbers. Can you explain how to handle them in equations?
```

###### Session 2: Memory Recall Test (Click "🔄 New Session" first)
Hi, it's Mark again. Can you remind me what we worked on last time?
```
I'm still having trouble with those negative number problems you mentioned. Can you give me more practice?
```
What math topics should I focus on next based on what you know about my learning?
```
Session 3: Progress Tracking
I've been practicing the problems you gave me. I got most of them right! What's the next level I should try?
```
Can you create a personalized study plan based on my strengths and weaknesses?
```