const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

const router = express.Router();

const users = [];
let refreshTokens = [];

// REGISTER
router.post('/register', async (req, res) => {
    const { username, password, role } = req.body;

    const hashed = await bcrypt.hash(password, 10);

    users.push({
        id: uuidv4(),
        username,
        password: hashed,
        role: role || 'customer'
    });

    res.json({ message: 'Registered' });
});

// LOGIN
router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    const user = users.find(u => u.username === username);
    if (!user) return res.sendStatus(401);

    const valid = await bcrypt.compare(password, user.password);
    if (!valid) return res.sendStatus(403);

    const scopes = user.role === 'admin'
        ? ['read:all', 'delete:user']
        : ['read:task', 'write:task'];

    const accessToken = jwt.sign(
        { id: user.id, role: user.role, scopes },
        process.env.ACCESS_TOKEN_SECRET,
        { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
        { id: user.id },
        process.env.REFRESH_TOKEN_SECRET,
        { expiresIn: '7d' }
    );

    refreshTokens.push(refreshToken);

    res.json({ accessToken, refreshToken });
});

// REFRESH TOKEN
router.post('/token', (req, res) => {
    const { token } = req.body;
    if (!token) return res.sendStatus(401);

    if (!refreshTokens.includes(token)) return res.sendStatus(403);

    jwt.verify(token, process.env.REFRESH_TOKEN_SECRET, (err, user) => {
        if (err) return res.sendStatus(403);

        const accessToken = jwt.sign(
            { id: user.id },
            process.env.ACCESS_TOKEN_SECRET,
            { expiresIn: '15m' }
        );

        res.json({ accessToken });
    });
});

module.exports = { router, users, refreshTokens };