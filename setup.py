from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["mission_planner_router.py", "schema.py", "utils_mission.py", "main.py"],
        compiler_directives={"language_level": "3"}  # Python 3 support
    ),
)