Installation
========================

Get the Project
------------------------

Choose a directory of your choice, in this case: ``~/dev/tmp``.

.. code-block:: console

    mkdir -p ~/dev/tmp
    cd ~/dev/tmp
    git clone https://github.com/paulross/pprune-threads.git
    cd pprune-threads

Virtual Environment
---------------------

Create a Python 3.13 environment in the directory of your choice, in this case:
``~/dev/tmp/pprune-threads/venv_3.13`` and activate it:

.. code-block:: console

    python3.13 -m venv venv_3.13
    source venv_3.13/bin/activate


Install the Dependencies
---------------------------------

This requires your environment setup correctly so you can talk to PyPi.
Places to look are your environment particularly these files:

.. code-block:: console

    ~/.zshrc

This command can be useful for finding out where pip gets its configuration information from:

.. code-block:: console

    pip config list -v

Then in ``~/dev/tmp/pprune-threads`` with your environment activated:

.. code-block:: console

    pip install -r requirements.txt

Install pprune-threads
---------------------------------

Then in ``~/dev/tmp/pprune-threads`` with your environment activated:

.. code-block:: console

    $ python setup.py develop

Checking the Installation
-------------------------

Then these command line tools should work:

.. code-block:: console

    tiff_metadata_main -h
    tiff_metadata_psql -h
    tiff_copy -h

Running the Tests
-----------------------

You now should be able to run the following commands successfully in
``~/dev/tmp/pprune-threads`` with your environment activated:

.. code-block:: console

    pytest tests/

If you get errors check which ``pytest`` is being picked up with ``which pytest``.
It should be in ``~/dev/tmp/pprune-threads/venv_3.13/bin/``.

If not you will have to specify it, in ``~/dev/tmp/pprune-threads``:

.. code-block:: console

     ./venv_3.13/bin/pytest tests

Running the AWS Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some tests are ignored as they tests the AWS performance and take quite a while.
To run these you need to be logged in to AWS.
Then use the ``--runslow`` option, you can also use ``-vs`` to see more information about the test output.

.. code-block:: console

     ./venv_3.13/bin/pytest tests --runslow -vs

These tests make ever increasing GET requests (up to 256MB) and time the response which can give an
idea of the latency and bandwidth of the connection.

For example:

.. code-block:: console

    tests/integration/test_int_aws_network.py::test_aws_network[00000-00000-         4] Ctor: 0.632810 Greedy:        0 Seek[       0]: 0.000004 Read [         4]: 0.433745
    tests/integration/test_int_aws_network.py::test_aws_network[00000-00000-         8] Ctor: 0.410112 Greedy:        0 Seek[       0]: 0.000005 Read [         8]: 0.413042
    tests/integration/test_int_aws_network.py::test_aws_network[00000-00000-        16] Ctor: 0.440343 Greedy:        0 Seek[       0]: 0.000004 Read [        16]: 0.400409
    8<---- Snip ---->8
    tests/integration/test_int_aws_network.py::test_aws_network[00000-00000-  67108864] Ctor: 0.464835 Greedy:        0 Seek[       0]: 0.000005 Read [  67108864]: 45.837576
    tests/integration/test_int_aws_network.py::test_aws_network[00000-00000- 134217728] Ctor: 0.441072 Greedy:        0 Seek[       0]: 0.000004 Read [ 134217728]: 78.228387
    tests/integration/test_int_aws_network.py::test_aws_network[00000-00000- 268435456] Ctor: 0.494413 Greedy:        0 Seek[       0]: 0.000006 Read [ 268435456]: 140.024657


Trying Your Installation Against Images
----------------------------------------------

Local Images
^^^^^^^^^^^^^^^^^^^^

There are some test images in the distribution.
These commands allow you to explore the image:

.. code-block:: console

    tiff_metadata_main tests/images/CMU-1_IFD_6-8.tiff --dump
    tiff_metadata_main tests/images/CMU-1_IFD_6-8.tiff --dump --columns --tags=254,255,256,257,259,274,277,278,282,283,296,306,322,323
    tiff_metadata_main tests/images/ --dump-statistics

Images on AWS
^^^^^^^^^^^^^^^^^^^^

To run this you need to be logged in to AWS.
For example this is a 7Gb file:

.. code-block:: console

    tiff_metadata_main s3://d1dcd571d773fc5b655f2e48e230d83e --dump

At the end there should be a summary of each IFD:

.. code-block:: console

    ...
    2023.13-20 10:46:02,294 -  tiff_metadata_output.py#924  - INFO     - IFD    0 W  221,292 L   88,821   19,655,376,732 ( 18.3 Gi) pixels   58,966,130,196 ( 54.9 Gi) bytes (decompressed).
    2023.13-20 10:46:02,294 -  tiff_metadata_output.py#924  - INFO     - IFD    1 W    1,024 L      411          420,864 (411.0 Ki) pixels        1,262,592 (  1.2 Mi) bytes (decompressed).
    2023.13-20 10:46:02,294 -  tiff_metadata_output.py#924  - INFO     - IFD    2 W  221,292 L   88,821   19,655,376,732 ( 18.3 Gi) pixels   58,966,130,196 ( 54.9 Gi) bytes (decompressed).
    2023.13-20 10:46:02,294 -  tiff_metadata_output.py#924  - INFO     - IFD    3 W  166,030 L   77,259   12,827,311,770 ( 11.9 Gi) pixels   38,481,935,310 ( 35.8 Gi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD    4 W   55,323 L   22,205    1,228,447,215 (  1.1 Gi) pixels    3,685,341,645 (  3.4 Gi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD    5 W   55,323 L   22,205    1,228,447,215 (  1.1 Gi) pixels    3,685,341,645 (  3.4 Gi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD    6 W   41,507 L   19,314      801,666,198 (764.5 Mi) pixels    2,404,998,594 (  2.2 Gi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD    7 W   13,830 L    5,551       76,770,330 ( 73.2 Mi) pixels      230,310,990 (219.6 Mi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD    8 W   13,830 L    5,551       76,770,330 ( 73.2 Mi) pixels      230,310,990 (219.6 Mi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD    9 W   10,376 L    4,828       50,095,328 ( 47.8 Mi) pixels      150,285,984 (143.3 Mi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD   10 W    3,457 L    1,387        4,794,859 (  4.6 Mi) pixels       14,384,577 ( 13.7 Mi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD   11 W    3,457 L    1,387        4,794,859 (  4.6 Mi) pixels       14,384,577 ( 13.7 Mi) bytes (decompressed).
    2023.13-20 10:46:02,295 -  tiff_metadata_output.py#924  - INFO     - IFD   12 W    2,594 L    1,207        3,130,958 (  3.0 Mi) pixels        9,392,874 (  9.0 Mi) bytes (decompressed).
    2023.13-20 10:46:02,295 -    tiff_metadata_main.py#419  - INFO     - tiff_analyse_AWS_file: File size: 7285630466 Time: 30.472403 (s) File: d1dcd571d773fc5b655f2e48e230d83e
    2023.13-20 10:46:02,295 -    tiff_metadata_main.py#486  - INFO     - Overall: Errors: 0 Files: 1 IFDs: 13 Execution time: 30,472.512 (ms) 30,472.512 (ms/file)

Have a look at the heatmap for IFD 0 (18 Giga-pixels):

.. code-block:: console

    tiff_metadata_main s3://d1dcd571d773fc5b655f2e48e230d83e --dump-tile-bytes-sizes --dump-heatmap --dump-heatmap-style=Purples --ifds=0
