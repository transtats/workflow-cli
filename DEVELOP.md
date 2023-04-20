## Developer Notes

### Service Layer

Service layer handles all REST API communications. `restclient.py` binds configuration with their HTTP Request requirements (headers, auth, etc.) and makes the call.
`Config` directory has API endpoint definitions. Create a new config to extend support, for example, [Crowdin](https://crowdin.com/).

`api_resources.py` is the factory where API requests are grouped by operations. (fetch_project_details, fetch_translation_stats, etc.)
This acts as an API for service layer consumers.

### Jobs Framework

Jobs are YML based. Tasks in YML are mapped to their respective (cmd) definitions in `action_mapper.py`.
System creates a linked list where each task represents a node. To extend, create new files in `cmds` directory and make an entry in action mapper.
Jobs runner acts as an interface between Jobs framework and CLI commands. It transforms command to their job execution state with required parameters.
Ideally `JobRunner` interface should be implemented for each CLI command.

### CLI Commands

CLI commands are based on [CLICK](https://click.palletsprojects.com/en/8.1.x/) framework. And they are all tied up with app_context in `twcli/__init__.py`.
See `config.py` to understand loading of user config.

_Happy Hacking_
