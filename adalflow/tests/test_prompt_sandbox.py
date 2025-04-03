import unittest
from adalflow.core import Generator
from adalflow.core.types import ModelClientType


class TestPromptSandbox(unittest.TestCase):
    def test_jinja2_sandbox_blocks_dangerous_template(self):
        """Ensure that dangerous Jinja2 expressions are blocked in the sandboxed environment."""

        malicious_template = (
            "{{ self._TemplateReference__context.cycler.__init__.__globals__.os.system('id') }}"
        )

        generator = Generator(
            template=malicious_template,
            model_client=ModelClientType.OPENAI()
        )

        with self.assertRaises(Exception) as context:
            generator.print_prompt()

        print(f"Caught exception: {context.exception}")
        self.assertTrue("unsafe" in str(context.exception))


if __name__ == "__main__":
    unittest.main()