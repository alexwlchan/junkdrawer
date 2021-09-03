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


function fish_prompt
  # Put a newline between new prompts for cleanliness, but not on the first run.
  if test \( -f "/tmp/$TERM_SESSION_ID" -o -f "/tmp/$XDG_SESSION_ID" \)
    echo ''
  end

  touch /tmp/$TERM_SESSION_ID 2>/dev/null
  touch /tmp/$XDG_SESSION_ID 2>/dev/null

  if [ (prompt_pwd) = "~" ]
    echo '$ '
    return
  end

  # Print the current directory
  set_color green
  printf (echo -n (prompt_pwd))

  # Add information about the current VCS
  parse_git_branch

  # Finally, print the shell prompt.  We have a slightly different prompt
  # for root users.
  set_color normal
  if [ "$USER" = "root" ]
    echo '' & echo '# '
  else
    echo '' & echo '$ '
  end
end
