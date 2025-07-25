# Bedrock Agent Core - Memory Feature

## Intro
- Amazon Bedrock AgentCore Memory is a feature that allows you to create and manage memory resources for AI agents. 
 It enables agents to maintain context across sessions, recognize returning customers, recall important details, and deliver personalized experiences. 
 Now you dont need to build your own memory story. 


## Types
 There are two main types of memory in AgentCore: 
 1. Short-term memory: This maintains context without persisting historical data. It's useful for tracking current conversation flow, such as in customer support interactions. 
 Short-term memory is quick to set up and doesn't require a memory strategy. 
 
 2. Long-term memory: This type of memory extracts and stores important information from conversations for future use. 
 It allows agents to provide highly personalized assistance without asking users to repeat information they've shared in previous interactions.
 

 The main differences between short-term and long-term memory are: 
- Persistence: Short-term memory doesn't persist historical data, while long-term memory does. 
 
- Setup: Short-term memory is quicker to set up, while long-term memory requires more configuration, including memory strategies. 

- Use case: Short-term memory is ideal for maintaining context within a single session, while long-term memory is used for personalization across multiple interactions. 
 
 ## Implementation: 
 To implement AgentCore Memory, you need to: 
 1. Install the required dependencies (bedrock-agentcore Python package). 
 2. Create a memory resource using the MemoryClient. 
 3. For short-term memory, use the create_event action to store agent interactions. 
 4. For long-term memory, configure memory strategies and use retrieve_memories to access stored information. 
 
 AgentCore Memory can be integrated into AI agents to enhance their ability to maintain context, personalize responses, and provide more effective customer support.

## Monitoring and Metrics 
 Use Logging 