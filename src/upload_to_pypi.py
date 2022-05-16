import os
import re
import shlex
import subprocess
import sys

import pygit2


def upload_to_pypi():
    os.environ["TWINE_USERNAME"] = "__token__"
    os.environ["TWINE_PASSWORD"] = os.environ["INPUT_PYPI_TOKEN"]
    tag = os.environ["GITHUB_REF"].split("/")[-1]
    build_folder = "dist"
    version = tag.strip("v")
    base_branch = re.findall(r"v\d+.\d+", tag)[0]

    print(f"Building version {version}")
    print(f"Building from branch {base_branch}")

    repo = pygit2.Repository(path=".")
    repo.checkout(refname=f"refs/remotes/origin/{base_branch}")

    subprocess.check_output(
        shlex.split(f"python -m build --sdist --outdir {build_folder}/")
    )
    dist_pkg = [pkg for pkg in os.listdir(build_folder) if version in pkg]
    if not dist_pkg:
        print(f"No package to upload under {build_folder}/ folder")
        sys.exit(1)

    dist_pkg = dist_pkg[0]
    subprocess.check_output(shlex.split(f"twine check {build_folder}/{dist_pkg}"))
    subprocess.check_output(
        shlex.split(f"twine upload {build_folder}/{dist_pkg} --skip-existing")
    )
