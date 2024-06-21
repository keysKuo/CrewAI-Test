from langchain_community.llms import Ollama
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from database_connector import db 

llm = Ollama(model="llama3")

executor = create_sql_agent(llm, db = db, agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

result = executor.invoke("How many ticket types in database?");