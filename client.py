import asyncio
import logging
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

# Set up logging to a common file
logging.basicConfig(filename='mcp_log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    # Load environment variables
    load_dotenv()

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_config_file('config.json')

    # Create LLM
    llm = ChatOpenAI(model="gpt-4o")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30, memory_enabled=True, verbose=True)

    # Interactive loop
    while True:
        user_query = input("\nEnter your query (or type 'exit' to quit): ")
        if user_query.strip().lower() == "exit":
            logging.info("Exiting client.")
            print("Exiting.")
            break
        try:
            logging.info(f"Sending query to server: {user_query}")
            result = await agent.run(user_query)
            logging.info(f"Received result from server: {result}")
            print(f"\n🧠 Result:\n{result}")
        except Exception as e:
            logging.error(f"Error during query: {e}")
            print(f"❌ Error during query: {e}")

if __name__ == "__main__":
    asyncio.run(main())
