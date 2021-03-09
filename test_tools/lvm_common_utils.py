#
# Copyright(c) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#


import datetime

from api.cas import casadm
from api.cas.cache_config import CacheMode
from api.cas.init_config import InitConfig
from storage_devices.lvm import get_block_devices_list
from test_tools import fs_utils
from test_tools.fio.fio import Fio
from test_tools.fio.fio_param import IoEngine, ReadWrite, VerifyMethod
from test_utils.size import Size, Unit

opencas_conf_path = "/etc/opencas/opencas.conf"


def prepare_devices(cache_dev, core_dev, partitions_size: Size, cache_mode: CacheMode = None):
    cache_dev.create_partitions([partitions_size])
    core_dev.create_partitions([partitions_size])

    cache = casadm.start_cache(cache_dev.partitions[0], cache_mode=cache_mode, force=True)
    core = cache.add_core(core_dev.partitions[0])

    return cache, core


def run_fio_on_lvm(volumes: []):
    fio_run = (Fio().create_command()
               .read_write(ReadWrite.randrw)
               .io_engine(IoEngine.sync)
               .io_depth(1)
               .time_based()
               .run_time(datetime.timedelta(seconds=180))
               .do_verify()
               .verify(VerifyMethod.md5)
               .block_size(Size(1, Unit.Blocks4096)))
    for lvm in volumes:
        fio_run.add_job().target(lvm).size(lvm.size)
    fio_run.run()


def run_fio(file_size: Size, io_target):
    (Fio().create_command()
        .target(io_target)
        .read_write(ReadWrite.randwrite)
        .io_engine(IoEngine.libaio)
        .io_depth(16)
        .file_size(file_size)
        .verification_with_pattern()
        .write_percentage(100)
        .block_size(Size(1, Unit.Blocks512))
        .run())


def get_test_configuration():
    InitConfig.create_init_config_from_running_configuration()
    config = fs_utils.read_file(opencas_conf_path)
    devices = get_block_devices_list()

    return config, devices
