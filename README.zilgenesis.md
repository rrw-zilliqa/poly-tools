# ZIL SyncGenesisHeader fixup


You must specify the polynet wallet password in the config - the command-line option doesn't work.

Someone will want to extract the DS committee and a block number to sync to. You can do this with:

```
./tool get_zil_sync_data -conf config.conf
```

This simply queries the current block height and dumps out some keys which you will later put in your config file.

Run:

```
./tool sync_hard_genesis_header -conf syncconf.conf
```


