# ZIL SyncGenesisHeader fixup


You must specify the polynet wallet password in the config (limitation of poly-tools)

The process here is that we extract the DS Committee and block information from Zilliqa, just once:

```
./tools -tool get_zil_sync_data -conf config.json -pwallets ./poly.wallet  --output_file /my/state_file.json
```

We then distribute this to everyone who needs to resync the genesis header. And they then run:

```
./tools -tool sync_zil_genesis_header_from_file -conf config.json -pwallets ./poly.wallet  --input_file /my/state_file.json -ppwds <polypwd>
```

This:

 * Reads the JSON from state_file.json
 * Checks the network id (but doesn't validate it! Be careful that you only sync genesis headers from the network the state file was extracted from)
 * Submits the new genesis header to polynet (allegedly! I copied the code here so be careful .. )

Sadly, it only really works with a state file from the last block (there may be a way to get previous blocks' states, but I'm not sure - the code in Zilliqa 1 is complex)

