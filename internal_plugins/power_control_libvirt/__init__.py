#
# Copyright(c) 2020 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from connection.ssh_executor import SshExecutor
from core.test_run import TestRun


class PowerControlPlugin:
    def __init__(self, params, config):
        print("Power Control LibVirt Plugin initialization")
        self.config = config

    def pre_setup(self):
        print("Power Control LibVirt Plugin pre setup")
        if self.config['connection_type'] == 'ssh':
            self.executor = SshExecutor(
                self.config['ip'],
                self.config['user'],
                self.config['password'],
                self.config.get('port', 22)
            )
        else:
            cls.executor = LocalExecutor()

    def post_setup(self):
        pass

    def teardown(self):
        pass

    def power_cycle(self):
        self.executor.run(f"virsh reset {self.config['domain']}")
        TestRun.executor.wait_for_connection_loss()
        TestRun.executor.wait_for_connection()


plugin_class = PowerControlPlugin