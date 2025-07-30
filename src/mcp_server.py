import os
import logging
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
from ansible_template import run_ansible_template

logger = logging.getLogger(__name__)

ENV_MCP_PORT = "MCP_PORT"
ENV_LOG_LEVEL = "LOG_LEVEL"

mcp = FastMCP("Ansible MCP")
sse_app = mcp.sse_app()

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool(
    annotations={
        "title": "Run's the demo job template.",
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def run_demo_job_template():
    """Runs the Demo Job Template """
    template_name = "Demo Job Template"
    run_ansible_template(template_name)


@mcp.tool(
    annotations={
        "title": "Run's a job template with the specified name as provided by the user in Ansible Automation Platform.",
        "readOnlyHint": False,
        "openWorldHint": True,
    }
)
def run_job_template_in_ansible(template_name: str):
    """Runs the specified Job Template in Ansible Automation Platform """
    run_ansible_template(template_name)



@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


@sse_app.route("/health")
async def health_check(request):
    """ Health check endpoint for the MCP Server. """

    return JSONResponse({"status": "ok"})


def main():
    """ Application Entry Point """
    port = 8080
    if ENV_MCP_PORT in os.environ:
        port = int(os.environ[ENV_MCP_PORT])
    print ("Port: ", port)

    log_level = "info"
    if ENV_LOG_LEVEL in os.environ:
        log_level = os.environ[ENV_LOG_LEVEL]
    print ("Log Level: ", log_level)

    uvicorn.run(sse_app, host="0.0.0.0", port=port, log_level=log_level)


if __name__ == "__main__":
    main()
