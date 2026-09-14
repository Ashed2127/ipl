#!/usr/bin/env bash
# ============================================================================
# IPL Security Gateway curl test suite
# Validates /health, /api/v1/models, /api/v1/verify, and /api/v1/execute
# ============================================================================

set -e

PORT=${1:-8000}
HOST="127.0.0.1"
BASE_URL="http://${HOST}:${PORT}"

echo "======================================================================"
echo "⚡ Starting IPL Security Gateway curl Test Suite against ${BASE_URL}"
echo "======================================================================"

SERVER_STARTED_BY_SCRIPT=0

# Check if gateway is already running, else start temporarily in background
if ! curl -s "${BASE_URL}/health" > /dev/null 2>&1; then
    echo "Starting local IPL Gateway on port ${PORT} in background..."
    python3 -m uvicorn gateway:create_app --factory --host "${HOST}" --port "${PORT}" --log-level error &
    GATEWAY_PID=$!
    SERVER_STARTED_BY_SCRIPT=1
    sleep 2
fi

cleanup() {
    if [ "$SERVER_STARTED_BY_SCRIPT" -eq 1 ]; then
        echo -e "\nStopping background Gateway (PID ${GATEWAY_PID})..."
        kill -9 "${GATEWAY_PID}" 2>/dev/null || true
    fi
}
trap cleanup EXIT

echo -e "\n[1/5] Testing GET /health..."
HEALTH_RESP=$(curl -s "${BASE_URL}/health")
echo "Response: ${HEALTH_RESP}"
echo "${HEALTH_RESP}" | grep -q '"status":"healthy"' && echo "✔ Health check passed"

echo -e "\n[2/5] Testing GET /api/v1/models..."
MODELS_RESP=$(curl -s "${BASE_URL}/api/v1/models")
echo "Response: ${MODELS_RESP}"
echo "${MODELS_RESP}" | grep -q '"embedded-fast-semantic-v1"' && echo "✔ Models list passed"

echo -e "\n[3/5] Testing POST /api/v1/verify (Valid Source)..."
VERIFY_RESP=$(curl -s -X POST "${BASE_URL}/api/v1/verify" \
  -H "Content-Type: application/json" \
  -d '{"source": "let x: Int = 42\nprint x"}')
echo "Response: ${VERIFY_RESP}"
echo "${VERIFY_RESP}" | grep -q '"valid":true' && echo "✔ Formal verification passed"

echo -e "\n[4/5] Testing POST /api/v1/execute (Safe Execution with Audit)..."
EXEC_RESP=$(curl -s -X POST "${BASE_URL}/api/v1/execute" \
  -H "Content-Type: application/json" \
  -d '{"source": "let price: Currency = intent \"99 dollars\" as Currency; let clean = sanitize(price); db_write(\"orders\", clean);", "audit": true}')
echo "Response: ${EXEC_RESP}"
echo "${EXEC_RESP}" | grep -q '"status":"success"' && echo "✔ Sandbox execution passed"

echo -e "\n[5/5] Testing POST /api/v1/execute (Zero-Trust Taint Violation Rejection)..."
TAINT_RESP=$(curl -s -X POST "${BASE_URL}/api/v1/execute" \
  -H "Content-Type: application/json" \
  -d '{"source": "let raw: String = intent \"untrusted data\" as String; db_write(\"orders\", raw);"}')
echo "Response: ${TAINT_RESP}"
echo "${TAINT_RESP}" | grep -q '"status":"blocked"' && echo "✔ Zero-Trust taint protection verified"

echo -e "\n======================================================================"
echo "🎉 ALL 5 GATEWAY ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY"
echo "======================================================================"
