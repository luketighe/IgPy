# IgPy
IG Labs REST &amp; Streaming API (in development).
This library is still in development therefore this ins't ready for production systems.

### Install
To install directly from github, run the following pip command:

```shell
pip install git+git://github.com/luketighe/IgPy.git
```

### Upgrade
To upgrade directly from github, run the following pip command:

```shell
pip install git+git://github.com/luketighe/IgPy.git --upgrade
```

### Uninstall
To uninstall, run the following pip command:
```shell
pip uninstall IgPy
```

## Example

How to log into IG using the REST API and invoke the Streaming API for USDJPY
```python
# import IGRestAPI and IGStreamingAPI
from igpy.rest_api import IGRestApi
from igpy.streaming_api import IGStreamingApi

# REST API authentication
ig_rest = IGRestApi('username', 'password', 'api_key', 'ig_url')
ig_rest.login() # will resolve authentication token and use for subsequent REST/Streaming requests

# inject the REST API into the Streaming API
ig_streaming = IGStreamingApi(ig_rest)

# create a custom handler to receiver the bars
def bar_handler(bar):
    ...
    # your python code to handle the bar
    ...

# subscribe to USDJPY that will invoke our custom handler
ig_streaming.subscribe('MERGE', ['CHART:CS.D.USDJPY.TODAY.IP:5MINUTE'], ['UTM', 'BID_OPEN', 'BID_HIGH', 'BID_LOW', 'BID_CLOSE', 'CONS_END'], bar_handler)

```

