# controller-tester
A simple program made to test the capabilities of `pygame._sdl2.controller` and loading in controller mappings in `pygame-ce`. Feel free to test out your various controllers in this program to see if `pygame-ce` will support them! This program is also intended to determine the best way to interact with external controllers in `pygame-ce`. Please report any interesting findings and/or comments regarding this project and controller/joystick support in `pygame-ce` to the [Pygame Community Discord](https://discord.com/invite/pygame).

# How To Use
Simply download or copy the `controllertest.py` file to your system (optionally also grabbing the `gamecontrollerdb.txt` file). This project was built on Python 3.12.2, but will probably work on earlier versions. Feel free to try out different versions of `pygame`, although `pygame-ce` is recommended. ALWAYS report your SDL version when talking about this project, as SDL adds new controller mappings to their library all the time. You can change what mapping file the program is looking for by editing the code. It should be near the top of the file, pretty obvious.

This program supports hot-plugging and can handle multiple controllers at once. There is a graphical interface where you can cycle through the controllers the system can see and view the state of their axes and buttons. The program will also generate a log file `controllertest.log`, which you can view to see the controllers being added and removed. Setting the main logger's level to `DEBUG` instead of `INFO` will also show the generated `Joystick` events, as well as the actual `Controller` events for axes and buttons.

# Known Issues / Interesting Things
The attributes `id` and `name` of the `Controller` object are not publicly visible in the documentation.

The `Controller` objects seem to only have a `device_index` id and not an `instance_id` id, so removing and adding the same controller again may crash when logger level is set to `DEBUG` or the `Controller` is remapped and generates a `pygame.CONTROLLERDEVICEREMAPPED` event.

No matter what controller mapping file you pass to the program, it doesn't seem to affect anything.
