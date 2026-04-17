# ENGINE SYSTEM

A modular, multi-layer engine architecture consisting of:

- `engine_core` — primary engine logic
- `quantum_lantern` — ignition and state engine
- `xyo_layer` — sentinel, archivist, bridge, diviner subsystems
- `scripts` — operational scripts
- `tests` — unit and integration test suite

## Structure

ENGINE/ │ ├── engine_core/ │   └── quantum_lantern/ │ ├── xyo_layer/ │   ├── sentinel/ │   ├── archivist/ │   ├── bridge/ │   └── diviner/ │ ├── scripts/ ├── tests/ └── docs/


## Running Tests

pytest -q
