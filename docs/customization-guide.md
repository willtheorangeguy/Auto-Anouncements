# Customization

Edit your JSON configuration and announcement files to customize delivery.
Source changes are not required.

## Body and files

Edit `message.html` to change the HTML body. Set `message_file` to a UTF-8 text
file such as `message.txt` for a plain-text body. Configure attachments separately,
for example `"attachments": ["announcements.pdf", "slides.pptx"]`.

Body and attachment paths are relative to the configuration file. The scheduler
rereads their contents on every run. It does not substitute variables inside files.

## Subject and recipients

Set `subject` to `Community announcements for {date}` to include the local send
date. Set `sender` and `recipients` in JSON to avoid interactive prompts.

After editing, validate your configuration:

```bash
python -m send --config config.json --dry-run
```

Restart a running scheduler after changing its configuration. See
[Configuration](configuration.md) for all options.
