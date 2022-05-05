# SA-base64

Version 3.0.0

_Base64 Add-On for Splunk_ provides a custom command for base64 encoding and decoding

## Example usage

Base64 Add-On for Splunk implements a streaming custom SPL search command called `base64`.

```
| makeresults
| eval encodedField="ZnJlZA==", otherEncodedField="YmFycnkK"
| base64 action=decode field=encodedField mode=append
| base64 action=decode field=otherEncodedField mode=append
| eval toEncode = "this is to be encoded"
| base64 action=encode field=toEncode mode=append
| table _time encodedField* otherEncodedField* *
```

### Search internal logs

Search for messages from the Base64 SPL search command:

```
index=_internal sourcetype=splunkd b64.py
```

## License

## Development

If you would like to develop or build this TA from source, see the [development](./DEVELOPMENT.md) documentation.

## Authors

 * Author: Robin Wu ([1.0](https://splunkbase.splunk.com/app/1922))
 * Author: Cedric Le Roux ([1.1](https://splunkbase.splunk.com/app/5143/))
 * Author: Cameron Just ([2.0.x](https://github.com/cameronjust/TA-base64))
 * Author: Lowell Alleman ([3.0](https://github.com/Kintyre/SA-base64))


## Changelog
- 1.0   - First Splunkbase app release by Robin Wu
- 1.1   - Initial Splunk 6.3 version from Splunkbase by Cedric Le Roux
- 2.0.0 - Upgraded splunklib and b64.py to be Splunk 8.x compatible (by Cameron Just)
- 2.0.1 - Added in the ability for carriage return and line feed passthrough + Added fixing up of incorrect padding
- 2.0.2 - Updated Splunklib and fixed up encode commands
- 3.0.0 - Added packaging.  Rename to SA-base64 (search addon) to avoid any conflicts with existing release



---

This addon was built from the [Kintyre Splunk App builder](https://github.com/Kintyre/cypress-cookiecutter) (version 1.9.0) [cookiecutter](https://github.com/audreyr/cookiecutter) project.
