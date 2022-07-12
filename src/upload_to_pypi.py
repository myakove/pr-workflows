import os
import re
import shlex
import subprocess


def upload_to_pypi():
    os.environ["TWINE_USERNAME"] = "__token__"
    os.environ["TWINE_PASSWORD"] = os.environ["INPUT_PYPI_TOKEN"]
    build_folder = "dist"

    _out = subprocess.check_output(
        shlex.split(f"python -m build --sdist --outdir {build_folder}/")
    )
    dist_pkg = re.search(r"Successfully built (.*.tar.gz)", _out.decode("utf-8")).group(
        1
    )
    dist_pkg_path = os.path.join(build_folder, dist_pkg)
    subprocess.check_output(shlex.split(f"twine check {dist_pkg_path}"))
    subprocess.check_output(
        shlex.split(f"twine upload {dist_pkg_path} --skip-existing")
    )
