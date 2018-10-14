tell application "iTerm"
	tell (create window with default profile) to tell current tab to tell the current session to write text "ssh -t alexwlchan@helene.linode 'cd ~/repos/alexwlchan.net; fish'"

	tell (create window with default profile) to tell current tab to tell the current session to write text "ssh -t alexwlchan@helene.linode 'cd ~/repos/alexwlchan.net; make analytics-report; fish'"
end tell
