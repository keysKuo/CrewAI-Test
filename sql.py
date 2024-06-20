from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from database_schema import schema

model = Ollama(model="llama3")

email = "listing popular ticket types last month"

# Responder agent modified to generate optimal queries for the database
responder = Agent(
    role="database query generator",
    goal="Generate an optimal SQL query to retrieve relevant information from the database based on the provided email content. Be concise and accurate. Then run that query from your machine and print out the output",
    backstory=f"You are an AI assistant whose job is to generate optimal SQL queries to retrieve relevant information from a database based on the content of the email. Then run that query from your machine and print out the output. Here is the database schema you will be working with:\n{schema}",
    verbose=True,
    allow_delegation=False,
    llm=model
)

# Task to generate a database query based on email content
generate_query = Task(
    description=f"Generate a database query for the email: '{email}'. Then run that query from your machine and print out the output",
    agent=responder,
    expected_output="An optimal SQL query to retrieve relevant information from the database based on the content of the email and result output"
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
