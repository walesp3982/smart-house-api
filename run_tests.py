#!/usr/bin/env python3
"""
Script helper para ejecutar tests
Uso: python run_tests.py [tipo]

Tipos disponibles:
  - unit      : Solo tests unitarios (rápido, sin Ollama)
  - endpoint  : Solo tests del endpoint (rápido, sin Ollama)
  - integration : Solo tests de integración (requiere Ollama)
  - all       : Todos los tests
  - coverage  : Tests con reporte de cobertura
"""

import argparse
import subprocess
import sys


def run_command(cmd, description):
    """Ejecuta comando y muestra resultado"""
    print(f"\n{'=' * 70}")
    print(f"▶️  {description}")
    print(f"{'=' * 70}\n")

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"\n❌ Error en: {description}")
        return False

    print(f"\n✅ Completado: {description}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Helper para ejecutar tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python run_tests.py unit              # Solo tests unitarios
  python run_tests.py endpoint          # Solo tests del endpoint
  python run_tests.py all -v            # Todos los tests con verbose
  python run_tests.py coverage          # Con reporte de cobertura
        """,
    )

    parser.add_argument(
        "type",
        nargs="?",
        default="unit",
        choices=["unit", "endpoint", "integration", "all", "coverage"],
        help="Tipo de tests a ejecutar",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Output detallado")

    parser.add_argument("-s", "--show-output", action="store_true", help="Mostrar print statements")

    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        help="Ejecutar solo tests que coincidan con keyword",
    )

    args = parser.parse_args()

    verbose = "-v" if args.verbose else ""
    show_output = "-s" if args.show_output else ""
    keyword = f"-k {args.keyword}" if args.keyword else ""

    commands = {
        "unit": f"pytest tests/test_ollama_service.py {verbose} {show_output} {keyword}",
        "endpoint": f"pytest tests/test_ask_endpoint.py {verbose} {show_output} {keyword}",
        "integration": f"pytest tests/test_ollama_integration.py {verbose} {show_output} {keyword}",
        "all": f"pytest tests/ {verbose} {show_output} {keyword}",
        "coverage": f"pytest tests/ --cov=app/services/ollama --cov-report=term-missing --cov-report=html {verbose}",
    }

    cmd = commands[args.type]

    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    Smart House API - Test Runner                    ║
╚══════════════════════════════════════════════════════════════════════╝

Tipo de tests: {args.type.upper()}
Verbose: {args.verbose}
Show output: {args.show_output}
Keyword filter: {args.keyword or "None"}

Ejecutando: {cmd}
    """)

    success = run_command(cmd, f"Tests {args.type}")

    if args.type == "coverage":
        print("\n📊 Reporte de cobertura generado en: htmlcov/index.html")
        print("   Abre: open htmlcov/index.html")

    if args.type == "integration":
        print("\n⚠️  Asegúrate de que Ollama está corriendo:")
        print("   ollama serve")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
