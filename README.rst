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

The second goal is accomplished with some altering the gist at .. _pipista https://gist.github.com/pudquick/4116558 The pipista module is included in this package. Its altered dropbox counterpart is called dropbox_pipista.py. The dropbox_pipista.py module downloads sdist files from a given Dropbox path.

After an install, the following two commands are available at the command line:

* `set-keychain`
* `request-auth-token`

  This command will ask for and set 3 items onto the keyring or keychain:

  + Dropbox account password. 
          
        It is not necessary and is used to put onto the clipboard for convenient pasting on an iOS device when having to log into Dropbox in the Pythonista web browser.

  + Dropbox application key
  + Dropbox application secret


Using the authorization data that has been set after running `set-keychain`, this will take the user through the process of obtaining an authorization token from Dropbox and setting the access token key and secret onto the keyring or keychain. 

  On a desktop, url may be copied and pasted into a browser. On an iOS device, Pythonista's web browser is opened with the generated authorization url.

  On an iOS device the following two scripts may be run to accomplish the same task.

  client_scripts
  ├── set_access_key_and_secret.py
  ├── set_keychain.py


After setting up the keychain with credentials, a client used for accessing a Dropbox account may be used as follows:

  ::

        from pythonista_dropbox.client import get_client

        client = get_client()
        print client.account_info()
        metadata = client.metadata('/Public')
        print metadata


See tests/test_dropbox_pipista.py for an example of how a sdist tarball may be installed from a tarball file stored in a Dropbox directory.


Pythonista "install"
____________________


* Inside of the `site-packages` directory create a directory named `pythonista_dropbox`
* Inside of the `site-pacages` directory create scripts with the following names and paste the contents from the scripts with the same name from this package:

    * pipista.py
    * dropbox_pipista.py

Open and run the `pipista.py` script to install the setuptools package.

* Inside of the `pythonista_dropbox` directory create a directory named `client_scripts`
* Create scripts with the following names and paste the contents from the scripts with the same name from this package:

        * adapters.py
        * sensitive_data.py
        * request_auth_token.py
        * client.py
        * __init__.py  (No need to put any contents into this one.)

Close and restart Pythonista and run the scripts in side of `site-packages.pythonista_dropbox.client_scripts` in the following order:

    * set_keychain.py
    * set_access_key_and_secret.py


You may now install sdist packages from Dropbox or the PyPi cheese shop.

See the example in tests/test_dropbox_pipista.py



Features
--------

* Includes a class called PythonistaModuleAdapter that create Pythonista module mockups for developing Python on a desktop computer that then functions in Pythonista in iOS without further modifications.
* Download and install a source distribution into Pythonista from a Dropbox account.
* Download and install pure Python modules from the cheese shop using pipista.py



