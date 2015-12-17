===============================
Pythonista Dropbox
===============================



* Free software: ISC license


Non-Pythonista Install
______________________ 

Sometimes it is not convenient to develop Python scripts on an iOS device due to certain limitations.

This package started with the following goals in mind:

* Develop on a non-iOS device and produce Python code that did not have to be altered in any way to run on Pythonista.
* Programatically install the Python code to Pythonista without having to copy and paste except to install the installer.

The adapter.PythonModuleAdapter has accomplished so far the first goal. See the doc string in pythonista_dropbox.adapter. Modules that don't exist on a non-iOS platform can be mocked with this class.

The second goal is accomplished with some altering the gist at pipista_ The pipista module is included in this package. Its altered dropbox counterpart is called dropbox_pipista.py. The dropbox_pipista.py module downloads Python source distribution file files from a given Dropbox path.

After an install, the following command is available at the command line:

* `set-keychain`

  The `set-keychain` command will ask for and set 4 items onto the keyring or keychain:

  + Dropbox account password. 
          
    Entering a Dropbox account password is not necessary. It is simply used to put onto the clipboard for convenient pasting on an iOS device when having to log into Dropbox in the Pythonista web browser.
  + Dropbox application key
  + Dropbox application secret
  + Dropbox OAuth token for use in non-Pythonista environment. This OAuth token may be generated in your Dropbox app control panel. 

   .. Dropbox Apps https://www.dropbox.com/developers/apps




After setting up the keychain with credentials, a client used for accessing a Dropbox account may be used as follows:

::

    from pythonista_dropbox.client import get_client

        client = get_client()
        print client.account_info()
        metadata = client.metadata('/Public')
        print metadata


See tests/test_dropbox_pipista.py for an example of how a Python source distribution file tarball may be installed from a tarball file stored in a Dropbox directory.


Pythonista "install"
____________________


* Inside of the `site-packages` directory create a directory named `pythonista_dropbox`
* Inside of the `site-packages` directory create scripts with the following names and paste the contents from the scripts with the same name from this package:

* pipista.py
* dropbox_pipista.py

Open and run the `pipista.py` script to install the setuptools package.

* Create scripts with the following names and paste the contents from the scripts with the same name from this package. These scripts are in site-packages/pythonista_dropbox

  + adapters.py
  + sensitive_data.py
  + request_auth_token.py
  + client.py
  + __init__.py  (No need to put any contents into this one.)

* Inside of the `pythonista_dropbox` directory create a directory named `client_scripts`

Inside of the `client_scripts` create scripts with the same name and paste the contents of:

   + set_keychain.py

Close and restart Pythonista and run the following scripts inside of `site-packages.pythonista_dropbox.client_scripts` in the following order:

* set_keychain.py
  
You may now install Python source distribution file packages from Dropbox or the PyPi cheese shop.

See the example in tests/test_dropbox_pipista.py

N.B. Since this is impossible to do in an automated fashion, it is difficult to test in a way that is not tedious. Please notify me of anything confusing. "It works for me." makes me cringe. It does work for me and if it doesn't work for you, I likely left out some valuable information. :-)

Features
--------

* Includes a class called PythonistaModuleAdapter that create Pythonista module mockups for developing Python on a desktop computer that then functions in Pythonista in iOS without further modifications.
* Download and install a source distribution into Pythonista from a Dropbox account.
* Download and install pure Python modules from the cheese shop using pipista.py

.. _pipista: https://gist.github.com/pudquick/4116558
