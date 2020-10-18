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

append_dir_to_path ~/Library/Python/3.7/bin
append_dir_to_path ~/Library/Python/3.8/bin

append_dir_to_path ~/repos/ttml2srt

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
    ~/.virtualenvs/platform/bin/python $ROOT/services/travis/get_travis_logs.py (furl) --token=(cat $ROOT/travis_token.txt)
end

# Get the last screenshot I took.
#
# Note that Mojave changed the format of the filenames: previously they
# were "Screen Shot <date>", now they're "Screenshot <date>".
#
function last_screenshot
  find ~/Desktop -name 'Screenshot*' | tail -n 1
end

# Adjust the border on the last screenshot I took
function reborder_last_screenshot
  pushd ~/Desktop
    python3 $ROOT/reborder.py (basename (last_screenshot)) $argv[1]
    find ~/Desktop -name 'Screenshot*reborder.png' -print0 | xargs -0 stat -f '%m %N' | sort -rn | head -1 | cut -f2- -d" "
  popd
end

# Only keep a single copy of my ~/.terraform plugins, rather than one copy
# per working directory
# See https://www.terraform.io/docs/configuration/providers.html#provider-plugin-cache
set -x TF_PLUGIN_CACHE_DIR ~/.terraform.d/plugin-cache


###############################################################################
# virtualfish -- a fish wrapper for virtualenv
# https://github.com/adambrenecki/virtualfish
###############################################################################
set -g VIRTUALFISH_VERSION 2.4.0
set -g VIRTUALFISH_PYTHON_EXEC /usr/local/opt/python@3.8/bin/python3.8
source ~/Library/Python/3.8/lib/python/site-packages/virtualfish/virtual.fish
emit virtualfish_did_setup_plugins

###############################################################################
# Other fish config files
###############################################################################

. $DIR/_prompt.fish
. $DIR/_git.fish
. $DIR/_dockerfiles.fish
. $DIR/_imdown.fish
. $DIR/_twitter.fish
. $DIR/_wellcome.fish
. $DIR/_completions.fish

# Load macOS-specific utilities
if [ (uname -s) = "Darwin" ]
    . $DIR/_macos.fish
end
