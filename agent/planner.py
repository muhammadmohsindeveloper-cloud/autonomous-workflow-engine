import json

class Planner:

    def create_plan(self, user_input: str):
        """
        Simple rule-based AI planner
        (baad me LLM se replace karenge)
        """

        user_input = user_input.lower()

        steps = []

        if "email" in user_input:
            steps.append("send_email")

        if "database" in user_input or "db" in user_input:
            steps.append("save_db")

        if "http" in user_input or "api" in user_input:
            steps.append("http_request")

        if not steps:
            steps.append("log")

        return {
            "steps": steps
        }