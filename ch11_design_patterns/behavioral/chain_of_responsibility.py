# The **Chain of Responsibility (CoR)** pattern is a **behavioral design pattern**
# that allows a request to be **passed along a chain of handlers**, where each
# handler decides **whether to process it** or **pass it to the next handler**.

from abc import ABC, abstractmethod

class WorkflowHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, request: dict) -> dict:
        pass


class AuthHandler(WorkflowHandler):
    def handle(self, request: dict) -> dict:
        if not request.get("authenticated", False):
            raise Exception("User not authenticated!")
        print("Authentication passed")
        return self.next_handler.handle(request) if self.next_handler else request


class ValidationHandler(WorkflowHandler):
    def handle(self, request: dict) -> dict:
        if "query" not in request:
            raise Exception("Invalid request: missing query!")
        print("Request validated")
        return self.next_handler.handle(request) if self.next_handler else request


class ExecutionHandler(WorkflowHandler):
    def handle(self, request: dict) -> dict:
        request["results"] = ["case-1", "case-2"]
        print("Workflow executed, results attached")
        return request


if __name__ == "__main__":
    chain = AuthHandler(ValidationHandler(ExecutionHandler()))

    original_request = {"authenticated": True, "query": "find cases"}
    final_response = chain.handle(original_request)
    print("Final Response:", final_response)