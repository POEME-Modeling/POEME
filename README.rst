====================================================
POEME: Python Object Engineering Modular Environment
====================================================

    POEME: A good model works.  A great model is a work of art.  (THIS CODE IS IN ALPHA! SEE ABOUT SECTION)

.. raw:: html

    <p>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
    <a href="#"><img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status"></a>
    </p>

Table of Contents
=================

- `About`_
- `Features`_
- `Requirements`_
- `Installation`_
- `Usage`_
- `Project Structure`_
- `Contributing`_
- `License`_
- `Contact`_

About
=====

POEME (pronounced "poem") is a python-based object-oriented modular engineering environment code. 
It is designed to solve your problems, supporting many kinds of physics-based modeling such as
electric circuit modeling, a spring mass dynamic system, and thermodynamic cycle system modeling
and Brayton thermodynamic cycles in particular.
The thermodynamic system models include an air conditioner cycle, a transient ground 
power system with a PIV controller, and a commercial turbofan engine running a flight envelope.

Note with regard to the latter: If you are a thermodynamic engineer, you should really explore 
learning the Numerical Propulsion System Simulation (NPSS) code. 
NPSS is the standard professional tool for analyzing and designing aircraft engine thermodynamic
cycles. POEME is an engineering and software simplification of NPSS; there are no 
secondary effects on turbomachinery performance and the bleed system modeling is 
simplified. POEME is not capable of running real-time transient analysis, which is major 
driver for professional aircraft engine dynamic system simulation. POEME, although designed to 
run quickly, executes each thermodynamic cycle case on the order of one second.
As such, POEME should be viewed as a stepping stone to more advanced tools but is
sufficient for academic use.

This codebase is currently in alpha! It should not be relied on and will be subject to breaking
API changes. Additionally, this README is woefully inadequate. There is currently no API
documentation. There is currently no implemented testing. That said, if you would like to contribute,
feel free to open a pull request!

Running the Examples
====================

To run the examples, go to the ``tests/`` directory and type ``python <test_file_name>.py``. These tests can serve as a starting point to learn from and modify.

The models are:

- ``turbofan_test.py`` — Runs a commercial turbofan engine over a flight envelope.
- ``brayton_cantera.py`` — Runs a transient turbojet power generator with a PIV controller. Uses the ``cantera`` package to determine gas properties. This model is completely notional and not based on any real design.
- ``spring_mass_test.py`` — A dynamic spring system that oscillates when perturbed from equilibrium.
- ``lcr.py`` — An electric circuit with a resistor, capacitor, and an inductor.
- ``ac.py`` — A notional air conditioner flow circuit.

Features
========

- Feature one
- Feature two
- Feature three

Requirements
============

- Python 3.9 or higher
- pip

Installation
============

1. Clone the Repository
-----------------------

.. code-block:: bash

    git clone https://github.com/POEME-Modeling/POEME/tree/docs
    cd poeme

2. Set Up a Virtual Environment
--------------------------------

It is strongly recommended to use a virtual environment to avoid conflicts with other Python projects on your system.

**Create the virtual environment:**

.. code-block:: bash

    python -m venv .venv

**Activate the virtual environment:**

On macOS/Linux:

.. code-block:: bash

    source .venv/bin/activate

On Windows (Command Prompt):

.. code-block:: bash

    .venv\Scripts\activate.bat

On Windows (PowerShell):

.. code-block:: bash

    .venv\Scripts\Activate.ps1

You should see ``(.venv)`` appear at the start of your terminal prompt, confirming the environment is active.

**To deactivate the virtual environment when you're done:**

.. code-block:: bash

    deactivate

3. Install the Package
----------------------

**For regular use**, install the package and its dependencies:

.. code-block:: bash

    pip install .

**For development**, install in editable mode with development dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

Usage
=====

**For usage examples**, see the tests in the ``tests/`` directory.


Project Structure
=================

.. code-block:: text

    poeme/
    ├── LICENSE
    ├── README.rst
    ├── docs/
    ├── pyproject.toml
    ├── src/
    │   └── poeme/
    │       ├── __init__.py
    │       ├── brayton/
    │       ├── core/
    │       ├── electrical/
    │       ├── spring_mass/
    │       └── working/
    └── tests/

Contributing
============

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch (``git checkout -b feature/your-feature-name``)
3. Make your changes
4. Run the tests (``pytest``)
5. Commit your changes (``git commit -m 'Add some feature'``)
6. Push to the branch (``git push origin feature/your-feature-name``)
7. Open a Pull Request

Please make sure your code follows the existing style and that all tests pass before submitting.

Please note: pull requests created solely by AI bots, or pull requests submitted by human accounts but which were clearly written entirely by AI bots will be closed without further action.

License
=======

This project is licensed under the `MIT License <LICENSE>`_.

Contact
=======

Project Link: https://github.com/POEME-Modeling/POEME
