**********
Quickstart
**********

.. role:: python(code)
    :language: python

Using the Code
--------------
With the necessary modules installed the code can be used from directly by typing the following commands in kriging directory instead of using the GUI

.. code:: python

    run kriging.py

This enables you to access all the functions in that file. A csv file can be loaded to train the data in the following way

.. code:: python

    train_model(path/to/save/model, path/to/training/data) 

Currently only csv files are supported for all the training data files and also the model files. So give in any csv files to the model and training data files. You can see the progress of the model in the terminal due to the print statements

.. code:: python