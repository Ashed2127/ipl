#!/bin/bash
# IPL Installation Script with Optional Ollama Integration
# This script provides a one-command installation experience

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  IPL Installation Script${NC}"
echo -e "${BLUE}  Intelligent Programming Language${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        OS="windows"
    else
        echo -e "${RED}Unsupported OS: $OSTYPE${NC}"
        exit 1
    fi
    echo -e "${GREEN}Detected OS: $OS${NC}"
}

# Function to check Python installation
check_python() {
    echo -e "${BLUE}Checking Python installation...${NC}"
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo -e "${GREEN}Python $PYTHON_VERSION found${NC}"
    else
        echo -e "${RED}Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
        exit 1
    fi
}

# Function to install IPL
install_ipl() {
    echo -e "${BLUE}Installing IPL...${NC}"
    pip3 install -e .
    echo -e "${GREEN}✅ IPL installed successfully${NC}"
}

# Function to install Ollama
install_ollama() {
    echo -e "${BLUE}Installing Ollama...${NC}"
    
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo -e "${YELLOW}Please install Homebrew first, then run: brew install ollama${NC}"
            return 1
        fi
    elif [[ "$OS" == "windows" ]]; then
        echo -e "${YELLOW}Please download Ollama from https://ollama.com/download${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Ollama installed successfully${NC}"
}

# Function to start Ollama service
start_ollama() {
    echo -e "${BLUE}Starting Ollama service...${NC}"
    
    # Start Ollama in background
    ollama serve > /tmp/ollama.log 2>&1 &
    OLLAMA_PID=$!
    
    # Wait for Ollama to be ready
    echo "Waiting for Ollama to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Ollama service is running${NC}"
            return 0
        fi
        sleep 1
    done
    
    echo -e "${RED}❌ Ollama failed to start${NC}"
    cat /tmp/ollama.log
    return 1
}

# Function to download Qwen model
download_qwen() {
    echo -e "${BLUE}Checking for Qwen model...${NC}"
    
    if curl -s http://localhost:11434/api/tags | grep -q "qwen2.5-coder:0.5b"; then
        echo -e "${GREEN}✅ Qwen model already available${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}Downloading Qwen2.5-Coder:0.5b model (this may take a few minutes)...${NC}"
    ollama pull qwen2.5-coder:0.5b
    echo -e "${GREEN}✅ Qwen model downloaded successfully${NC}"
}

# Function to verify installation
verify_installation() {
    echo -e "${BLUE}Verifying installation...${NC}"
    
    # Test IPL
    if python3 -m cli --version &> /dev/null; then
        echo -e "${GREEN}✅ IPL is working${NC}"
    else
        echo -e "${RED}❌ IPL verification failed${NC}"
        return 1
    fi
    
    # Test Ollama if installed
    if command -v ollama &> /dev/null; then
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Ollama is working${NC}"
        else
            echo -e "${YELLOW}⚠️  Ollama is installed but not running${NC}"
        fi
    fi
}

# Main installation flow
main() {
    detect_os
    check_python
    
    # Ask user about Ollama installation
    echo -e "\n${YELLOW}Do you want to install Ollama with Qwen model for advanced AI features?${NC}"
    echo -e "${YELLOW}This enables deep reasoning capabilities (requires ~400MB download).${NC}"
    echo -e "${YELLOW}Note: IPL works perfectly without Ollama using built-in intelligence.${NC}"
    read -p "Install Ollama? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        INSTALL_OLLAMA=true
    else
        INSTALL_OLLAMA=false
        echo -e "${BLUE}Skipping Ollama installation (using embedded intelligence)${NC}"
    fi
    
    # Install IPL
    install_ipl
    
    # Install Ollama if requested
    if [[ "$INSTALL_OLLAMA" == true ]]; then
        if command -v ollama &> /dev/null; then
            echo -e "${GREEN}Ollama is already installed${NC}"
        else
            install_ollama
        fi
        
        start_ollama
        download_qwen
    fi
    
    # Verify installation
    verify_installation
    
    # Print usage instructions
    echo -e "\n${GREEN}================================================${NC}"
    echo -e "${GREEN}  Installation Complete!${NC}"
    echo -e "${GREEN}================================================${NC}\n"
    
    echo -e "${BLUE}Quick Start:${NC}"
    echo -e "  Run IPL script:  ${YELLOW}ipl run examples/01_intelligent_variables.ipl${NC}"
    echo -e "  Start REPL:      ${YELLOW}ipl repl${NC}"
    echo -e "  List models:     ${YELLOW}ipl models${NC}"
    
    if [[ "$INSTALL_OLLAMA" == true ]]; then
        echo -e "\n${BLUE}Advanced AI Features (with Ollama):${NC}"
        echo -e "  Use Qwen model:  ${YELLOW}ipl run script.ipl --model qwen2.5-coder:0.5b${NC}"
    else
        echo -e "\n${BLUE}Note: IPL is using embedded intelligence (fast, no dependencies)${NC}"
        echo -e "${BLUE}To add advanced AI later, run: ${YELLOW}curl -sSL https://install.ipl-lang.sh | bash${NC} and select 'y' for Ollama${NC}"
    fi
    
    echo -e "\n${BLUE}For more information, see: ${YELLOW}https://github.com/your-repo/ipl${NC}"
}

# Run main function
main