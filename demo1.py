from langchain_community.utilities import SQLDatabase

mysql_uri = "mysql+mysqlconnector://root:9952811@localhost:3306/Ezticket"
db = SQLDatabase.from_uri(mysql_uri)

# print(db.dialect)
# print(db.get_usable_table_names())
# output = db.run("SELECT * FROM User LIMIT 10;")

# print(output)

from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
# from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains import create_sql_query_chain

llm = ChatOllama(model="llama3")
# llm = ChatGoogleGenerativeAI(
#     google_api_key = "AIzaSyA-WcZvlwOGIcV_BJN0BHWoawZ99QH5v2I",
#     model = "gemini-1.5-flash"
# );

# chain = create_sql_query_chain(llm, db)
# response = chain.invoke({"question": "How many users are there?"})
# print(response)

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
response = chain.invoke({"question": "How many ticket types are there"})
# print(response)

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

response = chain.invoke({"question": "How many users are there"})
print(response)
# from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

# execute_query = QuerySQLDataBaseTool(db=db)
# write_query = create_sql_query_chain(llm, db)
# chain = write_query | execute_query
# response = chain.invoke({"question": "How many User are there"})
# response = db.run()
# print(response)

# from operator import itemgetter

# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnablePassthrough

# answer_prompt = PromptTemplate.from_template(
#     """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

# Question: {question}
# SQL Query: {query}
# SQL Result: {result}
# Answer: """
# )

# chain = (
#     RunnablePassthrough.assign(query=write_query).assign(
#         result=itemgetter("query") | execute_query
#     )
#     | answer_prompt
#     | llm
#     | StrOutputParser()
# )

# response = chain.invoke({"question": "How many User are there"})
# print(response)
