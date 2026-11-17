from pathlib import Path
import pytest

FICHIERS = [f for f in Path(".").rglob("*.py")
            if "actions-runner" not in f.parts and "tests" not in f.parts]

@pytest.mark.parametrize("fichier", FICHIERS, ids=str)
def test_compile(fichier):
    compile(fichier.read_text(), str(fichier), "exec")
