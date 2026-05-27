import ast
import astor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AST-Patcher")

class VulnerabilityTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            logger.warning(f"Vulnerability found: Unsafe eval() call at line {node.lineno}")
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id="ast", ctx=ast.Load()), attr="literal_eval", ctx=ast.Load()),
                args=node.args,
                keywords=node.keywords
            )
        return node

def patch_source_code(source_code: str) -> tuple:
    tree = ast.parse(source_code)
    transformer = VulnerabilityTransformer()
    patched_tree = transformer.visit(tree)
    ast.fix_missing_locations(patched_tree)
    return astor.to_source(patched_tree), transformer.patches_applied

if __name__ == "__main__":
    pass

# Refactored update: stage 4 checkpoint - 2026-05-27
