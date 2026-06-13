#!/bin/bash

echo "Starting backend on port 8001..."
cd backend || exit
source venv/bin/activate
python manage.py runserver 8001 &
BACKEND_PID=$!
cd ..

echo "Starting frontend on port 3000..."
cd frontend || exit
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "==================================================="
echo "Servers are running:"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8001"
echo "==================================================="
echo "Press Ctrl+C to stop both servers."

# Trap Ctrl+C (SIGINT) and kill both child processes
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" EXIT INT TERM

# Wait for both processes to keep the script running
wait
