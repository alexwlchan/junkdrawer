tell application "Preview" to open "{jp2_path}"

tell application "System Events"
    tell process "Preview"
        set frontmost to true
        click menu item "Export…" of menu "File" of menu bar 1
        repeat until sheet 1 of window 1 exists
            delay 0.1
        end repeat

        tell window 1
            tell sheet 1
                tell pop up button 1 of group 1
                    click
                    delay 0.1
                    click menu item "JPEG" of menu 1
                end tell

                set value of slider 1 of group 1 to 1

                tell button 1 to click
            end tell
        end tell
    end tell
end tell

tell application "Preview" to close window 1
