import setuptools
from os.path import dirname
from glob import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Package list is autogenerated to be any 'perceval' subfolder containing a __init__.py file
package_list = [dirname(p).replace('\\', '.') for p in glob('perceval/**/__init__.py', recursive=True)]

setuptools.setup(
    name="perceval-quandela",
    author="quandela",
    author_email="perceval@quandela.com",
    description="A powerful Quantum Photonic Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quandela/Perceval",
    project_urls={
        "Documentation": "https://perceval.quandela.net/docs/",
        "Source": "https://github.com/Quandela/Perceval",
        "Tracker": "https://github.com/Quandela/Perceval/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=package_list,
    install_requires=['sympy', 'numpy', 'scipy', 'tabulate', 'matplotlib', 'multipledispatch',
                      'protobuf>=3.20.3', 'drawsvg>=2.0', 'Deprecated', 'requests', 'networkx~=3.1', 'latexcodec',
                      'platformdirs'],
    extras_require={
        "qiskit_bridge": ["qiskit~=0.45.1", "seaborn~=0.13"],
        "qutip_bridge": ["qutip~=4.7.3"],
        "myqlm_bridge": ["myqlm~=1.9.5"]
    },
    setup_requires=["scmver"],
    python_requires=">=3.8,<3.12",
    scmver=True
)
