# Scout Agent - LangGraph-based Chatbot

This is a Streamlit-based chatbot application that uses LangGraph for conversation management and memory handling. The application provides an interactive chat interface with user profile management and conversation history tracking.

## Features

- 🤖 Interactive chat interface with memory-enabled conversations
- 👤 User profile management
- 📚 Conversation history tracking
- 🧹 Memory clearing functionality
- 💡 Context-aware responses
- 🔄 Persistent conversation threads

## Technical Implementation

### Core Components

1. **ChatBot Class (agent_langgraph.py)**
   - Implements conversation management using LangGraph
   - Handles memory persistence and retrieval
   - Manages user context and conversation threads

2. **Streamlit Interface (app.py)**
   - Provides the user interface
   - Manages session state
   - Handles user interactions

### Key Features Implementation

#### Conversation Management
- Uses UUID for unique thread identification
- Maintains separate conversation threads for different chat sessions
- Implements memory-enabled conversations for context retention

#### User Context
- Stores user profile information (name, company, email)
- Associates context with specific user IDs
- Persists user preferences across sessions

#### Memory Handling
- Implements conversation history storage
- Provides memory clearing functionality
- Tracks message count for interaction insights

## Usage

1. **Starting the Application**
   ```bash
   cd additional
   streamlit run app.py
   ```

2. **User Profile Setup**
   - Access the sidebar to set your profile information
   - Update profile details as needed
   - Profile information is used to personalize responses

3. **Chat Interaction**
   - Type messages in the input field
   - Click "Send" to interact with the bot
   - View conversation history in the sidebar
   - Clear chat memory when needed

4. **Features**
   - Profile Management: Update user information
   - Memory Management: Clear chat history
   - History Viewing: Access past conversations
   - Quick Tips: Receive periodic interaction suggestions

## Technical Requirements

- Python 3.x
- Streamlit
- LangGraph
- UUID

## Dependencies

```python
streamlit
langgraph
uuid
```

## Architecture

The application follows a modular architecture:

```
additional/
├── app.py              # Streamlit interface
├── agent_langgraph.py  # LangGraph implementation
└── README.md          # Documentation
```

## Best Practices Implemented

1. **Session Management**
   - Uses Streamlit's session state for persistence
   - Implements unique thread IDs for conversation tracking
   - Maintains user context across sessions

2. **User Experience**
   - Clean, intuitive interface
   - Responsive feedback
   - Clear error handling
   - Interactive elements

3. **Code Organization**
   - Separation of concerns
   - Modular design
   - Clear documentation
   - Maintainable structure

## Future Enhancements

1. Add support for multiple conversation threads
2. Implement advanced memory management
3. Add export functionality for conversation history
4. Integrate with external APIs for enhanced capabilities
5. Add authentication and user management

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 