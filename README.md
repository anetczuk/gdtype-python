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


## References

- Godot Binary serialization API (https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html)
