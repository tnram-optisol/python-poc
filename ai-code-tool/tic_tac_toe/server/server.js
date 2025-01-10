const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

let clients = []; // Keep track of connected clients

// Broadcast function to send a message to all clients
function broadcast(message) {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(message));
    }
  });
}

wss.on('connection', (ws) => {
  // Add new client to the list
  clients.push(ws);

  // Notify the first player that it's their turn
  if (clients.length === 2) {
    clients[0].send(JSON.stringify({ type: 'start', player: 'X' }));
    clients[1].send(JSON.stringify({ type: 'start', player: 'O' }));
  }

  // Listen for messages from clients
  ws.on('message', (message) => {
    const data = JSON.parse(message);

    // If a player made a move, broadcast it to the other player
    if (data.type === 'move') {
      broadcast(data);
    }

    // If a player wins, notify both players
    if (data.type === 'win') {
      broadcast(data);
    }
  });

  // Remove client when they disconnect
  ws.on('close', () => {
    clients = clients.filter(client => client !== ws);
  });
});

console.log('WebSocket server is running on ws://localhost:8080');