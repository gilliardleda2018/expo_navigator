import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "app.py").read_text(encoding="utf-8")

class AppStructureTests(unittest.TestCase):
    def test_python_syntax(self):
        ast.parse(SOURCE)

    def test_twelve_questions(self):
        tree = ast.parse(SOURCE)
        assignment = next(node for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "QUESTIONS" for t in node.targets))
        self.assertEqual(len(ast.literal_eval(assignment.value)), 12)

    def test_no_idle_stop_button(self):
        self.assertNotIn('st.button("Parar', SOURCE)
        self.assertNotIn('st.button("Encerrar', SOURCE)

    def test_six_guided_arrival_steps(self):
        tree = ast.parse(SOURCE)
        assignment = next(node for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ROUTE" for t in node.targets))
        route = ast.literal_eval(assignment.value)
        self.assertEqual(len(route), 6)
        self.assertIn("Marco Polo", route[0][0])
        self.assertIn("hospedagem", route[-1][0].lower())
        self.assertTrue(all(len(step) == 5 for step in route))

    def test_guided_navigation_and_progress(self):
        self.assertIn("st.progress(", SOURCE)
        self.assertIn("st.session_state.route_step", SOURCE)
        self.assertIn("Concluir e avançar", SOURCE)
        self.assertIn("Anterior", SOURCE)

    def test_audio_and_translation_paths(self):
        self.assertIn("st.audio_input(", SOURCE)
        self.assertIn("transcribe(client, data)", SOURCE)
        self.assertIn("translate(client, original)", SOURCE)
        self.assertIn("speech(client, translated)", SOURCE)

if __name__ == "__main__":
    unittest.main()
