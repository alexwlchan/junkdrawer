set -x DIR (dirname (status -f))
set -x ROOT (dirname $DIR)


# Add a directory to the path, if it exists
function append_dir_to_path
    set dir $argv[1]
    if [ -d "$dir" ]
        set -g -x PATH $PATH $dir
    end
end


###############################################################################
# Entry point for fish shell config
###############################################################################

# Add Cargo install path
append_dir_to_path ~/.cargo/bin

append_dir_to_path "$DIR/pathscripts"

# A useful alias for quickly tallying a set of data
alias tally "sort | uniq -c | sort"

# Quickly create and cd to a temporary directory
function tmpdir
    cd (mktemp -d)
end

# Alias for finding out which subdirectories of the current dir contain
# the most files.  Useful when trying to find wasted disk space.
alias cdir 'for l in (ls); if [ -d $l ]; echo (find $l | wc -l)"  $l"; end; end | sort'

function reload_fish_config
  . ~/.config/fish/config.fish
end

function get_travis_logs
    ~/.virtualenvs/platform/bin/python $ROOT/servcies/travis/get_travis_logs.py (furl) --token=(cat $ROOT/travis_token.txt)
end

function tfdiff
    python3 $ROOT/tfdiff.py (pbpaste)
end

# Get the last screenshot I took.
#
# Note that Mojave changed the format of the filenames: previously they
# were "Screen Shot <date>", now they're "Screenshot <date>".
#
function last_screenshot
  find ~/Desktop -name 'Screen Shot*' -print0 -o -name 'Screenshot*' -print0 | grep -v 'reborder.png' xargs -0 stat -f '%m %N' | sort -rn | head -1 | cut -f2- -d" "
end

# Adjust the border on the last screenshot I took
function reborder_last_screenshot
  pushd ~/Desktop
    python3 $ROOT/reborder.py (basename (last_screenshot)) $argv[1]
    find ~/Desktop -name 'Screen Shot*reborder.png' -print0 -o -name 'Screenshot*reborder.png' -print0 | xargs -0 stat -f '%m %N' | sort -rn | head -1 | cut -f2- -d" "
  popd
end


###############################################################################
# virtualfish -- a fish wrapper for virtualenv
# https://github.com/adambrenecki/virtualfish
###############################################################################
eval (python3 -m virtualfish auto_activation) >> /dev/null 2>&1 &


###############################################################################
# Other fish config files
###############################################################################

. $DIR/_prompt.fish
. $DIR/git.fish
. $DIR/_docker.fish
. $DIR/_dockerfiles.fish
. $DIR/_imdown.fish
. $DIR/_twitter.fish
. $DIR/_wellcome.fish

. $DIR/_aws.fish

# Load macOS-specific utilities
if [ (uname -s) = "Darwin" ]
    . $DIR/_macos.fish
end

if [ (hostname) = "Alexs-MacBook-2" -o (hostname) = "Alexs-MacBook-2.local" ]
  . $DIR/_macbook.fish
end
