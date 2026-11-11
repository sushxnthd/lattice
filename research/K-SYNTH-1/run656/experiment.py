"""Run656: executable synthetic descriptor-resolution counterexample; NOT upstream qualification."""
import functools
import json

def arm(parent_text, child_text):
    class Response:
        def get_data(self, as_text=False):
            return "hello" if as_text else b"hello"
    if parent_text:
        Response.text = property(lambda self: self.get_data(as_text=True))
    class TestResponse(Response):
        pass
    if child_text:
        descriptor = functools.cached_property(lambda self: self.get_data(as_text=True))
        descriptor.__set_name__(TestResponse, "text")
        TestResponse.text = descriptor
    p, c = Response(), TestResponse()
    return {
        "response_text": getattr(p, "text", None),
        "test_response_text": getattr(c, "text", None),
        "test_response_own_descriptor": "text" in TestResponse.__dict__,
        "test_response_inherited": "text" not in TestResponse.__dict__ and hasattr(c, "text"),
    }

results = {
    "base": arm(False, True),
    "remove_child_only": arm(False, False),
    "add_parent_only": arm(True, True),
    "full": arm(True, False),
}
assert results["add_parent_only"]["response_text"] == "hello"
assert results["add_parent_only"]["test_response_text"] == "hello"
assert results["add_parent_only"]["test_response_own_descriptor"]
assert results["full"]["test_response_inherited"]
assert results["base"]["response_text"] is None
assert results["remove_child_only"]["test_response_text"] is None
print(json.dumps({"scope": "synthetic Python descriptor resolution, not Werkzeug execution", "results": results}, sort_keys=True, indent=2))
