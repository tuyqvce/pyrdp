from pyrdp.enum import PlayerMessageType
from pyrdp.layer import RDPFastPathDataLayerObserver, RDPDataLayerObserver
from pyrdp.pdu.rdp.data import RDPConfirmActivePDU, RDPInputPDU, RDPUpdatePDU
from pyrdp.recording.recorder import Recorder


class RecordingFastPathObserver(RDPFastPathDataLayerObserver):
    def __init__(self, recorder: Recorder, messageType: PlayerMessageType):
        self.recorder = recorder
        self.messageType = messageType
        RDPFastPathDataLayerObserver.__init__(self)

    def onPDUReceived(self, pdu):
        self.recorder.record(pdu, self.messageType)
        RDPFastPathDataLayerObserver.__init__(self)

class RecordingSlowPathObserver(RDPDataLayerObserver):
    def __init__(self, recorder: Recorder):
        RDPDataLayerObserver.__init__(self)
        self.recorder = recorder

    def onPDUReceived(self, pdu):
        if isinstance(pdu, (RDPConfirmActivePDU, RDPUpdatePDU, RDPInputPDU)):
            self.recorder.record(pdu, PlayerMessageType.SLOW_PATH_PDU)