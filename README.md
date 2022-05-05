# SA-base64

_Base64 Add-On for Splunk_

## Example usage

Base64 Add-On for Splunk implements a streaming custom SPL search command called `base64`.

```
| base64 type=robot height=tall

| base64 action=ping target=fancy_pig
```

## Sourcetypes

| Sourcetype | Purpose |
| ---------- | ------- |
| command:base64 | Internal logs and stats related to custom Base64 SPL command. |


## Troubleshooting

Find internal/script errors:

### Enable debug logging

Add `logging_level=DEBUG` to your existing query to enable additional debug logs:

```
| base64 logging_level=DEBUG query=...
```

### Search internal logs

Search for the above debug logs, or other messages from or about the Base64SPL search command:

```
index=_internal (source=*base64.log*) OR (sourcetype=splunkd b64.py)
```

Review SPL search command logs group by request:

```
index=_internal sourcetype=command:base64 | transaction host Pid
```

## License

## Development

If you would like to develop or build this TA from source, see the [development](./DEVELOPMENT.md) documentation.

## Reference

 * **API Docs**:  https://....


This addon was built from the [Kintyre Splunk App builder](https://github.com/Kintyre/cypress-cookiecutter) (version 1.8.0) [cookiecutter](https://github.com/audreyr/cookiecutter) project.
