#! /usr/bin/env python3

"""
Given a leveldb file, this script will grab the DsCommittee from it and output a json file that can be read by
zil_reconstruct_genesis_header.

"""

import plyvel
import click
import typing
import json
import os

class DSCMember:
    def __init__(self,data: str):
        # The data here is comes from a DequeueOfNode, which is a std::deque<PairOfNode>
        # PairOfNode = std::pair<PubKey, Peer>
        # And we store it by serializing the PubKey, then the Peer
        # A serialized PubKey is just 33 bytes of key.
        self.PubKey = data[:33]
        self.IpAddress = None
        self.ListenPortHost = 0
        self.HostName = ""

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DSCMember):
            fmtkey = f"0x{obj.PubKey.hex()}"
            return { "PubKey" : fmtkey,
                     "IpAddress": obj.IpAddress,
                     "ListenPortHost" : obj.ListenPortHost,
                     "HostName": obj.HostName }
        return json.JSONEncoder.default(self, obj)

@click.command()
@click.argument('persistence')
@click.argument('outfile')
@click.option('--blocks/--no-blocks', default = True)
def extract(persistence,outfile, blocks):
    """ Reconstruct a genesis header tracker input file
    Usage:
      extract [persistence] [outfile]

    [persistence] is the location of persistence.
    Leaves the genesis start file in [outfile] and prints the tx block number to which it applies.
    Uses TxBlocks (for the tx block number) and DSCommittee (for the DSC)
    """
    print(f"Reconstructing genesis header starting point from {persistence}")
    dsCommittee = []
    dsMap = [ ]
    if blocks:
        print("Finding the latest txblock .. ")
        tx = plyvel.DB(os.path.join(persistence, "txBlocks"))
        blks = [ ]
        # once again, sorted by string order ..
        print("Reading blocks .. ")
        for key, value in tx:
            blks.append(int(key))
        all_blks = sorted(blks)
        print(f"There are {len(all_blks)} blocks, from {all_blks[0]} to {all_blks[-1]}")
        tx.close()
    print("Now extracting the ds committe .. ")
    db = plyvel.DB(os.path.join(persistence, "dsCommittee"))
    # Amusingly, though these are sorted, they are sorted in string order, not in numerical order, and we therefore
    # have to sort them again!
    # index 0 stores the index number of the leader; the rest are just the dscommittee members in order.
    for key, value in db:
        dsMap.append((int(key), DSCMember(value)))
        print(value)
        print(len(value))
    # Sort the tuples
    dsMapSorted = sorted(dsMap, key = lambda x: x[0])
    # Remove 0 - it's the identity of the leader.
    dsMapFiltered = list(map(lambda x: x[1], filter(lambda x : x[0] != 0, dsMapSorted)))
    print(f"Writing {len(dsMapFiltered)} DSC members to {outfile}")
    with open(outfile, 'w') as f:
        f.write(json.dumps({ "DsComm" : dsMapFiltered }, cls = MyEncoder))
    db.close()


if __name__ == '__main__':
    extract()
