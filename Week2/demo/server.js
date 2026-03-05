const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const dbPath = path.join(__dirname, 'database', 'db.json');

// Middleware
app.use(cors());
app.use(express.json());

// Helper functions
const readDatabase = () => {
  try {
    const data = fs.readFileSync(dbPath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return { users: [] };
  }
};

const writeDatabase = (data) => {
  fs.writeFileSync(dbPath, JSON.stringify(data, null, 2));
};

// Routes

// GET all users
app.get('/api/users', (req, res) => {
  try {
    const db = readDatabase();
    res.json(db.users || []);
  } catch (error) {
    res.status(500).json({ message: 'Error reading users' });
  }
});

// GET user by ID
app.get('/api/users/:id', (req, res) => {
  try {
    const db = readDatabase();
    const user = (db.users || []).find(user => user.id === req.params.id);
    
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    
    res.json(user);
  } catch (error) {
    res.status(500).json({ message: 'Error reading user' });
  }
});

// POST - Create new user
app.post('/api/users', (req, res) => {
  try {
    const { name, email, phoneNumber } = req.body;
    
    if (!name || !email) {
      return res.status(400).json({ message: 'Name and email are required' });
    }
    
    const db = readDatabase();
    const maxId = Math.max(...(db.users || []).map(u => parseInt(u.id) || 0), 0);
    
    const newUser = {
      id: String(maxId + 1),
      name,
      email,
      phoneNumber: phoneNumber || ''
    };
    
    if (!db.users) {
      db.users = [];
    }
    
    db.users.push(newUser);
    writeDatabase(db);
    
    res.status(201).json(newUser);
  } catch (error) {
    res.status(500).json({ message: 'Error creating user' });
  }
});

// PUT - Update user
app.put('/api/users/:id', (req, res) => {
  try {
    const { name, email, phoneNumber } = req.body;
    const db = readDatabase();
    const userIndex = (db.users || []).findIndex(user => user.id === req.params.id);
    
    if (userIndex === -1) {
      return res.status(404).json({ message: 'User not found' });
    }

    if (!name || !email) {
      return res.status(400).json({ message: 'Name and email are required' });
    }
    
    if (name) {
      db.users[userIndex].name = name;
    }
    if (email) {
      db.users[userIndex].email = email;
    }
    if (phoneNumber !== undefined) {
      db.users[userIndex].phoneNumber = phoneNumber;
    }
    
    writeDatabase(db);
    res.json(db.users[userIndex]);
  } catch (error) {
    res.status(500).json({ message: 'Error updating user' });
  }
});

// DELETE - Delete user
app.delete('/api/users/:id', (req, res) => {
  try {
    const db = readDatabase();
    const userIndex = (db.users || []).findIndex(user => user.id === req.params.id);
    
    if (userIndex === -1) {
      return res.status(404).json({ message: 'User not found' });
    }
    
    const deletedUser = db.users.splice(userIndex, 1)[0];
    writeDatabase(db);
    
    res.json({ message: 'User deleted', user: deletedUser });
  } catch (error) {
    res.status(500).json({ message: 'Error deleting user' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Users API Server is running on http://localhost:${PORT}`);
  console.log(`\n📝 Available Endpoints:`);
  console.log(`   GET    /api/users       - Get all users`);
  console.log(`   GET    /api/users/:id   - Get user by ID`);
  console.log(`   POST   /api/users       - Create new user`);
  console.log(`   PUT    /api/users/:id   - Update user`);
  console.log(`   DELETE /api/users/:id   - Delete user`);
  console.log(`   GET    /api/health      - Health check\n`);
});
