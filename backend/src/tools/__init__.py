
from langgraph.prebuilt import ToolNode
from src.tools.shell import shell_local, shell_docker
from src.tools.retrieval import retrieval_query, retrieval_add, retrieval_load
from src.tools.agent import agent_builder, available_tools
from src.tools.sql import sql_query_read, sql_query_write
from src.tools.browser import browser_use
tools = [       
    available_tools,
    # shell_local,
    shell_docker,
    retrieval_query,
    retrieval_add,
    retrieval_load,
    agent_builder,
    sql_query_read,
    sql_query_write,
    browser_use,
]
tool_node = ToolNode(tools)

###################################### UTILS ######################################
def collect_tools(selected_tools: list[str]):
    filtered_tools = [tool for tool in tools if tool.name in selected_tools]
    if len(filtered_tools) == 0:
        raise ValueError(f"No tools found by the names: {selected_tools.join(', ')}")
    return filtered_tools

