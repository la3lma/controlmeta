
import random

class SipService:

    sendMessageTemplate = ''.join([
        "MESSAGE sip:%s@%s SIP/2.0\n",
        "Via: SIP/2.0/UDP %s;branch=%x\n",
        "Max-Forwards: 2\n",
        "From: %s <sip:%s@%s:%d>;tag=%d\n",
        "To: sip:%s@%s\n",
        "Call-ID: %x@%s:%d\n",
        "CSeq: 1 MESSAGE\n",
        "Content-Type: text/plain\nContent-Length: %u\n",
        "\n%s\n"])

    _smqueueIP="123.456.789.123"
    _smqueuePort=4711
    _myIp="127.0.0.1"
    _myPort=6969
    _smscCode="978342"

    def newUnsignedRandom(self):
        return random.randint(0,0xffffffff)

    def newSipMessageString(
            self,
            smqueueIP,
            smqueuePort,
            myIP,
            myPort,
            smscCode,
            fromAddr,
            to,
            msg):
        randomBranch=self.newUnsignedRandom()
        randomTag=self.newUnsignedRandom()
        randomCallId=self.newUnsignedRandom()

        
        return self.sendMessageTemplate % (smscCode,
                                     smqueueIP,
                                     myIP,
                                     randomBranch,
                                     fromAddr,
                                     fromAddr,
                                     myIP,
                                     myPort,
                                     randomTag,
                                     to,
                                     smqueueIP,
                                     randomCallId,
                                     myIP,
                                     myPort,
                                     len(msg),
                                     msg)

    def sendMessage(self, fromAddr, to, msg):
        msgToSend = self.newSipMessageString(
            self._smqueueIP,
            self._smqueuePort,
            self._myIp,
            self._myPort,
            self._smscCode,
            fromAddr,
            to,
            msg)
        print "Simulating sending of '" + msgToSend + "'"

    
