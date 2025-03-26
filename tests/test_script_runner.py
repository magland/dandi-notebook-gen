"""
Tests for the script_runner module
"""

import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

from dandi_notebook_gen.script_runner import (
    check_for_matplotlib,
    add_matplotlib_backend,
    run_script,
    preprocess_and_run_script
)


class TestScriptRunner(unittest.TestCase):
    """Test cases for the script_runner module"""

    def test_check_for_matplotlib_true(self):
        """Test that matplotlib usage is correctly detected"""
        script_content = """
        import matplotlib.pyplot as plt

        # Some code
        plt.plot([1, 2, 3], [4, 5, 6])
        plt.show()
        """
        self.assertTrue(check_for_matplotlib(script_content))

    def test_check_for_matplotlib_false(self):
        """Test that non-matplotlib scripts are correctly identified"""
        script_content = """
        import numpy as np

        # Some code without matplotlib
        x = np.array([1, 2, 3])
        print(x)
        """
        self.assertFalse(check_for_matplotlib(script_content))

    def test_add_matplotlib_backend_with_import(self):
        """Test adding backend with existing matplotlib import"""
        script_content = "import matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3])"
        modified = add_matplotlib_backend(script_content)
        self.assertIn("matplotlib.use(\"Agg\")", modified)
        self.assertTrue(modified.index("import matplotlib") < modified.index("matplotlib.use(\"Agg\")"))

    def test_add_matplotlib_backend_with_from_import(self):
        """Test adding backend with from matplotlib import"""
        script_content = "from matplotlib import pyplot as plt\n\nplt.plot([1, 2, 3])"
        modified = add_matplotlib_backend(script_content)
        self.assertIn("matplotlib.use(\"Agg\")", modified)
        self.assertTrue(modified.index("import matplotlib") < modified.index("matplotlib.use(\"Agg\")"))
        self.assertTrue(modified.index("matplotlib.use(\"Agg\")") < modified.index("from matplotlib"))

    def test_add_matplotlib_backend_no_import(self):
        """Test adding backend when no matplotlib import exists"""
        script_content = "import numpy as np\n\nx = np.array([1, 2, 3])"
        modified = add_matplotlib_backend(script_content)
        self.assertIn("matplotlib.use(\"Agg\")", modified)
        self.assertTrue(modified.index("import matplotlib") == 0)

    @patch('subprocess.run')
    def test_run_script_success(self, mock_run):
        """Test running a script successfully"""
        # Mock successful subprocess run
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Script output"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        success, output, error = run_script("test_script.py")
        self.assertTrue(success)
        self.assertEqual(output, "Script output")
        self.assertIsNone(error)

    @patch('subprocess.run')
    def test_run_script_failure(self, mock_run):
        """Test running a script that fails"""
        # Mock failed subprocess run
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = ""
        mock_process.stderr = "Error message"
        mock_run.return_value = mock_process

        success, output, error = run_script("test_script.py")
        self.assertFalse(success)
        self.assertIsNone(output)
        self.assertEqual(error, "Error message")

    @patch('dandi_notebook_gen.script_runner.run_script')
    def test_preprocess_and_run_script_no_matplotlib(self, mock_run_script):
        """Test preprocessing and running a script without matplotlib"""
        # Mock successful script run
        mock_run_script.return_value = (True, "Output", None)

        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(b"print('Hello, world!')")
            temp_path = temp.name

        try:
            success, output, error = preprocess_and_run_script(temp_path)
            self.assertTrue(success)
            self.assertEqual(output, "Output")
            self.assertIsNone(error)

            # Verify the original script was run (no _run file created)
            mock_run_script.assert_called_once_with(temp_path, True)
        finally:
            os.unlink(temp_path)

    @patch('dandi_notebook_gen.script_runner.run_script')
    def test_preprocess_and_run_script_with_matplotlib(self, mock_run_script):
        """Test preprocessing and running a script with matplotlib"""
        # Mock successful script run
        mock_run_script.return_value = (True, "Output", None)

        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(b"import matplotlib.pyplot as plt\nplt.plot([1, 2, 3])\nplt.show()")
            temp_path = temp.name

        try:
            success, output, error = preprocess_and_run_script(temp_path)
            self.assertTrue(success)
            self.assertEqual(output, "Output")
            self.assertIsNone(error)

            # Verify the modified script was run (with _run suffix)
            run_path = Path(temp_path).with_stem(f"{Path(temp_path).stem}_run")
            mock_run_script.assert_called_once_with(str(run_path), True)

            # Verify the modified file exists and contains the backend setting
            self.assertTrue(os.path.exists(run_path))
            with open(run_path, 'r') as f:
                content = f.read()
                self.assertIn("matplotlib.use(\"Agg\")", content)

            # Clean up the modified file
            os.unlink(run_path)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
