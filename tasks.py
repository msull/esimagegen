from pathlib import Path

from invoke import Context, task


class Paths:
    repo_root = Path(__file__).parent
    src_dir = repo_root / 'src'
    example_tables = repo_root / "example_tables"


def from_repo_root(c: Context):
    return c.cd(Paths.repo_root)


@task
def compile_requirements(c: Context, install=True, upgrade=False):
    with from_repo_root(c):
        upgrade_flag = "--upgrade" if upgrade else ""
        c.run(f"pip-compile {upgrade_flag} -v --strip-extras --extra dev --extra build pyproject.toml", pty=True)
        c.run("mv requirements.txt requirements.dev.txt", pty=True)
        c.run('echo "-e ." >> requirements.dev.txt')
        if install:
            c.run("pip-sync requirements.dev.txt", pty=True)


@task
def run_streamlit_app(c: Context):
    with c.cd(Paths.src_dir):
        c.run("streamlit run streamlit_app.py --server.headless True --server.address 0.0.0.0", pty=True)
