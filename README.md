# controller-tester
A simple program you can use to test out controller functionality and controller mappings for `pygame._sdl2.controller` for `pygame-ce`.

## Goals / Intentions
This program was developed with the following intentions:
- Test different controllers to determine if they are recognized and/or accurate
- Test different controller mapping files
- Research and improve the API for the `controller` module
- Determine the best ways to interact with controllers using the `controller` module
- Compare and contrast the `pygame.controller` module with the `pygame.joystick` module

Interested in controller support for `pygame-ce`? Join the [Pygame Community Discord](https://discord.com/invite/pygame)!

## How To Use
Simply download or copy the `controllertest.py` file to your system (optionally also grabbing the `gamecontrollerdb.txt` file). This project was built on Python 3.12.2, but will probably work on earlier versions. Feel free to try out different versions of `pygame-ce`. You can change what mapping file the program is looking for by editing the code. It should be near the top of the file and be pretty obvious.

This program supports hot-plugging and can handle multiple controllers at once. There is a graphical interface where you can cycle through the controllers the system can see and view the state of their axes and buttons. The program will also generate a log file `controllertest.log`, which you can view to see the controllers being added and removed. Setting the main logger's level to `DEBUG` instead of `INFO` will also show the generated `Joystick` events, as well as the `Controller` events for axis and button updates.

## Known Issues / Interesting Things
`Controller.id` is the device index, not the instance id, so it is unreliable after devices have been added and removed. This program works around that by forcing a `pygame.CONTROLLERDEVICEREMAPPED` event (which has the instance id) by using `Controller.set_mapping(Controller.get_mapping())`. Controllers reside in a pending list until the remap event happens. View the code to see how it works.

Controllers that have been removed and re-added will generate `CONTROLLERDEVICEREMAPPED` events for each instance id they once had. If a controller is plugged in three times, it will generate three remap events with each of its previous instance ids.

Controller mapping files only seem to work if the GUID is exactly the GUID of your `Controller` device, making them impractical.

The only way to check for rumble support is to call the `Controller.rumble` method, which returns a boolean value indicating whether the effect was played successfully. Calling `rumble` with intensity values of zero will always return True. This indicator value isn't always accurate, and can even return different values when called with the same arguments. Thankfully, most programs won't need to check for rumble support.

The `Controller.rumble()` method appears to change to a different method internally? Sometimes Pycharm will mark the signature as `*args, **kwargs`. More testing is required.

## Proposed `pygame._sdl2.controller` Changes
- Document `Controller.id` and `Controller.name`
- Document `pygame.CONTROLLERDEVICEADDED.guid`
- Add `get_guid()` method or read-only `guid` attribute to `Controller` (currently only available through `pygame.CONTROLLERDEVICEADDED.guid`)
- Add `instance_id` functionality to `Controller` like in `Joystick` (`Controller.id` is the device index, unreliable after devices have been added and removed)
