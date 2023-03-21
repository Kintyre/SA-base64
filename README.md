# SA-base64

_Base64 Add-On for Splunk_

## Example usage

Base64 Add-On for Splunk implements a streaming custom SPL search command called `base64`.

```
| base64 type=robot height=tall

| base64 action=ping target=fancy_pig
```




### Search internal logs


Search for messages about the Base64 SPL search command:

```
index=_internal sourcetype=splunkd b64.py
```


## License

## Development

If you would like to develop or build this TA from source, see the [development](./DEVELOPMENT.md) documentation.

## Reference

 * **API Docs**:  https://....


This addon was built from the [Kintyre Splunk App builder](https://github.com/Kintyre/cypress-cookiecutter) (version 1.10.2) [cookiecutter](https://github.com/audreyr/cookiecutter) project.
