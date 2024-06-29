from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from Database import DatabaseManager
import re

# from db_schema_2 import schema2

# Define model
model = Ollama(model="llama3")
running = True;
past_result = ""

def generate(question, schema, memory=""):
    generator = Agent(
        role="Database Query Specialist",
        goal="Generate SQL queries based on user input while adhering to strict guidelines.",
        backstory="""
            You are a database query specialist with extensive experience in creating precise and efficient SQL queries. Your expertise ensures that every query you generate adheres to the highest standards and rules set by the database schema.
        """,
        verbose=True,
        allow_delegation=False,
        llm=model 
    )

    # Define tasks
    generator_task = Task(
        description=f"""
            Schema: {schema}. 
            userQuestion: {question}
            pastResult: {memory}
            Generate an SQL query based on the userQuestion and pastResult while strictly adhering to the following rules:

            - Use the exact name of tables and properties, they MUST be exactly the same in the query as in the schema.
            - ONLY use the tables and tables' properties in the database schema to see what you can query.
            - ONLY use the column names which existing in the tables. 
            - Check exactly whether columns name is belong to tables.
            - Naming table must be unique.
            - ALWAYS use 'LIMIT' function to limit for instance 20 rows.
            - Use function to get the current date, if the question involves "today".
            - If there are tables need to be joined, you always use 'JOIN' function to join tables.
            - Query ONLY the columns that are needed to answer the user question.
            - Unless the user specifies in the question specific columns to obtain, display for at most 5 significant columns. 
            - The ORDER of the results to return the most informative data in the database. The schema's primary key(s) must always be used in SELECT query.
            - When 'GROUP BY', specifically check if enough essential columns
            - Reply as Vietnamese if userQuestion use Vietnamese language
            Do NOT skip this step

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
            Output as markdown format explain how to query work and an optimal, syntactically correct SQL query to retrieve relevant information from the database schema based on the content of the userQuestion
        """
    )

    extractor = Agent(
        role = "SQL Query Extractor",
        goal = """
            To extract only SQL query code block from a passage or text while adhering to strict guidelines.
        """,
        backstory = """
            You are an SQL queries extractor expert and specialist.
            You are responsible for extracting ONLY SQL queries code block from a passage or text.
            You must extract SQL queries and place it in this format ```sql ```.
        """,
        verbose=True,
        allow_delegation=False,
        llm=model
    )

    extractor_task = Task(
        description = """
            Strictly adhering to the following rules:
                - Receive the output from 'generator' agent and extract ONLY the SQL queries code block.
                - Format the SQL queries code block to format ```sql ``` of markdown.
                Do NOT skip this step.
        """,
        agent=extractor,
        expected_output = """
            Explaination of the query,
            SQL language markdown code get from 'generator'.
        """,
        context = [generator_task]
    )

    # Define crew
    crew = Crew(
        agents=[generator, extractor],
        tasks=[generator_task, extractor_task],
        verbose=2,
        process=Process.sequential
    )

    # Kickoff the process and print the output
    output = crew.kickoff()
    # past_result = output
    # print("* SQl Query: \n" + output)

    sql_query = ""
    pattern_1 = re.compile(r'```sql(.*?)```', re.DOTALL)
    matches_1 = pattern_1.findall(output)
    if len(matches_1) != 0:
        sql_query = matches_1[0]  
    

    try:
        DB = DatabaseManager("mysql")
        DB.setup(schema)
        result, columns = DB.query(sql_query)

        # return test result
        d = dict()
        d['output'] = output
        d['execute'] = result
        d['columns'] = columns
        return d

    except Exception as e:
        print("Lỗi ở local: " + str(e))
        d = dict()
        d['output'] = output
        return d
