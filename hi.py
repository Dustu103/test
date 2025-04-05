from flask import Flask, redirect, request, session, jsonify
from Main_agent import compile_main_agent_graph
main_agent = compile_main_agent_graph()
from langchain_core.runnables import RunnableConfig

app = Flask(__name__)

@app.route("/")
def home():
    print("✅ / route hit")
    return "✅ Backend working"

@app.route("/query", methods=["POST"])
def query():
    print("🔍 Querying main agent")
    data = request.json
    input_data = data.get("input")
    if not input_data:
        return jsonify({"error": "No input provided"}), 400

    # Define configuration
    config = RunnableConfig(
        configurable={"user_id": "user_12345"}
    )
    # Run the main agent with the provided input
    result = main_agent.invoke(input_data, run_config=RunnableConfig(max_retries=3))
    
    # Return the result as JSON
    return jsonify({"result": result})