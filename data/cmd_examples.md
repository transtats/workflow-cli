## Commands

### Push

```
./transtats push
    --package-name anaconda
    --project-uid rFOGucI6IwH4fZPijXXXXX
    --target-langs ja,zh_CN
    --repo-type weblate
    --repo-branch rhel-9
    --update false
    --prepend-branch false
```

```
./transtats push
    --package-name foreman-2
    --project-uid GVajCPA7jOE9cloLuXXXXX
    --target-langs ja,zh_CN
    --repo-type transifex
    --repo-branch foreman_discoverypot
    --update false
    --prepend-branch true
```

### Pull

```
./transtats pull
    --package-name anaconda
    --project-uid rFOGucI6IwH4fZPijXXXXX
    --target-langs ja,zh_CN
    --repo-type weblate
    --repo-branch main
    --workflow-step translations
```

```
./transtats pull
    --package-name foreman-2
    --project-uid GVajCPA7jOE9cloLuXXXXX
    --target-langs ja,zh_CN
    --repo-type foreman_discoverypot
    --repo-branch main
    --workflow-step translations
```
