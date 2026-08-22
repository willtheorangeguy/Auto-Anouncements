# API

Auto Announcements exposes one public Python function, `send.main()`. The console scripts and
module entry points call the same function. It prompts for two addresses, creates the fixed HTML
message, and sends it through an SMTP relay on `localhost`.

## Calling `main`

Call `main()` only when a local SMTP relay is available. The function takes no arguments and
returns `None` after the SMTP call succeeds.

```python
from send import main

main()
```

```text
YOUR email address:sender@example.com
RECIPIENT's email address:recipient@example.com
2026-08-22 12:00:00
Message sent successfully on 2026-08-22 12:00:00 !
```

The timestamps reflect the time of the run. If no relay accepts the connection on
`localhost:25`, the SMTP exception propagates to the caller.

## Reference

::: send.send
    options:
      members:
        - main
