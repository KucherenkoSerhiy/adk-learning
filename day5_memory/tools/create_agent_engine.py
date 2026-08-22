import vertexai

from constants import PROJECT, LOCATION

client = vertexai.Client(project=PROJECT, location=LOCATION)
memory_bank = client.agent_engines.create()
agent_engine_id = memory_bank.api_resource.name.split("/")[-1]
print("Agent Engine ID:", agent_engine_id)

