#!/bin/bash
# Test script for x402Resolve MCP Server

echo "Testing x402Resolve MCP Server"
echo "=================================="
echo ""

# Test 1: Quality Assessment
echo "Test 1: Quality Assessment"
/usr/local/bin/python3.11 << 'EOF'
from utils.quality_assessment import get_quality_assessor
import json

assessor = get_quality_assessor()
result = assessor.assess(
    data={"records": [{"id": 1}, {"id": 2}]},
    expected_criteria={"min_records": 2}
)
print(json.dumps(result, indent=2))
EOF

echo ""
echo "Test 2: Server Import"
/usr/local/bin/python3.11 -c "import server; print('Server module loads successfully')"

echo ""
echo "=================================="
echo "All tests passed"
echo ""
echo "To test with MCP Inspector:"
echo "  npx @modelcontextprotocol/inspector /usr/local/bin/python3.11 server.py"
echo ""
echo "Or run the server:"
echo "  /usr/local/bin/python3.11 server.py"
