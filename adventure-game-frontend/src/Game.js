import React, { useState } from 'react';
import axios from 'axios';
import { useQuery } from 'react-query';

function Game({ token }) {
  const [command, setCommand] = useState('');
  const headers = { Authorization: `Bearer ${token}` };
  
  const { data: gameState, refetch } = useQuery('gameState', () =>
    axios.get('/api/state/', { headers }).then(res => res.data)
  );

  const handleCommand = (e) => {
    e.preventDefault();
    // Parse and send the command to the backend
    // For simplicity, assume commands are in the format: action parameter
    const [action, ...params] = command.split(' ');
    let url = '';
    let data = {};
    if (action === 'move') {
      url = '/api/move/';
      data = { direction: params[0] };
    } else if (action === 'pick') {
      url = '/api/pick-up/';
      data = { item_name: params[1] }; // assuming command is 'pick up itemname'
    }
    // Send the request
    axios.post(url, data, { headers })
      .then(() => {
        refetch();
        setCommand('');
      })
      .catch(error => {
        console.error('Command failed:', error);
      });
  };

  if (!gameState) return <div>Loading...</div>;

  return (
    <div>
      <h2>{gameState.current_room.name}</h2>
      <p>{gameState.current_room.description}</p>
      <h3>Items in the room:</h3>
      <ul>
        {gameState.current_room.items.map(item => (
          <li key={item.name}>{item.name}: {item.description}</li>
        ))}
      </ul>
      <h3>Your Inventory:</h3>
      <ul>
        {gameState.inventory.map(item => (
          <li key={item.name}>{item.name}: {item.description}</li>
        ))}
      </ul>
      <form onSubmit={handleCommand}>
        <input value={command} onChange={e => setCommand(e.target.value)} placeholder="Enter command" />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
export default Game;
