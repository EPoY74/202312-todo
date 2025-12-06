import sys
import shutil
import subprocess


def _build_cmd():
    """Build command to run the CLI. Prefer using `uv run`
     if available, otherwise use the current
    Python executable. Pass --help to avoid interactive
     prompts and make the test minimal.
    """
    base = [sys.executable, "-m", "src.cli", "--help"]
    if shutil.which("uv"):
        return ["uv", "run"] + base
    return base


def test_cli_runs_help():
    cmd = _build_cmd()
    # Run the CLI, capture output. Keep timeout short to avoid hanging tests.
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0, (
        f"CLI exited with non-zero status {res.returncode}.\n"
        + f"stdout:\n{res.stdout}\n\nstderr:\n{res.stderr}"
    )
    # Ensure some output (help text usually appears on stdout or stderr)
    output = (res.stdout or "") + (res.stderr or "")
    assert output, "No output from CLI help (stdout and stderr are empty)"

    # Expected help substrings. Each entry is a list of acceptable variants
    #  for the same feature.
    # For example the list command may be named --task_list or --tasks_list
    #  depending on implementation.
    expected_groups = [
        ["--create_db"],
        ["-h, --help"],
        ["--task_add"],
        ["--task_list", "--tasks_list"],
        ["--deadline_at"],
        ["--completed_at"],
        ["--task_del_id", "--task_delete", "--task_del"],
    ]

    missing_groups = []
    for group in expected_groups:
        if not any(option in output for option in group):
            # record the canonical name (first in group) for the error message
            missing_groups.append(group[0])

    assert not missing_groups, (
        "The CLI help output is missing expected option(s): "
        + ", ".join(missing_groups)
        + f"\n\nFull help output:\n{output}"
    )
