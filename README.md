# workflow-cli
CLI for translation workflows

```shell
Usage: transtats [OPTIONS] COMMAND [ARGS]...

  Transtats Localization Workflow CLI

Options:
  --help  Show this message and exit.

Commands:
  pull       Download translations from Phrase (Memsource) and submit...
  push       Download translations from a Platform (Weblate, Transifex)...
  templates  List available job templates.
  version    Display the current version.
```

Place [transtats.conf](https://github.com/transtats/workflow-cli/tree/devel/data/config-example) at `~/.config/` directory before running push/pull.
<br>For custom path set `TRANSTATS_CONFIG_PATH` environment variable. 

See `push` and `pull` command examples [here](https://github.com/transtats/workflow-cli/blob/devel/data/cmd_examples.md).

Developer notes are [here](https://github.com/transtats/workflow-cli/blob/devel/DEVELOP.md).

#### Contribution

* Fork [workflow-cli repo](https://github.com/transtats/workflow-cli) to your username and clone repository locally.
* Setup development environment `pip install -r requirements.txt`
* The *devel* branch is the release actively under development.
* The *main* branch corresponds to the latest stable release.
* If you find any bug/issue or got an idea, open a [github issue](https://github.com/transtats/transtats-cli/issues/new).

### License

[Apache License](http://www.apache.org/licenses/LICENSE-2.0), Version 2.0
