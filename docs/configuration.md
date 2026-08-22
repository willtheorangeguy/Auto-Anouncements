# Auto Announcements — Configuration

There is no configuration file, no environment variable, and no command-line flag. Everything is
a literal in `send/send.py`.

Earlier documentation gave **line numbers** for these edits, and they no longer match the file.
This page names the symbols instead.

## The sender and recipient prompts

```python
sendaddress = input("YOUR email address:")
receiveaddress = input("RECIPIENT's email address:")
```

To stop it asking, replace either `input(...)` call with a literal:

```python
sendaddress = "announcements@example.org"
```

That is the whole of the "email addresses can be hard coded" feature — an edit you make, not
something the program supports.

## The message body

```python
msg = MIMEText("<h1>A Heading</h1><p>Hello There!</p>", "html")
```

A hardcoded string. To send real content, put your HTML there — or read a file:

```python
with open("message.html", encoding="utf-8") as f:
    msg = MIMEText(f.read(), "html")
```

**`message.html` already exists in the repository** — 57 lines of Word-generated HTML — and
nothing reads it. It appears to be the intended body from a previous design. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## The subject

```python
msg["Subject"] = "Church Announcements for " + date_today
```

The prefix is a literal, left over from the original use. Change it for anything else.

## The SMTP server

```python
s = smtplib.SMTP("localhost")
```

Hardcoded, with no port, no `starttls()`, and no `login()`. To use a real provider you would need
all three:

```python
s = smtplib.SMTP("smtp.example.org", 587)
s.starttls()
s.login(username, password)
```

Which also means finding somewhere to keep the password — there is no mechanism for that here.

## What is not configurable

Everything above requires editing the source. There is no argument parsing in this program at
all: `main()` takes no parameters, and the console script passes none.
