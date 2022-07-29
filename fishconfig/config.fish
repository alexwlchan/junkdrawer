set -x DIR ~/repos/junkdrawer/fishconfig
set -x ROOT (dirname $DIR)

# Name of the current branch
# http://stackoverflow.com/a/12142066/1558022
alias gcb="git rev-parse --abbrev-ref HEAD"


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
append_dir_to_path ~/Library/Python/3.9/bin

append_dir_to_path ~/repos/ttml2srt
append_dir_to_path ~/repos/pathscripts

append_dir_to_path "$DIR/pathscripts"

export NVM_DIR="$HOME/.nvm"
bash /usr/local/opt/nvm/nvm.sh

# Quickly create and cd to a temporary directory
function tmpdir
    cd (mktemp -d)
end

function scratch
    set DIR ~/"Desktop/scratch/scratch."(date +"%Y-%m-%d")"."(openssl rand -hex 4)
    mkdir -p "$DIR"
    cd "$DIR"
end

function reload_fish_config
  . ~/.config/fish/config.fish
end

# Only keep a single copy of my ~/.terraform plugins, rather than one copy
# per working directory
# See https://www.terraform.io/docs/configuration/providers.html#provider-plugin-cache
set -x TF_PLUGIN_CACHE_DIR ~/.terraform.d/plugin-cache

###############################################################################
# Other fish config files
###############################################################################

. $DIR/_prompt.fish
. $DIR/_twitter.fish

if [ (uname -s) = "Darwin" ]
    alias furl "~/.cargo/bin/safari url"

    function gh-clone
        github-clone (~/.cargo/bin/safari url)
    end
end

# This means NoMAD won't nag me as long as I have a Terminal
# window open (which is basically always, haha)
if [ (hostname) = "WTC02DT99KML7H" ]
	bash $DIR/pathscripts/killall_nomad.sh &
end

alias imgcat=$HOME/.iterm2/imgcat;alias imgls=$HOME/.iterm2/imgls;alias it2api=$HOME/.iterm2/it2api;alias it2attention=$HOME/.iterm2/it2attention;alias it2check=$HOME/.iterm2/it2check;alias it2copy=$HOME/.iterm2/it2copy;alias it2dl=$HOME/.iterm2/it2dl;alias it2getvar=$HOME/.iterm2/it2getvar;alias it2git=$HOME/.iterm2/it2git;alias it2setcolor=$HOME/.iterm2/it2setcolor;alias it2setkeylabel=$HOME/.iterm2/it2setkeylabel;alias it2ul=$HOME/.iterm2/it2ul;alias it2universion=$HOME/.iterm2/it2universion

function cddir
    cd $argv[1]
    cdir
end
