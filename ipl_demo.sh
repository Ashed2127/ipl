#!/bin/bash
# IPL CLI Demo Script
# This script demonstrates the key features of the IPL CLI

echo "=== IPL CLI Demo ==="
echo ""
echo "1. Show help"
python3 cli.py --help
echo ""
echo "Press Enter to continue..."
read

echo "2. List available AI models"
python3 cli.py models
echo ""
echo "Press Enter to continue..."
read

echo "3. Run a simple IPL program with admin privileges"
python3 cli.py run examples/08_neuro_symbolic_compiler.ipl --user developer --role admin
echo ""
echo "Press Enter to continue..."
read

echo "4. Try the same program with guest privileges (should be blocked)"
python3 cli.py run examples/08_neuro_symbolic_compiler.ipl --user guest --role guest
echo ""
echo "Press Enter to continue..."
read

echo "5. Audit the program with cryptographic trace"
python3 cli.py audit examples/08_neuro_symbolic_compiler.ipl --user developer --role admin
echo ""
echo "Demo complete!"