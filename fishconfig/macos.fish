###############################################################################
# macOS-specific shell config
###############################################################################

# Provide a convenient alias for the front URL
alias furl="~/.cargo/bin/safari url"


# Dump the complete list of Safari URLs
function safari-dump
  set ds (date +'%Y-%m-%d_%H-%M')
  ~/.cargo/bin/safari urls-all > ~/Desktop/safari_$ds.txt
  echo ~/Desktop/safari_$ds.txt
end


# Open the current working directory as a Git repository in GitUp
function gup
    set top_level (git rev-parse --show-toplevel)
    if [ "$status" -eq "0" ]
        set curdir (pwd)
        cd $top_level
        open -a GitUp.app .
        cd $curdir
        return 0
    else
        return 1
    end
end


# Get the URL of the frontmost GitHub page and clone it
function gh-clone
    github-clone (furl)
end
