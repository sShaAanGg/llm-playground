# from langchain_community.llms import LlamaCpp
# from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

# # Callbacks support token-wise streaming
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# # Make sure the model path is correct for your system!
# llm = LlamaCpp(
#     model_path="/home/shang/.ollama/Meta-Llama-3-8B.Q2_K.gguf",
#     temperature=0.75,
#     max_tokens=2000,
#     top_p=1,
#     callback_manager=callback_manager,
#     verbose=True,  # Verbose is required to pass to the callback manager
# )
llm = Ollama(model='llama2')
embeddings = OllamaEmbeddings(model='llama2')
loader = UnstructuredMarkdownLoader('./functional_metrics.md')
pages = loader.load_and_split()
print("Loaded", len(pages), "pages")
vectordb = FAISS.from_documents(pages, embeddings)
print("Created FAISS index")
retriever = vectordb.as_retriever()

@traceable # Auto-trace this function
def pipeline(user_input: str):
    prompt = ChatPromptTemplate.from_messages([
        ('system', """You are an expert in the field of computer science, 
        software engineering, and programming. Please review the following code, 
        provide a score, and point out the code that can be improved based on the metrics:\n\n{context}."""),
        ('user', 'Code: {input}'),
    ])
    doc_chain = create_stuff_documents_chain(llm, prompt)
    ret_chian = create_retrieval_chain(retriever, doc_chain)
    response = ret_chian.invoke({
        'input': user_input,
        'context': context
    })
    return response

context = []
input_file = input('Please input a file> ')
while input_text != 'exit':
    input_text = open(input_file, 'r').read()
    response = pipeline(input_text)
    print(response['answer'])
    context = response['context']
    input_file = input('Please input a file> ')
