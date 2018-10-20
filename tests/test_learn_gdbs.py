#!/usr/local/bin/python

from nose import with_setup
from os import environ

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
pygdbsdir = os.path.join(parentdir, 'pygdbs')
sys.path.insert(0, pygdbsdir)

from ClientTcp import ClientTcp

class TestGdbServerProtocol:

    @classmethod
    def setup_class(self):
        self.in_docker = True if environ.get("IN_DOCKER") is not None else False
        self.hostname = "test-server" if self.in_docker else "127.0.0.1"
        self.port = 9999
        self.startup_message = b'$qSupported:multiprocess+;swbreak+;hwbreak+;qRelocInsn+;fork-events+;vfork-events+;exec-events+;vContSupported+;QThreadEvents+;no-resumed+;xmlRegisters=i386#6a'
        self.startup_server_response = b'$PacketSize=47ff;QPassSignals+;QProgramSignals+;QStartupWithShell+;QEnvironmentHexEncoded+;QEnvironmentReset+;QEnvironmentUnset+;QSetWorkingDir+;QCatchSyscalls+;qXfer:libraries-svr4:read+;augmented-libraries-svr4-read+;qXfer:auxv:read+;qXfer:spu:read+;qXfer:spu:write+;qXfer:siginfo:read+;qXfer:siginfo:write+;qXfer:features:read+;QStartNoAckMode+;qXfer:osdata:read+;multiprocess+;fork-events+;vfork-events+;exec-events+;QNonStop+;QDisableRandomization+;qXfer:threads:read+;ConditionalTracepoints+;TraceStateVariables+;TracepointSource+;DisconnectedTracing+;FastTracepoints+;StaticTracepoints+;InstallInTrace+;qXfer:statictrace:read+;qXfer:traceframe-info:read+;EnableDisableTracepoints+;QTBuffer:size+;tracenz+;ConditionalBreakpoints+;BreakpointCommands+;QAgent+;Qbtrace:bts+;Qbtrace-conf:bts:size+;Qbtrace:pt+;Qbtrace-conf:pt:size+;Qbtrace:off+;qXfer:btrace:read+;qXfer:btrace-conf:read+;swbreak+;hwbreak+;qXfer:exec-file:read+;vContSupported+;QThreadEvents+;no-resumed+#7f'

    def test_can_get_response(self):
        client = ClientTcp()
        client.open(self.hostname, self.port)
        client.write(self.startup_message)
        result = client.read()
        client.close()
        assert result == b'+'

    def test_can_get_second_response(self):
        client = ClientTcp()
        client.open(self.hostname, self.port)
        client.write(self.startup_message)
        result_1 = client.read()
        result_2 = client.read()
        client.close()
        assert result_2 == self.startup_server_response

    def test_can_get_third_none_response(self):
        client = ClientTcp()
        client.open(self.hostname, self.port)
        client.write(self.startup_message)
        result_1 = client.read()
        result_2 = client.read()
        result_3 = client.read()
        client.close()
        assert result_3 == None
