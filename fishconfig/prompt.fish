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


function parse_svn_branch
  which svn > /dev/null 2>&1
  if [ $status = "0" ]
    set branch (svn info 2> /dev/null | sed -n "/URL:/s/.*\///p")
    if [ -n "$branch" ]
      set_color normal
      printf " on svn:"
      set_color cyan
      printf "$branch"
    end
  end
end


function parse_hg_branch
  which hg > /dev/null 2>&1
  if [ $status = "0" ]
    set branch (hg branch 2> /dev/null | awk '{print $1}')
    if [ -n "$branch" ]
      set_color normal
      printf " on hg:"
      set_color cyan
      printf "$branch"
    end
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
  printf (hostname)

  # Print the current directory
  set_color normal
  printf (echo ' in ')
  set_color green
  printf (echo -n (prompt_pwd))

  # Add information about the current VCS
  parse_git_branch
  parse_svn_branch
  parse_hg_branch

  # Finally, print the shell prompt.  We have a slightly different prompt
  # for root users.
  set_color normal
  if [ "$USER" = "root" ]
    echo '' & echo '# '
  else
    echo '' & echo '$ '
  end
end
