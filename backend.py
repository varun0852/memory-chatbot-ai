import os
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import LLMChain
from langchain_core.chat_history import InMemoryChatMessageHistory



def initialize_gemini_chain(api_key):
    # api_key = "AIzaSyBLQN5NO0DFWiQHAXsAtOueDm308_nD2LE"

    if not api_key:
        return None
    
    llm = ChatGoogleGenerativeAI(
        model ="gemini-3-flash-preview",
        google_api_key = "api_key",
        temperature = 0.7
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system" , "You are a friendly and helpful AI assistant. That Answer Questions clearly."),
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human" , "{question}")
    ])
    memory = ConversationBufferMemory(
        memory_key = "chat_history",
        return_messages = True
    )


    conversation_chain = LLMChain(
        llm = llm,
        prompt = prompt,
        memory = memory,
        verbose = False
    )

    return conversation_chain

def get_chatbot_response(chain , user_input):

    response = chain.invoke({"question" : user_input})
    return response["text"]


   
