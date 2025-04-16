# Copyright 2025 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Adapted from huggingface/transformers: https://github.com/huggingface/transformers/blob/21a2d900eceeded7be9edc445b56877b95eda4ca/setup.py


import re
import shutil
from pathlib import Path

from setuptools import find_packages, setup


# Remove stale open_r1.egg-info directory to avoid https://github.com/pypa/pip/issues/5466
stale_egg_info = Path(__file__).parent / "open_r1.egg-info"
if stale_egg_info.exists():
    print(
        (
            "Warning: {} exists.\n\n"
            "If you recently updated open_r1, this is expected,\n"
            "but it may prevent open_r1 from installing in editable mode.\n\n"
            "This directory is automatically generated by Python's packaging tools.\n"
            "I will remove it now.\n\n"
            "See https://github.com/pypa/pip/issues/5466 for details.\n"
        ).format(stale_egg_info)
    )
    shutil.rmtree(stale_egg_info)


# IMPORTANT: all dependencies should be listed here with their version requirements, if any.
#   * If a dependency is fast-moving (e.g. trl), pin to the exact version
_deps = [
    "accelerate",
    "bitsandbytes",
    "datasets",
    "deepspeed",
    "distilabel[vllm,ray,openai]",
    "e2b-code-interpreter",
    "einops",
    "flake8",
    "hf_transfer",
    "huggingface-hub[cli]",
    "isort",
    "langdetect",  # Needed for LightEval's extended tasks
    "latex2sympy2_extended",
    "liger_kernel",
    "lighteval @ git+https://github.com/huggingface/lighteval.git@ed084813e0bd12d82a06d9f913291fdbee774905",
    "math-verify",  # Used for math verification in grpo
    "packaging",
    "parameterized",
    "peft",
    "pytest",
    "python-dotenv", 
    "ruff",
    "safetensors",
    "sentencepiece",
    "torch",
    "transformers",
    "trl",
    "vllm",
    "wandb",
]

# this is a lookup table with items like:
#
# tokenizers: "tokenizers==0.9.4"
# packaging: "packaging"
#
# some of the values are versioned whereas others aren't.
deps = {b: a for a, b in (re.findall(r"^(([^!=<>~ \[\]]+)(?:\[[^\]]+\])?(?:[!=<>~ ].*)?$)", x)[0] for x in _deps)}


def deps_list(*pkgs):
    return [deps[pkg] for pkg in pkgs]


extras = {}
extras["tests"] = deps_list("pytest", "parameterized", "math-verify")
extras["torch"] = deps_list("torch")
extras["quality"] = deps_list("ruff", "isort", "flake8")
extras["code"] = deps_list("e2b-code-interpreter", "python-dotenv")
extras["eval"] = deps_list("lighteval", "math-verify")
extras["dev"] = extras["quality"] + extras["tests"] + extras["eval"] + extras["code"]

# core dependencies shared across the whole project - keep this to a bare minimum :)
install_requires = [
    deps["accelerate"],
    deps["bitsandbytes"],
    deps["einops"],
    deps["datasets"],
    deps["deepspeed"],
    deps["hf_transfer"],
    deps["huggingface-hub"],
    deps["langdetect"],
    deps["latex2sympy2_extended"],
    deps["math-verify"],
    deps["liger_kernel"],
    deps["packaging"],  # utilities from PyPA to e.g., compare versions
    deps["safetensors"],
    deps["sentencepiece"],
    deps["transformers"],
    deps["trl"],
    deps["wandb"],
]

setup(
    name="open-r1",
    version="0.1.0.dev0",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
    author="The Hugging Face team (past and future)",
    author_email="lewis@huggingface.co",
    description="Open R1",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="llm inference-time compute reasoning",
    license="Apache",
    url="https://github.com/huggingface/open-r1",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    extras_require=extras,
    python_requires=">=3.10.9",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
