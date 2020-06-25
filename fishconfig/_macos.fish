###############################################################################
# macOS-specific shell config
###############################################################################

# Provide a convenient alias for the front URL in both browsers
alias furl="~/.cargo/bin/safari url"
alias gurl="osascript -e 'tell application \"Google Chrome\" to tell front window to get URL of tab (active tab index)'"


# Open the current working directory as a Git repository in GitUp
function gup
    set top_level (git rev-parse --show-toplevel)
    if [ "$status" -eq "0" ]
        open -a GitUp.app $top_level
        return 0
    else
        return 1
    end
end


# Get the URL of the frontmost GitHub page and clone it
function gh-clone
    github-clone (furl)
end


# Scramble the current MAC address (for... reasons)
# https://apple.stackexchange.com/a/183370/14295
function scramble_mac_address
    sudo /System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport --disassociate
    sudo ifconfig en0 ether (openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/./0/2; s/.$//')
    networksetup -detectnewhardware
end


function backup_overcast
    set overcast_dir ~/Documents/backups/overcast
    set opml_path "$overcast_dir"/overcast.(date +"%Y-%m-%d").opml.xml
    mv ~/Desktop/overcast.opml.xml $opml_path
    python3 ~/repos/overcast-downloader/download_overcast_podcasts.py --download_dir $overcast_dir/audiofiles $opml_path

    osascript -e '
      tell application "Things3"
        repeat with todayToDo in to dos of list "Today"
          if ((name of todayToDo) = "Download podcast episodes from Overcast") then
            set status of todayToDo to completed
          end if
        end repeat
      end tell
    '
end


function nvalt_tags
  grep --no-filename '^tags: ' *.md \
    | cut -c 7- \
    | tr ' ' '\n' \
    | tr '@' ' ' \
    | sort \
    | uniq -c
end


function nvalt_lists
  grep --no-filename '^list: ' *.md | \
    cut -c 7- | \
    sort | \
    uniq -c
end
