# controller-tester
A simple program you can use to test out controller functionality and controller mappings for `pygame-ce`.

This program is also intended to determine the best way to interact with controllers in `pygame-ce`. Please report any interesting findings and/or comments regarding this project and controller/joystick support in `pygame-ce` to the [Pygame Community Discord](https://discord.com/invite/pygame).

## How To Use
Simply download or copy the `controllertest.py` file to your system (optionally also grabbing the `gamecontrollerdb.txt` file). This project was built on Python 3.12.2, but will probably work on earlier versions. Feel free to try out different versions of `pygame-ce`. You can change what mapping file the program is looking for by editing the code. It should be near the top of the file and be pretty obvious.

This program supports hot-plugging and can handle multiple controllers at once. There is a graphical interface where you can cycle through the controllers the system can see and view the state of their axes and buttons. The program will also generate a log file `controllertest.log`, which you can view to see the controllers being added and removed. Setting the main logger's level to `DEBUG` instead of `INFO` will also show the generated `Joystick` events, as well as the `Controller` events for axis and button updates.

## Known Issues / Interesting Things
`Controller.id` is the device index, not the instance id, so it is unreliable after devices have been added and removed. There is no other `id` to use however, so `Controllers` may behave strangely after having been removed and re-added. The events generated by an "invisible" `Controller` will have the ID of `??` and the name of `UNKNOWN`.

Controller mapping files only seem to work if the GUID is exactly the GUID of your `Controller` device, making them impractical.

## Proposed `pygame._sdl2.controller` Changes
- Document `Controller.id` and `Controller.name`
- Document `pygame.CONTROLLERDEVICEADDED.guid`
- Add `get_guid()` method or read-only `guid` attribute to `Controller` (currently only available through `pygame.CONTROLLERDEVICEADDED.guid`)
- Add `instance_id` functionality to `Controller` like in `Joystick` (`Controller.id` is the device index, unreliable after devices have been added and removed)
