import vertexai
from vertexai.preview import rag

from day4_grounding.constants import PROJECT, LOCATION

vertexai.init(project=PROJECT, location=LOCATION)
for c in rag.list_corpora():
    print(c.name, c.display_name)
