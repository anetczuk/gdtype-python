# Godot binary serialization API to Python

Serialize and deserialize Godot types between GDScript and Python using binary format compatible with Godot's Binary serialization API.

Code compatible with *Godot 4.0 beta*.

## Use case

Library is useful is case of communicating with GDScript using Python, for example when game expose API through network interface.

Sending variant over network using `GDScript`:
```gdscript
var stream: StreamPeer
var data
# ...
stream.put_var( data )
```


Deserialization in `Python` can be done as follows:
```python
rawData: bytes = None
# ...
gdObject = gdtype.deserialize( rawData )
```


## Running tests

Checking library functionality can be done by executing one of following scripts:
- `./src/testgdtype/runtests.py` for executing unit tests
- `./test/run_tests.sh` for executing integration tests using Godot
- `./test/samples.sh` for generating samples using Godot


## References

- [Godot Binary serialization API (stable)](https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html)
