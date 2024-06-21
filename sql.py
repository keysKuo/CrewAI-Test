from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from database_schema import schema

model = Ollama(model="llama3")

email = "listing popular ticket types last month"

# Responder agent modified to generate optimal queries for the database
responder = Agent(
    role="database query generator",
    goal="""
        1. Generate an optimal SQL query to retrieve relevant information from the database based on the provided email content.
        2. Run SQL query in given schema and print out the result by table
        3. Visualize with chart from the result
        * Focus on accuracy, if data isn't enough or you don't know, response with the answer that you don't know. Do not give wrong answer
     """,
    backstory=f"You are an AI assistant whose job is help client to optimize SQL queries to retrieve relevant information from a database, show the result and visualize it. Here is the database schema you will be working with:\n{schema}",
    verbose=True,
    allow_delegation=False,
    llm=model
)

# Task to generate a database query based on email content
generate_query = Task(
    description=f"Generate a database query for the email: '{email}', then show and visual it's result",
    agent=responder,
    expected_output="An optimal SQL query to retrieve relevant information from the database based on the content of the email, result and visualization"
)

# Crew to run the task
crew = Crew(
    agents=[responder],
    tasks=[generate_query],
    verbose=2,
    process=Process.sequential
)

# Kickoff the process and print the output
output = crew.kickoff()
print(output)
