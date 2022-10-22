#! /usr/bin/env python
# encoding: utf-8

from asyncio import subprocess
import os

APPNAME = "quiche"
VERSION = "1.0.0"


def configure(conf):

    conf.find_program("cargo")
    conf.find_program("rustc")

    conf.find_program("cmake")


def build(bld):

    quiche_dir = bld.dependency_node("quiche-source")

    bld.exec_command(
        f"cargo build --release --target-dir {bld.out_dir}",
        cwd=quiche_dir.abspath(),
        env=bld.env.env,
        stdout=subprocess.PIPE,
    )
