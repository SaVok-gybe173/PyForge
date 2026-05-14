# PyForge (2D and 3D engine/framework)

PyForge is an engine for creating 2D and 3D games, as well as graphical environments.
**Advantages:**
- Create a window and workspace in a couple of clicks.
- Package all dependencies into a single file (`.pyz` or `.exe`).
- Use OpenGL.

## Installing Dependencies

```bash```
- pip3 install pygame numpy # minimal set
- pip3 install PyOpenGL # for full 3D support

## Script Protection

To protect Python scripts from hacking, we recommend using:
```bash```
- pyarmor pack -e "--onefile" script.py

## Project Structure:

main.py — Create a project using the engine.
update.py — Update the engine to a new version.
info.py — engine information (version, logo, etc.).
init.py — imports all other engine modules.
game_object.py — the Game class for building the engine (runs in the main process).

## Folders:

pygames/ — tools for drawing and creating objects using Pygame (CPU computing).
OpenGL/ — tools for drawing and creating objects using OpenGL (GPU). Recommended for 3D objects with textures.

## Error codes:

Import and initialization (100–109)
- 100 Error importing and initializing
- 101 Error importing a module
- 102 Error importing Pygame
- 103 Error importing NumPy
- 104 Error importing OpenGL
- 105 Error importing .pyd modules
- 106 Error importing .so module
- 107 Error importing dependencies
- 108 Error importing MoviePy
- 109 Error importing OpenCV (cv2)

Runtime errors (200–201)
- 200 Error during runtime
- 201 Error searching for icon

## Version history

```0.1.1```
File name and data structure changes.
Temporarily removed game_client (for future modifications)

```0.1.0```
Added separate modules for import (to avoid overloading the engine).
Example of import changes:
from PyForge.button import Button instead of from PyForge import Button.
The new imports contain the GL version.
The coordinate_transformation function has been added to tools.py to convert coordinates from the range [-1, 1] to screen pixel coordinates.

``0.0.4```
(no details)

```0.0.4.beta-1```
Streams have been added to speed up startup (each scene is loaded separately).
Folder names have been changed.
The first beta version has been released, with scene loading from a JSON file.
Version 0.0.4 is planned to include a server architecture and changes to many classes.
The Button classes and InputLine initializer have been changed.
A camera, free movement within the scene, and rotation have been added to 3D. The shape math class has been changed and recompiled.

```0.0.3```
Bugs from the previous version have been fixed.
New error codes have been added (108, 109, etc.).
Sound handling and the ability to extract sound from video have been added.
New class for playing video with sound.
Separate class for working with sound.
The pougc module has been added to pygames for creating 2D top-down games.
A tools file has been added for debugging and speeding up development (a class and function for working with the mouse).
An installer folder has been created for a custom installer (currently only works with Yandex.Disk; future support will include adding programs to the registry, creating shortcuts, etc.).
The window_transparency module has been added to EaselPy (Windows only) with the set_window_transparency function.
A camera module and model have been added to pygames.
Bugs have been fixed.
Coming soon: a class for working with video and an installer.

```0.0.2```
Reworked main Window class.
Now each scene is executed separately, eliminating the need to create scenes manually.
Scenes can be made dependent on each other.
_scene: list[T | Scene] — stores all scenes.
condition = 0 — active scene number.
The add_scene(*args) function adds scenes at program startup (to the end of the list).
Added set_icon(icon: pg.Surface | str) and set_caption(caption: str | object) methods (separate functions for title and icon removed).
Completely reworked main class, slightly modified Game class.

``0.0.1```
First beta release.