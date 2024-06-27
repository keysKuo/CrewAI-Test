import os 
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
os.environ["OPENAI_MODEL_NAME"] ='llama3-70b-8192'  # Adjust based on available model
os.environ["OPENAI_API_KEY"] ='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'

from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from db_schema_2 import schema2
from Database import Database

# Define model
# model = Ollama(model="llama3")

def generate(question, schema, memory=""):
    generator = Agent(
        role="Database Query Specialist",
        goal="Generate SQL queries based on user input while adhering to strict guidelines.",
        backstory="""
            You are a database query specialist with extensive experience in creating precise and efficient SQL queries. Your expertise ensures that every query you generate adheres to the highest standards and rules set by the database schema.
        """,
        verbose=True,
        allow_delegation=False,   
    )

    # Define tasks
    generator_task = Task(
        description=f"""
            Schema: {schema}. 
            userQuestion: {question}
            pastResult: {memory}
            Generate an SQL query based on the userQuestion and pastResult while strictly adhering to the following rules:

            DO:
            - Use the exact name of tables and properties, they MUST be exactly the same in the query as in the schema.
            - ALWAYS look at the tables and tables' properties in the database schema to see what you can query.
            - Use only the column names you can see existing in the tables. 
            - Pay attention to which column is in which table.
            - Naming table must be unique.
            - ALWAYS use 'LIMIT' function to limit the out to 20 rows.
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
            - Duplicate table names.
            - Return any values beside the SQL query.
            Do NOT skip this step.
        """,
        agent=generator,
        expected_output="""
            An optimal and syntactically correct SQL query to retrieve relevant information from the database schema based on the content of the user input.
            Only the SQL query is returned. Nothing other than the SQL query is returned.
        """
    )

    # Define crew
    crew = Crew(
        agents=[generator],
        tasks=[generator_task],
        verbose=2,
        process=Process.sequential
    )

    # Kickoff the process and print the output
    output = crew.kickoff()
    past_result = output
    # print("* SQl Query: \n" + output)

    try:
        DB = Database("mysql")
        configs = {
            'host': 'localhost',
            'user': 'root',
            'password': '9952811',
            'database': 'ManageTest',
            'ssql': output
        }
        execute = DB.query(configs)

        # return test result
        d = dict()
        d['output'] = output
        d['execute'] = execute
        return d

        # print("* Records:")
        # for row in result:
        #     print(row)
    except Exception as e:
        print(e)

# past_result = ""

# user_input = str(input("Enter your request: "))
# if user_input == '.stop':
#     running = False
#     continue

# Define agents


    # Query Database for output
    


    