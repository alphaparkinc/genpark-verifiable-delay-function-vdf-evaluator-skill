"""MCP Server for Verifiable Delay Function Skill."""
import json
import sys
from client import VerifiableDelayFunction

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "evaluate_vdf",
                                "description": "Sequentially compute VDF output and proof",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "seed": {"type": "integer"},
                                        "steps": {"type": "integer"}
                                    },
                                    "required": ["seed", "steps"]
                                }
                            },
                            {
                                "name": "verify_vdf",
                                "description": "Verify VDF proof",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "seed": {"type": "integer"},
                                        "steps": {"type": "integer"},
                                        "output": {"type": "integer"},
                                        "proof": {"type": "string"}
                                    },
                                    "required": ["seed", "steps", "output", "proof"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "evaluate_vdf":
                    out_val, proof = VerifiableDelayFunction.evaluate(args["seed"], args["steps"])
                    out = {"output": out_val, "proof": proof}
                else:
                    valid = VerifiableDelayFunction.verify(args["seed"], args["steps"], args["output"], args["proof"])
                    out = {"valid": valid}
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
