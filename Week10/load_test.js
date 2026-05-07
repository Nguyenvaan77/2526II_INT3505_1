import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '5s', target: 10 },  // tăng tải
    { duration: '10s', target: 30 }, // load ổn định
    { duration: '5s', target: 0 }    // giảm tải
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% request < 500ms
    http_req_failed: ['rate<0.01'],   // lỗi < 1%
  }
};

const BASE_URL = 'http://host.docker.internal:5000';

export default function () {

  // 1. Health check
  let health = http.get(`${BASE_URL}/health`);
  check(health, {
    'health 200': (r) => r.status === 200,
  });

  // 2. Create user
  let userPayload = JSON.stringify({
    name: `User_${__VU}_${__ITER}`
  });

  let userRes = http.post(`${BASE_URL}/users`, userPayload, {
    headers: { 'Content-Type': 'application/json' }
  });

  check(userRes, {
    'create user success': (r) => r.status === 201,
  });

  let userId = undefined;
  try {
    userId = JSON.parse(userRes.body).id;
  } catch (e) {}

  // 3. Get users
  let users = http.get(`${BASE_URL}/users`);
  check(users, {
    'get users 200': (r) => r.status === 200,
  });

  // 4. Create task (nếu có userId)
  if (userId) {
    let taskPayload = JSON.stringify({
      title: `Task_${__VU}_${__ITER}`,
      user_id: userId
    });

    let taskRes = http.post(`${BASE_URL}/tasks`, taskPayload, {
      headers: { 'Content-Type': 'application/json' }
    });

    check(taskRes, {
      'create task success': (r) => r.status === 201,
    });
  }

  // 5. Get tasks
  let tasks = http.get(`${BASE_URL}/tasks`);
  check(tasks, {
    'get tasks 200': (r) => r.status === 200,
  });

  sleep(1);
}