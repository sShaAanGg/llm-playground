# import openai
# from langsmith.wrappers import wrap_openai
from langchain_community.llms import Ollama
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

# # Auto-trace LLM calls in-context
# client = wrap_openai(openai.Client())

llm = Ollama(model="llama2")

@traceable # Auto-trace this function
def pipeline(user_input: str):
    prompt = ChatPromptTemplate.from_messages([
        ('user', user_input),
    ])
    chain = prompt | llm
    response = chain.invoke({"input": user_input})
    return response
    # result = client.chat.completions.create(
    #     messages=[{"role": "user", "content": user_input}],
    #     model="gpt-3.5-turbo"
    # )
    # return result.choices[0].message.content

input_text = input('> ')
while input_text != 'exit':
    print(pipeline(input_text))
    input_text = input('> ')

# Out:  Hello there! How can I assist you today?
