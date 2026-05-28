const express = require('express');
const { authenticateToken } = require('../middleware/auth');
const { v4: uuidv4 } = require('uuid');

const router = express.Router();

let tasks = [];

// CREATE TASK
router.post('/', authenticateToken, (req, res) => {
    const task = {
        id: uuidv4(),
        title: req.body.title,
        ownerId: req.user.id
    };

    tasks.push(task);
    res.json(task);
});

// GET MY TASKS
router.get('/', authenticateToken, (req, res) => {
    const myTasks = tasks.filter(t => t.ownerId === req.user.id);
    res.json(myTasks);
});

// UPDATE TASK
router.put('/:id', authenticateToken, (req, res) => {
    const task = tasks.find(t => t.id === req.params.id);

    if (!task) return res.sendStatus(404);
    if (task.ownerId !== req.user.id) return res.sendStatus(403);

    task.title = req.body.title;
    res.json(task);
});

// DELETE TASK
router.delete('/:id', authenticateToken, (req, res) => {
    const index = tasks.findIndex(t => t.id === req.params.id);

    if (index === -1) return res.sendStatus(404);
    if (tasks[index].ownerId !== req.user.id) return res.sendStatus(403);

    tasks.splice(index, 1);
    res.json({ message: 'Deleted' });
});

module.exports = router;