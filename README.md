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

Place [transtats.config](https://github.com/transtats/workflow-cli/tree/devel/data/config-example) at `~/.config/` directory before running push/pull.

See `push` and `pull` command examples [here](https://github.com/transtats/workflow-cli/blob/devel/data/cmd_examples.md).

Developer notes are [here](https://github.com/transtats/workflow-cli/blob/devel/DEVELOP.md).
