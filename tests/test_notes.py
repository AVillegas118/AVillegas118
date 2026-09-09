"""Pruebas de los ejemplos escritos en Markdown, sin conexiones de red.

Ejecutar desde la raíz: python -m unittest discover -s tests -v
Los bloques se extraen de las notas: no mantenemos copias del código de ejemplo.
"""

import argparse
import ast
import csv
from email import policy
from email.parser import BytesParser
import io
from pathlib import Path
import re
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import MagicMock, call, patch

import requests


ROOT = Path(__file__).resolve().parents[1]
PYTHON_FENCE = re.compile(r"^```python[ \t]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)


def python_blocks(path):
    """Devuelve código y línea de origen para que un fallo señale la nota."""
    text = path.read_text(encoding="utf-8")
    for match in PYTHON_FENCE.finditer(text):
        line = text.count("\n", 0, match.start(1)) + 1
        yield match.group(1), f"{path.name}:{line}"


def load_example(filename, function_name):
    """Carga el bloque que define una función, sin activar su main protegido."""
    for code, origin in python_blocks(ROOT / filename):
        tree = ast.parse(code, filename=origin)
        if any(isinstance(node, ast.FunctionDef) and node.name == function_name
               for node in tree.body):
            module = types.ModuleType("notes_example")
            exec(compile(tree, origin, "exec"), module.__dict__)
            return module
    raise AssertionError(f"No se encontró {function_name} en {filename}")


class NotesTests(unittest.TestCase):
    def setUp(self):
        # Si se olvida un mock, fallamos en vez de consultar una red o enviar correo.
        for target in ("socket.socket.connect", "socket.socket.connect_ex",
                       "requests.sessions.Session.request", "smtplib.SMTP"):
            blocker = patch(target, side_effect=AssertionError("Red bloqueada en las pruebas"))
            blocker.start()
            self.addCleanup(blocker.stop)

    def test_all_python_blocks_compile(self):
        count = 0
        for path in sorted(ROOT.glob("*.md")):
            for code, origin in python_blocks(path):
                with self.subTest(block=origin):
                    tree = ast.parse(code, filename=origin)
                    compile(tree, origin, "exec")
                count += 1
        self.assertGreater(count, 0, "No se encontraron ejemplos Python")

    def test_port_numbers_include_boundaries_and_reject_invalid_values(self):
        scanner = load_example("Escáner de Puertos.md", "parse_port")
        for value in ("1", "80", "65535"):
            with self.subTest(value=value):
                self.assertEqual(scanner.parse_port(value), int(value))
        for value in ("0", "65536", "-1", "80.5", "ssh", ""):
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    scanner.parse_port(value)

    def test_scanner_rejects_invalid_targets_and_ranges_before_connecting(self):
        scanner = load_example("Escáner de Puertos.md", "main")
        cases = (
            ["--host", "192.0.2.10", "--start", "80", "--end", "80"],
            ["--host", "2001:db8::1", "--start", "80", "--end", "80"],
            ["--host", "localhost", "--start", "80", "--end", "80"],
            ["--start", "81", "--end", "80"],
            ["--start", "1", "--end", "1001"],
            ["--start", "0", "--end", "80"],
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                with patch("sys.argv", ["scanner.py", *arguments]), \
                        patch.object(scanner, "is_open") as connect, \
                        redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as result:
                        scanner.main()
                    self.assertEqual(result.exception.code, 2)
                    connect.assert_not_called()

    def test_scanner_accepts_loopback_and_checks_inclusive_range(self):
        scanner = load_example("Escáner de Puertos.md", "main")
        for address in ("127.0.0.1", "127.2.3.4", "::1"):
            with self.subTest(address=address):
                output = io.StringIO()
                arguments = ["scanner.py", "--host", address, "--start", "8000", "--end", "8001"]
                with patch("sys.argv", arguments), \
                        patch.object(scanner, "is_open", side_effect=[True, False]) as connect, \
                        redirect_stdout(output):
                    scanner.main()
                self.assertEqual(connect.call_args_list, [call(address, 8000), call(address, 8001)])
                self.assertEqual(output.getvalue().splitlines(), [f"ABIERTO  {address}:8000"])

    def test_connection_outcomes_and_socket_cleanup(self):
        scanner = load_example("Escáner de Puertos.md", "is_open")
        with patch.object(scanner.socket, "create_connection") as create:
            self.assertTrue(scanner.is_open("127.0.0.1", 8000, timeout=0.5))
            create.assert_called_once_with(("127.0.0.1", 8000), timeout=0.5)
            create.return_value.__exit__.assert_called_once_with(None, None, None)
        for error in (TimeoutError(), ConnectionRefusedError(), OSError("simulado")):
            with self.subTest(error=type(error).__name__):
                with patch.object(scanner.socket, "create_connection", side_effect=error):
                    self.assertFalse(scanner.is_open("127.0.0.1", 8000))

    def test_email_mime_text_roundtrip(self):
        email_example = load_example("Envió de Correos.md", "build_message")
        message = BytesParser(policy=policy.default).parsebytes(email_example.build_message().as_bytes())
        self.assertEqual(message["From"], "remitente@example.com")
        self.assertEqual(message["To"], "destinatario@example.net")
        self.assertEqual(message["Subject"], "Mensaje de laboratorio")
        self.assertEqual(message.get_content_type(), "text/plain")
        self.assertEqual(message.get_content().strip(),
                         "Este correo es ficticio y fue creado localmente para aprender.")

    def test_email_file_is_created_but_never_overwritten(self):
        email_example = load_example("Envió de Correos.md", "build_message")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "correo.eml"
            with patch.object(email_example, "OUTPUT", destination), redirect_stdout(io.StringIO()):
                email_example.main()
                original = destination.read_bytes()
                self.assertIn(b"Mensaje de laboratorio", original)
                with self.assertRaises(FileExistsError):
                    email_example.main()
                self.assertEqual(destination.read_bytes(), original)

    def test_scraper_extracts_paired_text_and_checks_http_status(self):
        scraper = load_example("Webscraping.md", "fetch_quotes")
        response = MagicMock()
        response.text = """
            <div class="quote"><span class="text"> Cita uno </span>
                <small class="author">Autora uno</small></div>
            <div class="quote"><span class="text"><b>Cita dos</b></span>
                <small class="author"> Autor dos </small></div>
        """
        with patch.object(scraper.requests, "get", return_value=response) as get:
            self.assertEqual(scraper.fetch_quotes(),
                             [("Cita uno", "Autora uno"), ("Cita dos", "Autor dos")])
            get.assert_called_once_with(scraper.URL, headers=scraper.HEADERS, timeout=10)
            response.raise_for_status.assert_called_once_with()
            response.raise_for_status.side_effect = requests.HTTPError("503 simulado")
            with self.assertRaises(requests.HTTPError):
                scraper.fetch_quotes()

    def test_scraper_rejects_missing_cards_or_fields(self):
        scraper = load_example("Webscraping.md", "fetch_quotes")
        for html in ("<p>Sin citas</p>",
                     '<div class="quote"><span class="text">Sin autor</span></div>',
                     '<div class="quote"><small class="author">Sin cita</small></div>'):
            with self.subTest(html=html):
                response = MagicMock(text=html)
                with patch.object(scraper.requests, "get", return_value=response):
                    with self.assertRaises(ValueError):
                        scraper.fetch_quotes()

    def test_csv_preserves_text_neutralizes_formulas_and_does_not_overwrite(self):
        scraper = load_example("Webscraping.md", "save_csv")
        suspicious = ("=1+1", "  =1+1", "+1+1", "-1+1", "@SUM(A1)", "\ttexto", "\rtexto")
        for value in suspicious:
            with self.subTest(value=value):
                self.assertEqual(scraper.csv_text(value), "'" + value)
        ordinary = 'Texto con coma, "comillas" y acento: acción'
        self.assertEqual(scraper.csv_text(ordinary), ordinary)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "citas.csv"
            scraper.save_csv([(ordinary, "Autora"), ("=1+1", "+2")], destination)
            original = destination.read_bytes()
            with destination.open(encoding="utf-8", newline="") as handle:
                self.assertEqual(list(csv.reader(handle)),
                                 [["cita", "autor"], [ordinary, "Autora"], ["'=1+1", "'+2"]])
            with self.assertRaises(FileExistsError):
                scraper.save_csv([("Otra cita", "Otra autora")], destination)
            self.assertEqual(destination.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
