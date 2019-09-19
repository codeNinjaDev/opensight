# OpenSight: The all-in-one opensource vision package for FRC

## About


## How it works
The main components of the OpenSight Vision framework are the *modules* and the *manager*. 
In short, vision *modules* are connected to each other to form a vision pipeline used to detect and track vision targets. The software that binds them together in the backend is called the *manager*, while the raw footage from the camera comes from the *Camera Server*.

### Modules
The modules determine what the vision pipeline tracks and to what extent. OpenSight Modules take after cv image operations, allowing the user to have much greater control over the vision pipeline
