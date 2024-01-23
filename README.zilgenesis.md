# ZIL SyncGenesisHeader fixup


You must specify the polynet wallet password in the config (limitation of poly-tools)

The process here is that we extract the DS Committee and block information from Zilliqa, just once:

```sh
./tools -tool get_zil_sync_data -conf config.json -pwallets ./poly.wallet  --output_file /my/state_file.json
```

We then distribute this to everyone who needs to resync the genesis header. And they then run:

```sh
./tools -tool sync_zil_genesis_header_from_file -conf config.json -pwallets ./poly.wallet  --input_file /my/state_file.json -ppwds <polypwd>
```

This:

 * Reads the JSON from state_file.json
 * Checks the network id (but doesn't validate it! Be careful that you only sync genesis headers from the network the state file was extracted from)
 * Submits the new genesis header to polynet (allegedly! I copied the code here so be careful .. )

Sadly, it only really works with a state file from the last block (there may be a way to get previous blocks' states, but I'm not sure - the code in Zilliqa 1 is complex)


Other tools:

Retrieve the number of guard nodes.

```sh
./tools -tool get_zil_guards -conf config.json -pwallets ./poly.wallet
```

Reconstruct a genesis header. This:

 * Reads the DS Committee from `dsc.json` (an output of `scripts/state_from_leveldb.py` run on Zilliqa persistence.
 * Assumes this is the DSC at `blkIn`
 * Assumes there are `g` guard nodes (and always were! so beware of guard node reductions)
 * Queries the blockchain forwards from `blkIn` to `blkOut`, applying DSC changes
 * Outputs a gen header as of `blkOut` to `gen.json`

```sh
./tools -tool zil_reconstruct_genesis_header -conf config.json -input_file dsc.json -output_file gen.json -data_for_block blkIn -block_number blkOut -guard_nodes g
```

