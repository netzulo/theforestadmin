theforestadmin
==============

Command line tool written on python to setup TheForest Servers


Setup
*****

``python setup.py install``


Server Usage
************

::
    
    usage: server.py [-h] [-v] [-c CONFIG_PATH]

    Performs TheForest server operations

    optional arguments:
        -h, --help            show this help message and exit
        -v, --verbose         Activate DEBUG level
        -c CONFIG_PATH, --config_path CONFIG_PATH
                              Path for custom JSON config
        -d, --deploy          Deploy new server based on JSON config
        -s, --start           Start server based on JSON config

    ----- help us on , https://github.com/netzulo/theforestadmin -------

Configuration file
------------------

+ Server script configuration

.. highlight:: json
.. code-block:: json
   :linenos:

::

    {
        "server_path": "d:\\0.programms\\Steam\\steamapps\\common\\TheForestDedicatedServer\\",
        "modules": {
            "steam":{ "name": "Steam", "enabled": true },
            "oxide":{ "name": "Oxide", "enabled": true, "custom": true },
            "plugins":{ "name": "Plugins", "enabled": false }
        },
        "options":[
            "-serverip \"0.0.0.0\"",
            "-serversteamport 27015",
            "-servergameport 27015",
            "-serverqueryport 27016",
            "-servername  \"[24/7][max:100]netzulo.com\"",
            "-serverplayers 100",
            "-serverpassword \"\"",
            "-serverpassword_admin \"0123456789\"",
            "-serversteamaccount \"\"",        
            "-serverAutoSaveInterval 15",
            "-difficulty Normal",
            "-initType New",
            "-slot 1",
            "-enableVAC on",
            "-showLogs on",
            "-serverContact \"netzuleando@gmail.com\""
        ]
    }

