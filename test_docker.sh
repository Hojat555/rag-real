#!/bin/bash
set -e

IMAGE="rag-real"
CONTAINER="rag-real-test"
PORT=8000

echo "=== 1. Building Docker image ==="
docker build -t $IMAGE .

echo ""
echo "=== 2. Starting container ==="
docker run -d --name $CONTAINER -p $PORT:$PORT $IMAGE
echo "Container started: $CONTAINER"

echo ""
echo "=== 3. Waiting for server to be ready ==="
for i in $(seq 1 30); do
    if curl -sf http://localhost:$PORT > /dev/null 2>&1; then
        echo "Server is ready (attempt $i)"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: Server did not start in time"
        docker logs $CONTAINER
        docker rm -f $CONTAINER
        exit 1
    fi
    sleep 2
done

echo ""
echo "=== 4. Testing GET / (health check) ==="
HEALTH=$(curl -sf http://localhost:$PORT)
echo "Response: $HEALTH"

echo ""
echo "=== 5. Testing POST /ask ==="
ANSWER=$(curl -sf -X POST http://localhost:$PORT/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What is RAG?"}')
echo "Response: $ANSWER"

echo ""
echo "=== 6. Cleaning up ==="
docker rm -f $CONTAINER
echo "Container removed"

echo ""
echo "=== All tests passed ==="
