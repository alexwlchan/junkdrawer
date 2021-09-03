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
