#!/usr/bin/env python3
import os
import sys
import logging

import pygame as pg
import pygame._sdl2.controller as pgc

logger = logging.getLogger(__name__)
logging.basicConfig(filename="controllertest.log", filemode="w", level=logging.INFO)

# Must be set before initializing modules.
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


def add_mappings(filename: str):
    """Set the gamepad mappings config file to the given filename."""
    os.environ["SDL_GAMECONTROLLERCONFIG_FILE"] = os.path.join(os.getcwd(), filename)


add_mappings("gamecontrollerdb.txt")

pg.init()
pgc.init()


AXIS_NAMES = {
    pg.CONTROLLER_AXIS_LEFTX: "Left_X",
    pg.CONTROLLER_AXIS_LEFTY: "Left_Y",
    pg.CONTROLLER_AXIS_RIGHTX: "Right_X",
    pg.CONTROLLER_AXIS_RIGHTY: "Right_Y",
    pg.CONTROLLER_AXIS_TRIGGERLEFT: "L_Trigger",
    pg.CONTROLLER_AXIS_TRIGGERRIGHT: "R_Trigger",
}

BUTTON_NAMES = {
    pg.CONTROLLER_BUTTON_A: "A",
    pg.CONTROLLER_BUTTON_B: "B",
    pg.CONTROLLER_BUTTON_X: "X",
    pg.CONTROLLER_BUTTON_Y: "Y",
    pg.CONTROLLER_BUTTON_BACK: "BACK",
    pg.CONTROLLER_BUTTON_GUIDE: "GUIDE",
    pg.CONTROLLER_BUTTON_START: "START",
    pg.CONTROLLER_BUTTON_LEFTSTICK: "L_STICK",
    pg.CONTROLLER_BUTTON_RIGHTSTICK: "R_STICK",
    pg.CONTROLLER_BUTTON_LEFTSHOULDER: "L_SHOULDER",
    pg.CONTROLLER_BUTTON_RIGHTSHOULDER: "R_SHOULDER",
    pg.CONTROLLER_BUTTON_DPAD_UP: "UP",
    pg.CONTROLLER_BUTTON_DPAD_DOWN: "DOWN",
    pg.CONTROLLER_BUTTON_DPAD_LEFT: "LEFT",
    pg.CONTROLLER_BUTTON_DPAD_RIGHT: "RIGHT",
}


