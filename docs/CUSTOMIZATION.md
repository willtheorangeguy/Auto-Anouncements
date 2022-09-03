# Auto Announcements Customization

Auto Announcements is designed to be highly customizable. The send and receive addresses can be changed, as well as the message body.

All of these instructions require [a text editor](https://code.visualstudio.com/) to be installed.

## Force the Same Sender

The bot can be configured to always use the same send email address every time it is run, rather than manually asking. To enable this, follow these steps:

1. _Line 8_: Replace the `input('YOUR email address:')` with the email address that the bot should always send from.
2. _Line 9_: Remove the `# replace above with your email address for direct delivery` comment.

## Force the Same Recipient

The bot can also be configured to always use the same recipient address every time it is run, rather than manually asking. To enable this, follow these steps:

1. _Line 10_: Replace the `input('RECIPIENT\'s email address:')` with the email address that the bot should always send to.
2. _Line 11_: Remove the `# replace above with the recipients email address for direct delivery` comment.

## Change the Message Body

This bot supports sending an `HTML` formatted email message. To change the email message that is sent each time it is run, follow these steps:

1. _Line 18_: Remove the `<h1>A Heading</h1><p>Hello There!</p>` text between the two apostrophes (`'...'`).
2. Replace this text with a single line of `HTML` code for your email message. If the email message is longer than a single line, just ensure the code is [minified](https://codebeautify.org/minify-html) to fit on one line.
