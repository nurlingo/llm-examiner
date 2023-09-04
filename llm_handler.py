from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate, LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain


from dotenv import load_dotenv
load_dotenv()


async def query_llm(
        knowledge_base_id: str, 
        outcome: str, 
        number_of_questions: int,
        question_types: [str],
        llm_model: str = "gpt-3.5-turbo") -> str:

    template = """
    You are an expert in education. 
    You goal is to test learners.
    Given a learning outcome, create an assessment quiz that corresponds to the outcome.
    
    The learning outcome is: {question}
    """
    
    template = template + f"""
    The quiz will have {number_of_questions} questions.
    Questions will be of the following types: {question_types}
    
    Here are the format for each question type:

    Single Selection:
    This question type has up to five answers options indexed by letters.
    The question has only one right answer.
    Write "Q: " before the question.
    Include the correct answer's index with "CA: " prefix.

    Multiple Selection:
    This question type has up to five answer options indexed by letters.
    Every question must have two or more correct answer options.
    Write "Q: " before questions.
    Mark the correct answers with "CA: " prefix.

    Rearrange the Lines:
    Generate a sequence of 5-8 actions or events related to the outcome.
    Return title and elements of sequences with prefix "- " in correct order.
    Prefix sequences by "S: "

    Tap To Code:
    Generate a question related to the outcome.
    Answer it with a sentence. Follow the pattern:
    Q: [question]
    A: [answer]

    Predict The Output:
    Generate a question related to the outcome with a single word as the answer.
    Return all right one-word answer variations, including likely typo mistakes.
    Follow the pattern:
    Q: [question]
    CA: [answer variant, ...]
    """

    llm = ChatOpenAI(temperature=1, model=llm_model)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    condense_question_prompt = PromptTemplate(template=template, input_variables=['question'])
    condense_question_chain = LLMChain(
        llm=llm,
        prompt=condense_question_prompt,
    )

    doc_prompt = PromptTemplate(
        template="Content: {page_content}\nSource: {source}",
        input_variables=["page_content", "source"]
    )

    final_qa_chain = StuffDocumentsChain(
        llm_chain=condense_question_chain,
        document_variable_name="question",
        document_prompt=doc_prompt,
    )

    db = Chroma(
        persist_directory=f"./chroma/{knowledge_base_id}",
        embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
    )

    retrieval_qa = ConversationalRetrievalChain(
        question_generator=condense_question_chain,
        retriever=db.as_retriever(),
        memory=memory,
        combine_docs_chain=final_qa_chain,
    )

    res = retrieval_qa.run({"question": outcome})
    print(res)

    return res


# # test from terminal:
# import asyncio
# knowledge_base_id = "namaz"
# outcome = "how to perform washing before the prayer"
# number_of_questions = 10  # Change this to your desired number
# question_types = ["Single Selection", "Multiple Selection:", "Rearrange the Lines", "Tap To Code", "Predict The Output"]  # Replace with actual question types

# # Call the asynchronous function using asyncio
# result = asyncio.run(query_llm(
#     knowledge_base_id, outcome, number_of_questions, question_types))
