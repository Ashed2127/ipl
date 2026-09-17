#!/bin/bash
set -e

# Function to start Ollama in background
start_ollama() {
    echo "Starting Ollama service..."
    ollama serve > /tmp/ollama.log 2>&1 &
    OLLAMA_PID=$!
    
    # Wait for Ollama to be ready
    echo "Waiting for Ollama to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "✅ Ollama is ready"
            return 0
        fi
        sleep 1
    done
    
    echo "❌ Ollama failed to start"
    cat /tmp/ollama.log
    exit 1
}

# Function to check if model is available
check_model() {
    echo "Checking for Qwen model..."
    if curl -s http://localhost:11434/api/tags | grep -q "qwen2.5-coder:0.5b"; then
        echo "✅ Qwen model is available"
        return 0
    else
        echo "⚠️  Qwen model not found, downloading..."
        ollama pull qwen2.5-coder:0.5b
        echo "✅ Qwen model downloaded"
    fi
}

# Main execution
case "$1" in
    gateway)
        start_ollama
        check_model
        echo "Starting IPL Gateway on port 8000..."
        exec python -m cli serve
        ;;
    
    repl)
        start_ollama
        check_model
        echo "Starting IPL REPL..."
        exec python -m cli repl
        ;;
    
    run)
        start_ollama
        check_model
        shift
        echo "Running IPL script: $@"
        exec python -m cli run "$@"
        ;;
    
    shell)
        start_ollama
        check_model
        echo "Starting interactive shell..."
        exec /bin/bash
        ;;
    
    *)
        # Default: start both services
        start_ollama
        check_model
        echo "Starting IPL Gateway (default)..."
        exec python -m cli serve
        ;;
esac