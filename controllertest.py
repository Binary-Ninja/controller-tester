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


def main():
    logger.info("Program started.")
    pg.display.set_caption("Controller Testing")
    screen = pg.display.set_mode((500, 500))
    clock = pg.time.Clock()
    font = pg.Font(None, 25)
    lines: list[str] = []
    controllers: dict[int, pgc.Controller] = {}
    rumbles: dict[int, bool] = {}

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

            if event.type == pg.JOYDEVICEADDED:
                if pgc.is_controller(event.device_index):
                    logger.debug("Joy added (Controller).")
                else:
                    logger.debug("Joy added (Joystick).")
                    logger.info("Attempting to convert bad Joystick.")
                    try:
                        pgc.Controller.from_joystick(pg.Joystick(event.device_index))
                    except Exception as ex:
                        logger.info(f"Nope: {ex}")
            if event.type == pg.JOYDEVICEREMOVED:
                logger.debug("Joy removed.")

            if event.type == pg.CONTROLLERDEVICEADDED:
                c = pgc.Controller(event.device_index)
                controllers[c.id] = c
                if c.rumble(0, 0.7, 100):
                    rumbles[c.id] = True
                else:
                    rumbles[c.id] = False
                logger.info(f"Controller {c.id} {c.name} added. Rumble: {rumbles[c.id]}")
                logger.info(f"Mapping: {c.get_mapping()}")
            if event.type == pg.CONTROLLERDEVICEREMOVED:
                if event.instance_id in controllers:
                    c = controllers[event.instance_id]
                    logger.info(f"Controller {c.id} {c.name} removed.")
                    del controllers[c.id]
                    del rumbles[c.id]
                else:
                    logger.info("Controller ??? removed.")
            if event.type == pg.CONTROLLERDEVICEREMAPPED:
                c = controllers[event.instance_id]
                logger.info(f"Controller {c.id} {c.name} remapped.")

            if event.type in (pg.JOYBUTTONUP, pg.JOYBUTTONDOWN, pg.JOYHATMOTION, pg.JOYAXISMOTION):
                logger.debug(f"JOY {event.instance_id}: {event.__dict__.get("button", "")} "
                             f"{event.__dict__.get("axis", "")} {event.__dict__.get("hat", "")} "
                             f"{event.__dict__.get("value", "")}")

            if event.type == pg.CONTROLLERAXISMOTION:
                logger.info(f"Axis {event.axis}: {event.value}")
            if event.type == pg.CONTROLLERBUTTONDOWN:
                logger.info(f"Button {event.button} down")
            if event.type == pg.CONTROLLERBUTTONUP:
                logger.info(f"Button {event.button} up")

        screen.fill((0, 0, 0))

        lines = []
        for c in controllers.values():
            lines.append(f"Controller {c.id} {c.name}")
            lines.append(f"Rumble supported: {rumbles[c.id]}")
            lines.append(f"Attached: {bool(c.attached())}")

            for axis in (pg.CONTROLLER_AXIS_LEFTX, pg.CONTROLLER_AXIS_LEFTY, pg.CONTROLLER_AXIS_RIGHTX,
                         pg.CONTROLLER_AXIS_RIGHTY, pg.CONTROLLER_AXIS_TRIGGERLEFT, pg.CONTROLLER_AXIS_TRIGGERRIGHT):
                lines.append(f"Axis {axis}: {c.get_axis(axis)}")

            for button in (pg.CONTROLLER_BUTTON_A, pg.CONTROLLER_BUTTON_B, pg.CONTROLLER_BUTTON_X,
                           pg.CONTROLLER_BUTTON_Y, pg.CONTROLLER_BUTTON_DPAD_UP, pg.CONTROLLER_BUTTON_DPAD_DOWN,
                           pg.CONTROLLER_BUTTON_DPAD_LEFT, pg.CONTROLLER_BUTTON_DPAD_RIGHT,
                           pg.CONTROLLER_BUTTON_LEFTSHOULDER, pg.CONTROLLER_BUTTON_RIGHTSHOULDER,
                           pg.CONTROLLER_BUTTON_LEFTSTICK, pg.CONTROLLER_BUTTON_RIGHTSTICK, pg.CONTROLLER_BUTTON_BACK,
                           pg.CONTROLLER_BUTTON_START, pg.CONTROLLER_BUTTON_GUIDE):
                lines.append(f"Button {button}: {c.get_button(button)}")

        screen.blit(
            font.render("\n".join(lines), True, "white", "black", 500 - 20), (10, 10)
        )

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
