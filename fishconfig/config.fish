set -x DIR (cd (dirname (status -f)); and pwd)
set -x ROOT (dirname $DIR)
cd ~


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

# A useful alias for quickly tallying a set of data
alias tally "sort | uniq -c | sort"

# Quickly create and cd to a temporary directory
function tmpdir
    cd (mktemp -d)
end

# Alias for finding out which subdirectories of the current dir contain
# the most files.  Useful when trying to find wasted disk space.
alias cdir 'for l in (ls); if [ -d $l ]; echo (find $l | wc -l)"  $l"; end; end | sort'


###############################################################################
# virtualfish -- a fish wrapper for virtualenv
# https://github.com/adambrenecki/virtualfish
###############################################################################
eval (python3 -m virtualfish auto_activation) >> /dev/null 2>&1


###############################################################################
# Other fish config files
###############################################################################

. $DIR/prompt.fish
. $DIR/git.fish
. $DIR/_aws.fish
. $DIR/_docker.fish
. $DIR/_dockerfiles.fish
. $DIR/_imdown.fish
. $DIR/_twitter.fish
. $DIR/_wellcome.fish

# Load macOS-specific utilities
if [ (uname -s) = "Darwin" ]
    . $DIR/_macos.fish
end

if [ (hostname) = "Alexs-MacBook-2" -o (hostname) = "Alexs-MacBook-2.local" ]
  . $DIR/_macbook.fish
end

if [ (hostname) = "Alexs-iMac.local" ]
  . $DIR/_imac.fish
end
