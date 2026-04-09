const express = require('express');
const { authenticateToken } = require('../middleware/auth');
const { authorizeRole } = require('../middleware/role');

const router = express.Router();
const { users } = require('./auth');

// GET ALL USERS
router.get('/', authenticateToken, authorizeRole('admin'), (req, res) => {
    res.json(users);
});

// DELETE USER
router.delete('/:id', authenticateToken, authorizeRole('admin'), (req, res) => {
    const index = users.findIndex(u => u.id === req.params.id);
    if (index === -1) return res.sendStatus(404);

    users.splice(index, 1);
    res.json({ message: 'User deleted' });
});

module.exports = router;