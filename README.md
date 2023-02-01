ReChecked Agent plugins are stored in here.

The main plugin is check_rcagent.py, which allows active checks to be performed against the rcagent.

#### Installation

To install the plugin on your Nagios systems:

- **Nagios XI** - Download and install the latest [ReChecked Nagios XI Config Wizard](https://rechecked.io/download) in the XI GUI.
- **Nagios Core** - Download the [check_rcagent.py](https://rechecked.io/download) file, place it in `/usr/local/nagios/libexec`.


#### Example

Running a check for memory usage:

```
./check_rcagent.py -H <host> -M memory/virtual -t <token>
```

Outputs:
```
OK: Using 36.71% (23.38/63.68GiB Total)
```

For full details about using the plugin, view the documentation at: https://rechecked.io/documentation