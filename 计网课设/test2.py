        TCPtext = ("Ether Ⅱ, Src: " + choosedPacket['Ethernet'].src + ", Dst: " + choosedPacket['Ethernet'].dst + "\n")
        TCPtext += ("     Destination: " + choosedPacket['Ethernet'].dst + "\n")
        TCPtext += ("     Source: " + choosedPacket['Ethernet'].src + "\n")
        TCPtext += ("     Type: " + str(choosedPacket['Ethernet'].type) + "\n")
        
        ------------------------------

        TCPtext += ("Internet Protocol Version 4, Src: " + choosedPacket['IP'].src + ", Dst: " + choosedPacket[
                'IP'].dst + "\n")
        TCPtext += ("     " + decimal_to_four_bit_binary(choosedPacket['IP'].version) + " .... = Version: " + str(
                choosedPacket['IP'].version) + "\n")
        TCPtext += ("     .... " + decimal_to_four_bit_binary(choosedPacket['IP'].ihl) + " = Header Length: " + str(
                choosedPacket['IP'].ihl) + "\n")
        TCPtext += ("     Differentiated Services Field: 0x" + decimal_to_four_bit_binary(
                choosedPacket['IP'].tos) + "\n")
        TCPtext += ("     Total Length: " + str(choosedPacket['IP'].len) + "\n")
        TCPtext += ("     Identification: 0x" + decimal_to_four_bit_binary(choosedPacket['IP'].id) + "(" + str(
                choosedPacket['IP'].id) + ")" + "\n")
        TCPtext += ("     Flags: 0x%03x " % int(choosedPacket['TCP'].flags) + "(" + flagTrans + ")" + "\n")

        TCPtext += ("            0... .... .... = Reserved: Not set" + "\n")
        if choosedPacket['IP'].flags.DF == 0:
                TCPtext += ("            .0.. .... .... = Don't fragment: Not set" + "\n")
        else:
                TCPtext += ("            .1.. .... .... = Don't fragment: Set" + "\n")
        if choosedPacket['IP'].flags.MF == 0:
                TCPtext += ("            ..0. .... .... = More fragments: Not set" + "\n")
        else:
                TCPtext += ("            ..1. .... .... = More fragments: Set" + "\n")

        TCPtext += ("     Fragment offset: " + str(choosedPacket['IP'].frag) + "\n")
        TCPtext += ("     Time to live: " + str(choosedPacket['IP'].ttl) + "\n")
        TCPtext += ("     Protocol: " + str(choosedPacket['IP'].proto) + "\n")

        # 计算校验和
        chksum = choosedPacket['IP'].chksum
        TCPtext += ("     Header checksum: " + hex(chksum) + " [correct]\n")

        ip_c = choosedPacket['IP'].copy()
        ip_c = ip_c.__class__(bytes(ip_c))
        checksum_self = ip_c.chksum

        if chksum == checksum_self:
                TCPtext += ("""     [Header checksum status: Good]-++++++++""" + "\n")
        else:
                TCPtext += ("""     [Header checksum status: Bad]""" + "\n")
        TCPtext += ("     [Calculated checksum: " + hex(checksum_self) + "]\n")

        TCPtext += ("     Source: " + str(choosedPacket['IP'].src) + "\n")
        TCPtext += ("     Destination: " + str(choosedPacket['IP'].dst) + "\n")