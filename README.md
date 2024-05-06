# controller-tester
A simple program you can use to test out controller functionality and controller mappings for `pygame._sdl2.controller` for `pygame-ce`.

## Goals / Intentions
This program was developed with the following intentions:
- Test different controllers to determine if they are recognized and/or accurate
- Test different controller mapping files/strings
- Research and improve the API for the `controller` module
- Determine the best ways to interact with controllers using the `controller` module
- Compare and contrast the `pygame.controller` module with the `pygame.joystick` module

Interested in controller support for `pygame-ce`? Join the [Pygame Community Discord](https://discord.com/invite/pygame)!

## How To Use
Simply download or copy the `controllertest.py` file to your system (optionally also grabbing the `gamecontrollerdb.txt` file). This project was built on Python 3.12.2, but will probably work on earlier versions. Feel free to try out different versions of `pygame-ce` and SDL to see what changes. The included database is there for testing purposes and can be found [here](https://github.com/mdqinc/SDL_GameControllerDB).

This program supports hot-plugging and can handle multiple controllers at once. There is a graphical interface where you can cycle through the controllers the system can see and view the state of their axes and buttons. The program will also generate a log file `controllertest.log`, which you can view to see the controllers being added and removed. Setting the main logger's level to `DEBUG` instead of `INFO` will also show the generated `Joystick` events, as well as the `Controller` events for axis and button updates.

## `Joystick` vs `Controller`
The `joystick` and `controller` modules are separate APIs that are not easily combined. For the time being, it is not recommended to try and blend them together into a comprehensive package to try and get the best of both worlds. The `controller` module is marked EXPERIMENTAL and is therefore unstable. It is one of the goals of this project to improve the API and make `controller` a more viable tool for use in `pygame-ce` programs.

The `joystick` module is a stable, flexible API for detecting and getting input from external controller devices. It has comprehensive documentation and tutorials available online. Its one major flaw is the lack of mapping support. Each device only declares the number of axes, buttons, hats (d-pads), and track balls it has and it is up to the application to decide what to do with something like "Button 3 down". This means that each application must create a new mapping for each new controller device it comes across, which is tedious for the user (to map their device) and the programmer (to program a mapping tool). A community-sourced database of mappings would be tedious to implement, as well as unnecessary due to the existence of the `controller` module.

The `controller` module is an experimental, in development API built over `joystick` for mapping controllers with standard layouts. The documentation is lacking and tutorials are practically non-existent. The `Controller` objects only support axes and buttons. Track balls are not available and hats (d-pads) are split into four separate buttons. This greatly simplifies the API and actually makes it easier on the programmer. `Controllers` provide easy mapping support, and their events look like "Button A down". Most standard layout controllers work with `controller` and won't need to be remapped. The module itself has several issues that make programming around it more difficult than it needs to be, but hopefully that will change in the near future. SDL itself adds new controller mappings to its internal database consistently, so controller support will only get better.

If you want to support a wide variety of gamepad devices and don't care about easy mapping functionality, `joystick` is the way to go. If you don't want to worry about all the manual setup needed for mapping and don't mind the weird API, you should use `controller`. ALthough `joystick` has better documentation, `controller` is easier to set up and use out of the box if you aren't going to add mapping and only care about supporting the basic gamepads registered by SDL.

## Guidelines for Gamepad Development
- Always make gamepad usage completely OPTIONAL. Your application should work just fine with only the mouse and keyboard.
- Always provide a mapping tool to reconfigure joysticks. "Button 0" isn't always the "Primary Action Button".
- Provide a remapping tool for controllers. Even if this is a simple json file, letting your users remap their controllers goes a long way.
- Provide a mapping tool for turning joysticks into controllers. You can piggyback functionality from your conroller remapping file, as they are essentially the same thing.
- Disconnecting an in-use gamepad should pause the game to avoid accidental disconnects causing player helplessness.
- Navigating menus should be possible with analog sticks, d-pads, and mouse/keyboard.
- The on-screen icons should match the gamepad being used. The only way to detect the button icons is to infer it from the system name of the gamepad, which isn't reliable, so applications should also provide a setting to change the icons globally. This is more of an optional polish feature.

## Guide to `controller` Development
`Controller.id` is the device index, not the instance id, so it is unreliable after devices have been added and removed. The only way to get the instance id is from a `pygame.CONTROLLERDEVICE*` event. Using `Controller.set_mapping()` generates a `pygame.CONTROLLERDEVICEREMAPPED` event, so we can work around this issue and make controllers reliable even after device swapping. This program showcases one way to do this, by using a `pending_controllers: list[pygame._sdl2.controller.Controller]` object and a `controllers: dict[int, pygame._sdl2.controller.Controller]` object. When a `pygame.CONTROLLERDEVICEADDED` event is dispatched, create a `Controller` object using the `device_index` attribute of the event, and add that controller to `pending_controllers`. Then, call `Controller.get_mapping(Controller.set_mapping())`. This will not change the controller's mapping, but will still generate the `pygame.CONTROLLERDEVICEREMAPPED` event. When handling that event, check to see if the event's `instance_id` is a key in `controllers`. If not, pop the first element of `pending_controllers` and set `controllers[event.instance_id] = pending_controllers.pop(0)`. Keep in mind that controllers will generate a `pygame.CONTROLLERDEVICEREMAPPED` event for every instance id they once had, so `pending_controllers` is not guaranteed to have a controller inside when `pygame.CONTROLLERDEVICEREMAPPED` events generate with instance ids not in `controllers`. These extra remap events can simply be discarded. See the code to see all of this in action.

Update: `Controller.from_joystick().get_instance_id()` can be used to get the instance id of any `Controller` object. The previous method will remain in this README and the code for demonstration purposes.

Controller mapping files/strings only seem to work when the GUID in the mapping exactly matches the controller, making them only useful for local mappings/remappings.

You can get the GUID of a `Controller` by reading the `pygame.CONTROLLERDEVICEADDED.guid` attribute or using `Controller.as_joystick().get_guid()`.

The only way to check for rumble support is to call the `Controller.rumble` method, which returns a boolean value indicating whether the effect was played successfully. Calling `rumble` with intensity values of zero will always return True. This indicator value isn't always accurate, and can even return different values when called with the same arguments. Thankfully, most programs won't need to check for rumble support and can just fire away `Controller.rumble()` calls without worrying about whether or not the given `Controller` supports it.

## Proposed `pygame._sdl2.controller` Changes
- Document `Controller.id` and `Controller.name`
- Document `pygame.CONTROLLERDEVICEADDED.guid`
- Add `get_guid()` method or read-only `guid` attribute to `Controller` (currently only available through `pygame.CONTROLLERDEVICEADDED.guid` and `Controller.as_joystick().get_guid()`)
- Add `instance_id` functionality to `Controller` like in `Joystick` (`Controller.id` is the device index, unreliable after devices have been added and removed)
- Add button layout/icon information to `Controller` (it seems to be supported in the SDL source code) (this is a non-essential quality of life feature)