def main():
    logger.info("Program started.")
    logger.info(f"pygame{"-ce" if getattr(pg, "IS_CE", False) else ""} v{pg.version.vernum} SDL v{pg.version.SDL}")
    pg.display.set_caption("Controller Testing")
    screen = pg.display.set_mode((500, 500))
    clock = pg.time.Clock()
    font = pg.Font(None, 25)

    controllers: dict[int, pgc.Controller] = {}
    rumbles: dict[int, bool] = {}
    display_index: int = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                logger.info("Program ended.")
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    logger.info("Program ended.")
                    pg.quit()
                    sys.exit()
                if event.key in (pg.K_RIGHT, pg.K_UP):
                    display_index += 1
                    display_index %= len(controllers)
                if event.key in (pg.K_LEFT, pg.K_RIGHT):
                    display_index -= 1
                    display_index %= len(controllers)

            if event.type == pg.JOYDEVICEADDED:
                if pgc.is_controller(event.device_index):
                    logger.debug(f"Joystick ID-{event.device_index} added (Controller).")
                else:
                    logger.info(f"Joystick ID-{event.device_index} added (Joystick).")
                    logger.info("Attempting to convert bad Joystick...")
                    try:
                        c = pgc.Controller.from_joystick(pg.Joystick(event.device_index))
                        rumble = c.rumble(0.7, 0.7, 500)
                        logger.info(f"Converted ID-{c.id} \"{c.name}\". Rumble: {rumble}")
                        logger.info(f"Mapping: {c.get_mapping()}")
                    except Exception as ex:
                        logger.warning(f"Error {ex.__class__}: {ex}")

            if event.type == pg.JOYDEVICEREMOVED:
                logger.debug(f"Joystick ID-{event.instance_id} removed.")
            if event.type == pg.JOYAXISMOTION:
                logger.debug(f"Joystick ID-{event.instance_id} Axis {event.axis}: {event.value}")
            if event.type == pg.JOYHATMOTION:
                logger.debug(f"Joystick ID-{event.instance_id} Hat {event.hat}: {event.value}")
            if event.type == pg.JOYBALLMOTION:
                logger.debug(f"Joystick ID-{event.instance_id} Ball {event.ball}: {event.rel}")
            if event.type == pg.JOYBUTTONDOWN:
                logger.debug(f"Joystick ID-{event.instance_id} Button {event.button}: down")
            if event.type == pg.JOYBUTTONUP:
                logger.debug(f"Joystick ID-{event.instance_id} Button {event.button}: up")

            if event.type == pg.CONTROLLERDEVICEADDED:
                try:
                    c = pgc.Controller(event.device_index)
                except Exception as ex:
                    logger.warning(f"Controller ID-{event.device_index} could not be initialized.")
                    logger.warning(f"Error {ex.__class__}: {ex}")
                    continue
                controllers[c.id] = c
                rumbles[c.id] = c.rumble(0.7, 0.7, 500)
                logger.info(f"Controller ID-{c.id} \"{c.name}\" added. Rumble: {rumbles[c.id]}")
                logger.info(f"Mapping: {c.get_mapping()}")

            if event.type == pg.CONTROLLERDEVICEREMOVED:
                if event.instance_id in controllers:
                    c = controllers[event.instance_id]
                    logger.info(f"Controller ID-{c.id} \"{c.name}\" removed.")
                    del controllers[c.id]
                    del rumbles[c.id]
                    if len(controllers):
                        display_index %= len(controllers)
                    else:
                        display_index = 0
                else:
                    logger.info("Controller ID-?? \"UNKNOWN\" removed.")

            if event.type == pg.CONTROLLERDEVICEREMAPPED:
                c = controllers[event.instance_id]
                logger.info(f"Controller ID-{c.id} \"{c.name}\" remapped.")
                logger.info(f"Mapping: {c.get_mapping()}")

            if event.type == pg.CONTROLLERAXISMOTION:
                c = controllers[event.instance_id]
                logger.debug(f"Controller ID-{c.id} \"{c.name}\" Axis {AXIS_NAMES[event.axis]}: {event.value}")
            if event.type == pg.CONTROLLERBUTTONDOWN:
                c = controllers[event.instance_id]
                logger.debug(f"Controller ID-{c.id} \"{c.name}\" Button {BUTTON_NAMES[event.button]} down")
            if event.type == pg.CONTROLLERBUTTONUP:
                c = controllers[event.instance_id]
                logger.debug(f"Controller ID-{c.id} \"{c.name}\" Button {BUTTON_NAMES[event.button]} up")

        screen.fill((0, 0, 0))

        lines: list[str] = [f"{pgc.get_count()} controller(s) detected. (ESC to quit program.)"]

        for i, c in enumerate(controllers.values()):
            if display_index != i:
                continue

            lines.append(f"Controller {display_index + 1}/{pgc.get_count()} (Use arrow keys to cycle controllers.)")
            lines.append(f"Controller ID-{c.id} \"{c.name}\"")
            lines.append(f"Rumble supported: {rumbles[c.id]}")
            lines.append(f"Attached: {bool(c.attached())}")

            for axis, name in AXIS_NAMES.items():
                lines.append(f"Axis {name}: {c.get_axis(axis)}")

            for button, name in BUTTON_NAMES.items():
                lines.append(f"Button {name}: {c.get_button(button)}")

        screen.blit(
            font.render("\n".join(lines), True, "white", "black", 500 - 20), (10, 5)
        )

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
