###############################################################################
# My fish prompt
###############################################################################

set -g -x fish_greeting ''


function parse_git_branch
  which git 2>&1 >/dev/null
  if [ $status = "0" ]
    set branch (git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
    if [ -n "$branch" ]
      set_color normal
      printf " on git:"
      set_color cyan
      printf "$branch"
    end
  end
end


function _display_hostname
  if test (sysctl hw.model 2>/dev/null | grep iMac)
    printf "🖥️ "
  else if test (sysctl hw.model 2>/dev/null | grep MacBook)
    printf "💻"
  else if test (sysctl kernel.osrelease 2>/dev/null | grep linode)
    printf "☁️ "
  else
    printf (hostname)
  end
end


function fish_prompt
  # A newline between new prompts for cleanliness
  echo ''

  # If we're in a virtualenv, print the venv name
  if set -q VIRTUAL_ENV
    echo -n -s (set_color yellow) "(" (basename "$VIRTUAL_ENV") ") "
  end

  # Print the username
  set_color magenta
  printf (eval whoami)

  # Print the hostname
  set_color normal
  printf (echo ' at ')
  set_color yellow
  _display_hostname

  # Print the current directory
  set_color normal
  printf (echo ' in ')
  set_color green
  printf (echo -n (prompt_pwd))

  # Add information about the current VCS
  parse_git_branch

  if set -q AWS_PROFILE
    if test -n "$AWS_PROFILE"
      echo -n -s (set_color yellow) " [👤 $AWS_PROFILE]"
    end
  end

  # Finally, print the shell prompt.  We have a slightly different prompt
  # for root users.
  set_color normal
  if [ "$USER" = "root" ]
    echo '' & echo '# '
  else
    echo '' & echo '$ '
  end
end
