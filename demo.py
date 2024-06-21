from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from database_schema import schema
from database_connector import db
import re
# Define model
model = Ollama(model="llama3")
running = True

while(running):
    # Define user input, user input must not be general
    user_input = str(input())

    if(user_input == '.stop'):
        running = False

    generator= Agent(
        role="Database Query Generator",
        goal="Generate optimal and syntactically correct SQL queries based on the given schema and user input specifications. Be concise and accurate. Do NOT make up information.",
        backstory="""
            You are an SQL expert.
            You're responsible for creating optimal and syntactically correct SQL queries based on a given database schemas.
            You must use exactly the column names in each table of the database.
        """,
        verbose=True,
        allow_delegation=False,
        llm=model
    )

    generator_task = Task(
        description=f"""You work on this database schema: {schema}. Generate optimimal and syntactically correct SQL queries based on user specifications {user_input}.
        
            DO:
            - Use the exact name of tables and properties, they MUST be exactly the same in the query as in the schema.
            - Naming table must be unique.
            - ALWAYS look at the tables and tables' properties in the database schema to see what you can query.
            - ALWAYS use 'LIMIT' function to limit the out to 20 rows.
            - Use only the column names you can see existing in the tables. Pay attention to which column is in which table.
            - Use function to get the current date, if the question involves "today".
            - If there are tables need to be joined, you always use 'JOIN' function to join tables.
            - Query only the columns that are needed to answer the user question.
            - Unless the user specifies in the question specific columns to obtain, display for at most 5 significant columns. 
            - The order of the results to return the most informative data in the database. The schema's primary key(s) must always be used in SELECT query.
            - When 'GROUP BY', specifically check if enough essential columns
            - Return SQL query ONLY.
            Do NOT skip this step.

            Do NOT:
            - Query for columns or properties that do not exist.
            - Make or generate any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
            - Use SQL subquery.
            - Change the table's name.
            - Use columns that not belong to table
            - Use SELECT *.
            - Use 'TOP 1'.
            - Duplicate table name with 'AS'.
            Do NOT skip this step.
        """,
        agent=generator,
        expected_output="""
            An optimal and syntactically correct SQL query to retrieve relevant information from the database schema based on the content of the input.
            Return as markdown.
        """
    )

    crew = Crew(
        agents=[generator],
        tasks=[generator_task],
        verbose=2,
        process=Process.sequential
    )

    # Kickoff the process and print the output
    output = crew.kickoff()

    try:
        sql_query = ""
        pattern_1 = re.compile(r'```sql(.*?)```', re.DOTALL)
        pattern_2 = re.compile(r'```(.*?)```', re.DOTALL)
        matches_1 = pattern_1.findall(output)
        matches_2 = pattern_2.findall(output)
        
        
        if len(matches_1) != 0:
            sql_query = matches_1[0]  
        elif len(matches_2) != 0:
            sql_query = matches_2[0]
        else:
            print("> No value returns")

        final = db.run(sql_query)
        print(final)
    except Exception  as e:
        print("> Please describe your request more specifically")
    finally:
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

    