from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import Literal, List, Dict, Any
from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import arxiv
import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
load_dotenv()
# You'll need to create this file with your prompts
# config/prompts.py should contain: PROMPT = "Based on the following document: {document}\n\nAnswer the user's question: {query}"

class ChatBot:
    def __init__(self, model_name: str = "gpt-4o-mini", memory_enabled: bool = True):
        """
        Initialize the chatbot with memory and tools
        
        Args:
            model_name: The OpenAI model to use
            memory_enabled: Whether to enable conversation memory
        """
        # Initialize LLM
        self.llm = ChatOpenAI(model=model_name)
        self.embedding = OpenAIEmbeddings()
        
        # Setup memory
        self.memory_enabled = memory_enabled
        if memory_enabled:
            self.memory = MemorySaver()
        else:
            self.memory = None
        
        # Initialize user context
        self.user_context = {}
        
        # Setup tools and workflow
        self.setup_tools()
        self.setup_workflow()
    
    def setup_tools(self):
        """Initialize all tools and bind them to the LLM"""
        
        @tool
        def arxiv_search(search_query: str, max_result: int = 3) -> str:
            """This tool is used to download top max_result research papers
            
            Args:
                search_query: It is the query search by the user
                max_result: Maximum number of papers to download (default: 3)
            
            Returns:
                str: Status message about the download and indexing
            """
            try:
                # Create papers directory if it doesn't exist
                papers_dir = Path("./papers")
                papers_dir.mkdir(exist_ok=True)
                
                # Clear existing papers
                for file in papers_dir.glob("*.pdf"):
                    file.unlink()
                
                client = arxiv.Client()
                
                # Search for papers
                search = arxiv.Search(
                    query=search_query,
                    max_results=max_result,
                    sort_by=arxiv.SortCriterion.SubmittedDate
                )
                
                results = client.results(search)
                all_results = list(results)
                
                if not all_results:
                    return "No papers found for the given search query."
                
                # Download papers
                for i, result in enumerate(all_results):
                    try:
                        result.download_pdf(dirpath="./papers", filename=f"paper_{i+1}.pdf")
                    except Exception as e:
                        print(f"Error downloading paper {i+1}: {e}")
                        continue
                
                # Load and process documents
                docs = []
                for filename in os.listdir("./papers"):
                    if filename.endswith(".pdf"):
                        file_path = os.path.join("./papers", filename)
                        try:
                            loader = PyPDFLoader(file_path)
                            doc = loader.load()
                            docs.extend(doc)
                        except Exception as e:
                            print(f"Error loading {filename}: {e}")
                            continue
                
                if not docs:
                    return "No documents could be loaded from the downloaded papers."
                
                # Split documents into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500, 
                    chunk_overlap=50
                )
                docs = text_splitter.split_documents(docs)
                
                # Create FAISS index
                db = FAISS.from_documents(docs, self.embedding)
                
                # Save index
                index_dir = "faiss_index"
                if os.path.exists(index_dir):
                    shutil.rmtree(index_dir)
                db.save_local(index_dir)
                
                return f"Successfully downloaded {len(all_results)} papers and created FAISS index with {len(docs)} chunks."
                
            except Exception as e:
                return f"Error in arxiv_search: {str(e)}"

        @tool
        def llm_summarizer(user_query: str) -> str:
            """This tool summarizes the PDFs based on user query
            
            Args:
                user_query: The user's question or query
                
            Returns:
                str: Summary based on the relevant documents
            """
            try:
                # Check if index exists
                index_dir = "faiss_index"
                if not os.path.exists(index_dir):
                    return "No FAISS index found. Please search for papers first using arxiv_search."
                
                # Load FAISS index
                db = FAISS.load_local(index_dir, self.embedding, allow_dangerous_deserialization=True)
                
                # Search for relevant documents
                results = db.similarity_search(user_query, k=3)
                
                if not results:
                    return "No relevant documents found for your query."
                
                # Create context from results
                context = "\n\n".join([doc.page_content for doc in results])
                
                # Create prompt
                prompt = f"""Based on the following research paper excerpts, please provide a comprehensive answer to the user's question.

Research Paper Excerpts:
{context}

User Question: {user_query}

Please provide a detailed and accurate answer based on the research papers:"""
                
                response = self.llm.invoke(prompt)
                return response.content
                
            except Exception as e:
                return f"Error in llm_summarizer: {str(e)}"
        
        # Store tools
        self.tools = [arxiv_search, llm_summarizer]
        self.tool_node = ToolNode(tools=self.tools)
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def call_model(self, state: MessagesState):
        """Call the LLM model with the current state"""
        messages = state['messages']
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def router_function(self, state: MessagesState) -> Literal["tools", "__end__"]:
        """Route to tools or end based on the last message"""
        messages = state['messages']
        last_message = messages[-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return "__end__"
    
    def setup_workflow(self):
        """Setup the workflow graph"""
        workflow = StateGraph(MessagesState)
        
        # Add nodes
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tool_node)
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            self.router_function,
            {"tools": "tools", "__end__": END}
        )
        workflow.add_edge("tools", "agent")
        
        # Compile with or without memory
        if self.memory_enabled and self.memory:
            self.app = workflow.compile(checkpointer=self.memory)
        else:
            self.app = workflow.compile()
    
    def chat(self, message: str, thread_id: str = "default") -> str:
        """
        Chat with the bot with memory support
        
        Args:
            message: User message
            thread_id: Thread ID for conversation memory
        """
        try:
            config = {"configurable": {"thread_id": thread_id}} if self.memory_enabled else {}
            
            # Create human message
            human_message = HumanMessage(content=message)
            
            # Invoke the workflow
            response = self.app.invoke(
                {"messages": [human_message]},
                config=config
            )
            
            # Extract the last AI message
            if response and 'messages' in response:
                last_message = response['messages'][-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
                else:
                    return str(last_message)
            
            return "I couldn't generate a response. Please try again."
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_conversation_history(self, thread_id: str = "default") -> List[Dict[str, Any]]:
        """
        Get conversation history for a thread
        
        Args:
            thread_id: Thread ID to get history for
        """
        if not self.memory_enabled:
            return []
        
        try:
            config = {"configurable": {"thread_id": thread_id}}
            state = self.app.get_state(config)
            
            history = []
            if state and hasattr(state, 'values') and 'messages' in state.values:
                for msg in state.values['messages']:
                    if isinstance(msg, HumanMessage):
                        history.append({"role": "user", "content": msg.content})
                    elif isinstance(msg, AIMessage):
                        history.append({"role": "assistant", "content": msg.content})
            
            return history
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def set_user_context(self, user_id: str, context: Dict[str, Any]):
        """Set user context for personalization"""
        self.user_context[user_id] = context
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user context"""
        return self.user_context.get(user_id, {})