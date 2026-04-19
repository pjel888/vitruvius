#!/bin/bash
# Start the Vitruvius Graph API + Explorer in one terminal
# Usage: ./start-explorer.sh

cd "$(dirname "$0")"

# Check Neo4j is running
if ! curl -s http://localhost:7474 > /dev/null 2>&1; then
  echo "⚠️  Neo4j is not running. Start it with:"
  echo "   brew services start neo4j"
  exit 1
fi

echo "🚀 Starting Vitruvius Graph API on port 3000..."
cd api && NEO4J_PASS=password bun run index.ts &
API_PID=$!
cd ..

# Wait for API to be ready
echo "⏳ Waiting for API to start..."
for i in {1..30}; do
  if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ API ready!"
    break
  fi
  sleep 1
done

echo "🌐 Starting Explorer dev server on port 5173..."
cd explorer && bun run dev --host

# When explorer exits, kill the API
echo "🛑 Shutting down API..."
kill $API_PID 2>/dev/null
