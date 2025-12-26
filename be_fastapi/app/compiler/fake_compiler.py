# MOCK VERSION - Use this to get the API working immediately
import json

class GuildFlowCompiler:
    def visit(self, tree):
        """
        Ignores the actual input tree and returns FAKE data 
        to test the API and Database connection.
        """
        print("⚠️ WARNING: Using Mock Compiler")
        
        # This matches the schema Member B built
        return [
            {
                "type": "WORKFLOW",
                "name": "mock_workflow", # We will overwrite this with the real name in main.py
                "trigger": "message",
                "filter": None,
                "actions": [
                    {
                        "type": "ACTION",
                        "command": "SEND_MESSAGE",
                        "params": {
                            "channel": "general",
                            "content": "This is a fake response from the API"
                        }
                    }
                ]
            }
        ]
