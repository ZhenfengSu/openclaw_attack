# Virtual Mail System

This directory is the default state root for the local virtual mail system when
you run:

```bash
python3 src/virtual_mail_system.py init --root virtual_mail
```

The simulator is file-based and intentionally simple, but it is much closer to a
real messaging system than a single pasted thread:

- per-mailbox folders
- inbox / drafts / sent separation
- thread tracking
- attachment copies
- local event log
- repeatable attack-scenario seeding

## Common flow

Initialize:

```bash
python3 src/virtual_mail_system.py init --root virtual_mail --reset
```

Seed one scenario:

```bash
python3 src/virtual_mail_system.py seed --root virtual_mail --scenario procurement_footer
```

List inbox:

```bash
python3 src/virtual_mail_system.py list --root virtual_mail --mailbox ops-assistant --folder inbox
```

Read one message:

```bash
python3 src/virtual_mail_system.py read --root virtual_mail --mailbox ops-assistant --message-id <message_id>
```

Create a reply draft:

```bash
python3 src/virtual_mail_system.py reply \
  --root virtual_mail \
  --mailbox ops-assistant \
  --message-id <message_id> \
  --body-file /tmp/reply.txt
```

Send the draft:

```bash
python3 src/virtual_mail_system.py send \
  --root virtual_mail \
  --mailbox ops-assistant \
  --message-id <draft_message_id>
```

## Built-in scenarios

- `procurement_footer`
- `travel_exfil`
- `forward_chain`
- `attachment_excerpt`
- `fake_system_notice`

These map to the workspace email attack cases in
`data/email_workspace_attack_cases.jsonl`.
