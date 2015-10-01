UI Application for camptocamp.org v6
====================================

Checkout
--------

    git clone https://github.com/c2corg/v6_ui.git

Build
-----

    cd v6_ui
    make -f config/{user} install

Run the application
-------------------

    make -f config/{user} serve

Open your browser at http://localhost:6543/ or http://localhost:6543/?debug (debug mode). Make sure you are
using the port that is set in `config/{user}`.

Available actions may be listed using:

    make help

Run the tests
--------------

    make -f config/{user} test
    
Or with the `check` target, which runs `flake8` and `test`:

    make -f config/{user} check

To run a specific test:

    .build/venv/bin/nosetests c2corg_ui/tests/views/test_summit.py

To see the debug output:

    .build/venv/bin/nosetests -s

Developer Tips
--------------

The UI is mainly built using the following components:
* Pyramid (Python framework) http://docs.pylonsproject.org/en/latest/
