#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import yaml
from infrasim.model import CSocat
from . import run_command, logger, CommandNotFound, CommandRunFailed, VM_DEFAULT_CONFIG


def get_socat():
    try:
        code, socat_cmd = run_command("which socat")
        return socat_cmd.strip(os.linesep)
    except CommandRunFailed as e:
        raise CommandNotFound("/usr/bin/socat")


def status_socat():
    try:
        run_command("pidof socat")
        print "Infrasim Socat service is running"
    except CommandRunFailed as e:
        print "Inrasim Socat service is stopped"


def start_socat(conf_file=VM_DEFAULT_CONFIG):
    try:
        with open(conf_file, 'r') as f_yml:
            conf = yaml.load(f_yml)

        socat = CSocat()
        # Read SOL device, serial port from conf
        # and set to socat
        if "sol_device" in conf:
            socat.set_sol_device(conf["sol_device"])
        if "serial_port" in conf:
            socat.set_port_serial(conf["serial_port"])

        socat.init()
        socat.precheck()
        cmd = socat.get_commandline()

        run_command(cmd+" &", True, None, None)
        time.sleep(3)
        logger.info("socat start")
    except CommandRunFailed as e:
        raise e


def stop_socat():
    socat_stop_cmd = "pkill socat"
    try:
        run_command(socat_stop_cmd, True, None, None)
        logger.info("socat stop")
    except CommandRunFailed as e:
        logger.error("socat stop failed")
