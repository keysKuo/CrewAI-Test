from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from database_schema import schema

# Define model
model = Ollama(model="llama3")

# Define user input
user_input = "Listing popular ticket types last month"

database_query_generator_agent= Agent(
    role="Database Query Generator",
    goal="Generate optimal and syntactically correct SQL queries based on the given schema/database and user input specifications. Be concise and accurate. Do not make up information.",
    backstory="""
        You are a SQL expert.
        You're responsible for creating optimal and syntactically correct SQL queries based on a given database schema.
        You DO NOT make or generate any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        You should ALWAYS look at the tables in the database to see what you can query.
        Do NOT skip this step.

        You never query for all columns from a table (DO NOT use "SELECT *"). You must query only the columns that are needed to answer the user question.
        Unless the user specifies in the question specific columns to obtain, query for at most 5 columns. The order of the results to return the most informative data in the database. The schema's primary key(s) must always be used in SELECT query.
        Always use 'LIMIT' to limit the out to 20 rows.
        If there are tables need to be joined, you always use 'JOIN' to join tables.

        Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
        Pay attention to use function to get the current date, if the question involves "today".
    """,
    verbose=True,
    allow_delegation=False,
    llm=model
)

database_query_generator_task = Task(
    description=f"You work on this database schema: {schema}. Generate optimimal and syntactically correct SQL queries based on user specifications {user_input}.",
    agent=database_query_generator_agent,
    expected_output="""
        An optimal and syntactically correct SQL query to retrieve relevant information from the database schema based on the content of the email.

        Never query for all columns from a table. DO NOT use "SELECT *". You must query only the columns that are needed to answer the user question.
        Unless the user specifies in the question specific columns to obtain, query for at most 5 columns. The order of the results to return the most informative data in the database. The schema's primary key(s) must always be used in SELECT query.
        Always use 'LIMIT' to limit the out to 20 rows.
        If there are tables need to be joined, always use 'JOIN' to join tables.

        Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
        Pay attention to use date('now') function to get the current date, if the question involves "today".
    """
)

crew = Crew(
    agents=[database_query_generator_agent],
    tasks=[database_query_generator_task],
    verbose=2,
    process=Process.sequential
)

# Kickoff the process and print the output
output = crew.kickoff()
print(output)

# Responder agent modified to generate optimal queries for the database
# responder = Agent(
#     role="database query generator",
#     goal="Generate an optimal SQL query to retrieve relevant information from the database based on the provided email content. Be concise and accurate. Then run that query from your machine and print out the output",
#     backstory=f"You are an AI assistant whose job is to generate optimal SQL queries to retrieve relevant information from a database based on the content of the email. Then run that query from your machine and print out the output. Here is the database schema you will be working with:\n{schema}",
#     verbose=True,
#     allow_delegation=False,
#     llm=model
# )
# Task to generate a database query based on email content
# generate_query = Task(
#     description=f"Generate a database query for the email: '{email}'. Then run that query from your machine and print out the output",
#     agent=responder,
#     expected_output="An optimal SQL query to retrieve relevant information from the database based on the content of the email and result output"
# )


# Crew to run the task
# crew = Crew(
#     agents=[responder],
#     tasks=[generate_query],
#     verbose=2,
#     process=Process.sequential
# )

# Kickoff the process and print the output
# output = crew.kickoff()
# print(output)

    