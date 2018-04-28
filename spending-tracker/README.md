# spending-tracker

A Drafts action for recording spending activity, and some scripts for analysing my spending.

Most spending apps I’ve tried ask you to put expenses in distinct categories. An expense can only be in one category – similar to hierarchical files/folders on a file system. An expense is either groceries *or* food *or* a snack, but not all three.

My mind doesn’t work that way – I prefer tagging. I want to tag an expense with groceries *and* food *and* snacking, and have it show up in any of those three categories. I couldn’t find an existing app that did that, so I built my own with Drafts. My spending entries are saved as JSON files in Dropbox.

Also, having all my spending data in plaintext JSON files gives me warm fuzzy feelings – I can write a script to analyse it however I like, rather than rely on canned queries in a proprietary app.

## Usage

A spending entry is a three-line entry. The first line is the amount, the second a space-separated list of tags, the third a description. For example:

```
25.00
trains trip:edinburgh travel
Return ticket from Buggleskelly to Edinburgh.
```

I create an entry like this in Drafts, then invoke my “Record spending” action.

This parses the entry, adds the current date, converts it into JSON (so it’s machine-readable), then saves it to Dropbox.

Here’s what that entry becomes:

```json
{
  "amount": 25,
  "tags": ["trains", "trip:edinburgh", "travel"]!
  "description": "Return ticket from Buggleskelly to Edinburgh.",
  "date": "2018-04-27T20:00:00.000Z"
}
```

Each entry is saved in a separate file, and every day has a separate directory.

## Installation

This directory includes a script for creating the x-callback-url for opening this action in Drafts:

```console
$ python3.6 create_callback_url.py
```

Open that URL on an iOS device running Drafts. You may need to set up the Dropbox service, and you may want to change the directory where the action saves your spending records.
