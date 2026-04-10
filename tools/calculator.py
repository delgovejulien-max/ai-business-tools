"""Outil : Calculatrice simple"""
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """
    Calcule une expression mathématique simple.

    Args:
        expression: L'expression à calculer (ex: "12 * 5 + 3")

    Returns:
        Le résultat du calcul
    """
    try:
        result = eval(expression)
        return str(result)
    except SyntaxError:
        return f"Erreur de syntaxe dans l'expression: {expression}"
    except Exception as e:
        return f"Erreur lors du calcul: {str(e)}"
