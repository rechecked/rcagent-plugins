ReChecked Agent related plugins.

The main plugin is check_rcagent.py, which allows active checks to be performed against the rcagent.

### Installation

To install the plugin on your Nagios systems:

- **Nagios XI** - Download and install the latest [ReChecked Nagios XI Config Wizard](https://rechecked.io/download) in the XI GUI.
- **Nagios Core** - Download the [check_rcagent.py](https://rechecked.io/download) file, place it in `/usr/local/nagios/libexec`.


### How To Use

Use the `--help` option to see all other options. For full details about using the plugin, [view the documentation](https://rechecked.io/documentation).

Endpoints are reached using `-e <endpoint>` while plugins are ran using `-p <plugin>`.

#### Endpoint Examples

Running a check for memory usage:

```
./check_rcagent.py -H <host> -t <token> -e memory/virtual -w 20 -c 60
```

Output:
```
CRITICAL: Memory usage is 68.28% (2.47/3.62 GiB Total) | 'percent'=68.28%;20;60 'available'=0.68GiB;20;60 'used'=2.47GiB;20;60 'free'=0.25GiB;20;60 'total'=3.62GiB;20;60
```

For pasing query arguments, such as `path=/` for the disk check use:

```
./check_rcagent.py -H <host> -t <token> -e disk -q path=/
```

Output:
```
OK: Disk usage of / is 34.91% (12.23/35.04 GiB Total) | 'percent'=34.91% 'used'=12.23GiB 'free'=22.81GiB 'total'=35.04GiB
```

#### Plugin Example

For running a plugin use `--arg=""` for proper parsing rather than `-a` if you are using `-`/`--` in your arugment, like this:

```
./check_rcagent.py -H <host> -t <token> -p check_test.sh --arg="--warning 10" --arg="-c 20"
```

Output for a plugin that returns the output of the arguments above passed to it:
```
--warning 10 -c 20
```
