import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState("");  // to store user input
  const [numberOfPeople, setNumberOfPeople] = useState(1); // to store number of people
  const [messages, setMessages] = useState([]);  // to store the conversation
  const [recipes, setRecipes] = useState([]); // to store the fetched recipes

  // Function to send the message to Flask
  const sendMessage = async () => {
    if (!input) return;  // Don't send empty messages

    // Add the user's message to the conversation
    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);
    
    // Send the input to the Flask backend
    const response = await fetch('http://127.0.0.1:5000/get-recipes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        groceries: input,  // Assuming input as a comma-separated list
        num_people: numberOfPeople  // Add number of servings to the request
      }),  
    });

    const data = await response.json();
    
    // Update recipes state with fetched recipes
    setRecipes(data.recipes);

    // Add the bot's response to the conversation
    setMessages([...newMessages, { text: "Here are your recipes!", sender: 'bot' }]);

    // Clear the input fields
    setInput("");
    setNumberOfPeople(1); // Reset servings to default
  };

  return (
    <div className="App">
      <h1>Chat with Recipe Bot</h1>

      {/* Servings input area */}
      <div style={{ marginBottom: '10px' }}>
        <label htmlFor="servings">Number of people:</label>
        <select
          id="servings"
          value={numberOfPeople}
          onChange={(e) => setNumberOfPeople(Number(e.target.value))}
          style={{ marginLeft: '5px' }}
        >
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
      </div>

      {/* Display recipes */}
      <div className="recipes">
          <pre>{recipes}</pre> {/* This will display the entire raw recipe text */}

      </div>

      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <div className="input-area">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter groceries (comma-separated) as: quantity item (e.g., 2 tomatoes, 1 lb ground beef)"
          rows="3"
          style={{ resize: 'vertical', width: '50%', padding: '10px', borderRadius: '8px', marginBottom: '10px' }} // Adding marginBottom to create space
        />
        
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
