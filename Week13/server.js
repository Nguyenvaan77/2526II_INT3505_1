require('dotenv').config();
const express = require('express');

const app = express();
app.use(express.json());

const authRoute = require('./routes/auth');
const userRoute = require('./routes/user');
const taskRoute = require('./routes/task');

app.use('/auth', authRoute.router);
app.use('/users', userRoute);
app.use('/tasks', taskRoute);

app.listen(3000, () => console.log('Server running'));