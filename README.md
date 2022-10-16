# Godot binary serialization API to Python

Serialize and deserialize Godot types between GDScript and Python using binary format compatible with Godot's Binary serialization API.

Code compatible with *Godot Engine 4.0 beta* and with *Godot Engine 3.5 stable*.


## Modules

There are two main modules `gdtype.binaryapiv4` and `gdtype.binaryapiv3`. First one is dedicated for handling data compatible with Godot 4. 
Second one is dedicated for Godot 4.

Both modules profide following functions:
- `def deserialize( message: bytes )` deserializing data provided by Godot to Python counterpart
- `def serialize( value ) -> bytes` serializing Python data representation to Godot binary format

For more details see those modules.


## Use example

Library is useful is case of communicating with GDScript using Python, for example when game expose API through network interface.

Sending variant over network using `GDScript`:
```gdscript
var stream: StreamPeer
var data
## initialize data and stream
stream.put_var( data )
## ...
var data2 = stream.get_var()
## handle new data
```


Deserialization in `Python` can be done as follows:
```python
from gdtype.binaryapiv4 as binaryapi

rawData: bytes = None
# receive bytes (e.g. from network or file)
gdObject = binaryapi.deserialize( rawData )
## change gdObject
rawData = binaryapi.serialize( gdObject )
## send or store rawData
```


## Installation

Installation does not require special preparation. Simply copy `src/gdtype` directory into your project directory tree and import it in script.


## Running tests

Checking library functionality can be done by executing one of following scripts:
- `./src/testgdtype/runtests.py` for executing unit tests
- `./test/run_tests_v3.sh` for executing integration tests using Godot v3
- `./test/run_tests_v4.sh` for executing integration tests using Godot v4
- `./test/samples.sh` for generating samples using Godot

All tests can be run using `./test/run_all_tests.sh`.


## Known issues

Module internally uses `type()` for finding proper serialization and deserialization functions. It can lead to serialization error `unable to serialize data`.
Error occurs if all conditions meet:
- `gdtype` package placed as subpackage,
- `sys.path` is altered (can happen in case of running scripts from within package tree)
-  `gdtype` is imported in more than one module in inconsistent manner:
    - `from mainpackage.gdtype import binaryapiv4 as binaryapi`
    - `import gdtype.binaryapiv4 as binaryapi`
- `gdtype` structure is initialized in one module and serialized in the other
As result `gdtype` will be imported twice with different *namespaces* and incompatible configurations.

To prevent the situation do one of:
- do not alter `sys.path` (interpreter will not allow to import `gdtype` in inconsistent way)
- wrap whole serialization/deserialization functionality in one module
- keep imports consistent


## Examples of not obvious mechanisms

- running GDScript scripts from command line (`./test/run_tests_v4.sh`)
- `main`-like structure of GDScript (`./test/lib/v4/gd_tests_v4.gd`)


## References

- [Godot Binary serialization API (latest)](https://docs.godotengine.org/en/latest/tutorials/io/binary_serialization_api.html)
- [Godot Binary serialization API (stable)](https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html)
