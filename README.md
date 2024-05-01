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

The `controller` module is an experimental, in development API built over `joystick` for mapping controllers with standard layouts. The documentation is lacking and tutorials are practically non-existent. The `Controller` objects only support axes and buttons. Track balls are not available and hats (d-pads) are split into four separate buttons. This greatly simplifies the API and actually makes it easier on the programmer. `Controllers` provide easy mapping support, and their events look like "Button X down". Most standard layout controllers work with `controller` and won't need to be remapped. The module itself has several issues that make programming around it more difficult than it needs to be, but hopefully that will change in the near future. SDL itself adds new controller mappings to its internal database consistently, so controller support will only get better.

## Guidelines for Development
- Always make gamepad usage completely OPTIONAL. Your application should work just fine with only the mouse and keyboard.
- Always provide a mapping tool to reconfigure the gamepads.
- Disconnecting an in-use gamepad should pause the game to avoid accidental disconnects causing player helplessness.
- Navigating menus should be possible with analog sticks, d-pads, and mouse/keyboard.
- The on-screen icons should match the gamepad being used. The only way to detect the button icons is to infer it from the system name of the gamepad, which isn't reliable, so applications should also provide a setting to change the icons globally.

## Known Issues / Interesting Things
`Controller.id` is the device index, not the instance id, so it is unreliable after devices have been added and removed. This program works around that by forcing a `pygame.CONTROLLERDEVICEREMAPPED` event (which has the instance id) by using `Controller.set_mapping(Controller.get_mapping())`. Controllers reside in a pending list until the remap event happens. View the code to see how it works.

Controllers that have been removed and re-added will generate `CONTROLLERDEVICEREMAPPED` events for each instance id they once had. If a controller is plugged in three times, it will generate three remap events with each of its previous instance ids.

Controller mapping files only seem to work if the GUID is exactly the GUID of your `Controller` device, making them impractical.

The only way to check for rumble support is to call the `Controller.rumble` method, which returns a boolean value indicating whether the effect was played successfully. Calling `rumble` with intensity values of zero will always return True. This indicator value isn't always accurate, and can even return different values when called with the same arguments. Thankfully, most programs won't need to check for rumble support.

## Proposed `pygame._sdl2.controller` Changes
- Document `Controller.id` and `Controller.name`
- Document `pygame.CONTROLLERDEVICEADDED.guid`
- Add `get_guid()` method or read-only `guid` attribute to `Controller` (currently only available through `pygame.CONTROLLERDEVICEADDED.guid`)
- Add `instance_id` functionality to `Controller` like in `Joystick` (`Controller.id` is the device index, unreliable after devices have been added and removed)
- Add button layout information to `Controller` (it seems to be supported in the SDL source code)
