#!/bin/bash
# Quick setup script for Library Management API comparison

echo "🎯 Setting up Library Management API Comparison..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found (optional for code generation tools)"
else
    echo "✅ Node.js found: $(node --version)"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the server:"
echo "   python app.py"
echo ""
echo "🧪 To run tests (in another terminal):"
echo "   python test_api.py"
echo ""
echo "📚 Documentation formats are in:"
echo "   - openapi/openapi.yaml"
echo "   - api-blueprint/blueprint.md"
echo "   - raml/library.raml"
echo "   - typespec/library.tsp"
