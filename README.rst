===============================
Pythonista Dropbox
===============================



* Free software: ISC license

Non-Pythonista Install
______________________ 

Sometimes it is not convenient to develop Python scripts on an iOS device due to certain limitations.

This package started with the following goals in mind:

1. Develop on a non-iOS device and produce Python code that did not have to be altered in any way to run on Pythonista.
  1. Programatically install the Python code to Pythonista without having to copy and paste except to install the installer.

The adapter.PythonModuleAdapter has accomplished so far the first goal. See the doc string in pythonista_dropbox.adapter. Modules that don't exist on a non-iOS platform can be mocked with this class.

The second goal is accomplished with some altering the gist at .. _pipista https://gist.github.com/pudquick/4116558 The pipista module is included in this package. Its altered dropbox counterpart is called dropbox_pipista.py. The dropbox_pipista.py module downloads sdist files from a given Dropbox path.

Features
--------

* Includes a class called PythonistaModuleAdapter that create Pythonista module mockups for developing Python on a desktop computer that then functions in Pythonista in iOS without further modifications.
* Download and install a source distribution into Pythonista from a Dropbox account.
