from contextlib import contextmanager
from pathlib import Path

from invoke import task, Context


class Paths:
    here = Path(__file__).parent
    repo_root = here
    src = repo_root / 'src'

    @staticmethod
    @contextmanager
    def cd(c: Context, p: Path):
        with c.cd(str(p)):
            yield


@task
def compile_requirements(c, install=True):
    with Paths.cd(c, Paths.repo_root):
        c.run("pip-compile -v -o requirements.txt --upgrade")
        if install:
            c.run("pip install -r requirements.txt")
            c.run("pip install -r requirements.dev.txt --upgrade")


@task
def run_streamlit(c):
    with Paths.cd(c, Paths.src):
        c.run(
            "python -m streamlit run streamlit_app.py",
            pty=True,
        )


@task
def lint(c):
    with Paths.cd(c, Paths.repo_root):
        c.run("ruff check . --fix", pty=True)
