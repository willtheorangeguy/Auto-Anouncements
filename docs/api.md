# API

Start with `send.main(argv)` for the command-line workflow. It returns an exit
status. File and SMTP failures return 1; invalid arguments raise `SystemExit(2)`.
The lower-level helpers raise their errors to the caller.

```python
from send import main

status = main(["--config", "config.example.json", "--dry-run"])
print(status)
```

The command prints a message summary and next scheduled time, followed by:

```text
0
```

## Reference

::: send.send
    options:
      members:
        - main
        - load_config
        - build_message
        - send_announcement
        - next_run
        - run_schedule
