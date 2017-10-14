theforestadmin
==============

Command line tool written on python to setup TheForest Servers


Setup
*****

```python setup.py install```


Server Usage
************

::
    
    ~root# server.py --help
    usage: server.py [-h] [-v] [-c CONFIG_PATH]

    Performs TheForest server operations

    optional arguments:
        -h, --help            show this help message and exit
        -v, --verbose         Activate DEBUG level
        -c CONFIG_PATH, --config_path CONFIG_PATH
                              Path for custom JSON config

    ----- help us on , https://github.com/netzulo/theforestadmin -------

Configuration file
------------------

+ Server script configuration

.. highlight:: json
.. code-block:: json
   :linenos:

::

    {
        "build": {
            "src_path": "",
            "dst_path": "",
            "oxide": {
                "enabled": true,
                "custom": true
            },
            "plugins": false
        }
    }
