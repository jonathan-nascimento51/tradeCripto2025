import argparse
import subprocess
import sys


def run(cmd: str) -> None:
    """Run a shell command and exit if it fails."""
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage changes, create a commit and push to the remote repository",
    )
    parser.add_argument("message", help="Commit message")
    parser.add_argument("--agent", required=True, help="Agent name for commit tag")
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="Specific files to add. Defaults to all modified files.",
    )
    parser.add_argument(
        "--remote", default="origin", help="Git remote to push to (default: origin)"
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="Branch to push to (default: current branch)",
    )
    args = parser.parse_args()

    if args.files:
        run("git add " + " ".join(args.files))
    else:
        run("git add -A")

    commit_msg = f"{args.message} – agent::{args.agent}"
    run(f"git commit -m \"{commit_msg}\"")

    push_cmd = f"git push {args.remote}"
    if args.branch:
        push_cmd += f" {args.branch}"
    run(push_cmd)


if __name__ == "__main__":
    main()