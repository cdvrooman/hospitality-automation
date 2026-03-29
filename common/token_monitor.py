import os

class MyTokenTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_calls = 0

    def log_usage(self, response):
        """I'll extract metadata from a GenAI response object."""
        usage = response.usage_metadata
        
        # I'm tracking individual chunks
        self.total_input_tokens += usage.prompt_token_count
        self.total_output_tokens += usage.candidates_token_count
        self.total_calls += 1
        
        print(f"\n--- 🎫 CALL #{self.total_calls} USAGE ---")
        print(f"Prompt (Input): {usage.prompt_token_count}")
        print(f"Candidate (Output): {usage.candidates_token_count}")
        print(f"Total Call Tokens: {usage.total_token_count}")

    def get_summary(self):
        """I'll use this at the end of a Deep Research run."""
        return {
            "calls": self.total_calls,
            "input": self.total_input_tokens,
            "output": self.total_output_tokens,
            "total": self.total_input_tokens + self.total_output_tokens
        }

# I'll instantiate this for my current session
tracker = MyTokenTracker()