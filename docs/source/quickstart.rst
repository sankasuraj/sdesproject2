**********
Quickstart
**********

.. role:: python(code)
    :language: python

**Using the Code**

With the necessary modules installed the code can be used from directly by typing the following commands in kriging directory instead of using the GUI

.. code:: python

    run kriging.py

This enables you to access all the functions in that file. A csv file can be loaded to train the data in the following way

.. code:: python

    train_model(path/to/save/model, path/to/training/data) 

Currently only csv files are supported for all the training data files and also the model files. So give in any csv files to the model and training data files. You can see the progress of the model in the terminal due to the print statements. After this is done you can see if the model is in the given place as required. To use the model to find values of y for a given x_data the following command can be used

.. code:: python

    find_values(path/to/model, path/to/x_data, path/to/save/y_data)


.. This will generate the y_data at a given x_data by using the model which has to be previously trained using data with number of dimensions equal to the dimension of x_data. The required y_data can be found in the mentioned path. 

**Note:**
 
 - Please only mention valid .csv files for all the inputs
 - While training the data the code automatically takes x dimension as n-1 and y dimension as 1 where n is the total number of columns in the training data