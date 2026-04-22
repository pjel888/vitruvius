#!/bin/bash
# Start the Vitruvius Graph API + Explorer in one terminal
# Usage: ./start-explorer.sh

set -e
cd "$(dirname "$0")"
PROJECT_ROOT="$(pwd)"

# Check Neo4j is running
if ! curl -s http://localhost:7474 > /dev/null 2>&1; then
  echo "⚠️  Neo4j is not running. Start it with:"
  echo "   brew services start neo4j"
  exit 1
fi

# Kill any existing API on port 3000
EXISTING_API=$(lsof -ti:3000 2>/dev/null || true)
if [ -n "$EXISTING_API" ]; then
  echo "🧹 Cleaning up existing API on port 3000..."
  kill "$EXISTING_API" 2>/dev/null || true
  sleep 1
fi

echo "🚀 Starting Vitruvius Graph API on port 3000..."
cd "$PROJECT_ROOT/api"
NEO4J_PASS="${NEO4J_PASS:-password}" bun run index.ts &
API_PID=$!
cd "$PROJECT_ROOT"

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
cd "$PROJECT_ROOT/explorer"
bun run dev --host

# When explorer exits, kill the API
echo "🛑 Shutting down API..."
kill $API_PID 2>/dev/null || true
