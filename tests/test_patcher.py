from patcher import patch_source_code

def test_eval_remediation():
    vulnerable = "result = eval(user_input)"
    secured, count = patch_source_code(vulnerable)
    assert count == 1
    assert "ast.literal_eval" in secured
    assert "eval(" not in secured

def test_safe_calculations():
    safe_code = "def add(a, b): return a + b"
    secured, count = patch_source_code(safe_code)
    assert count == 0
    assert "def add(a, b):" in secured
