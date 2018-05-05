# Based on http://brettterpstra.com/2018/05/04/shell-tricks-what-to-do-when-you-cant-do-internet/

function nag
  set last_phrase ""

  while true
    # Choose a random phrase, but make sure we don't pick the same phrase
    # twice in a row.
    set phrase (random choice $argv)
    if [ "$phrase" = "$last_phrase" ]
      continue
    end

    set last_phrase "$phrase"

    afplay /System/Library/Sounds/Ping.aiff
    say -v Samantha "$phrase"
    sleep 5
  end
end


function imdown
  while true
    ping -W1 -c1 1.1.1.1
    if [ "$status" = "0" ]
      break
    end
    sleep 10
  end
  nag \
    "internet connection is back up\!" \
    "Skynet is thinking" \
    "your tribulation is over, the internet is here" \
    "Praise what gods may be, we have internet\!" \
    "O M G we're online" \
    "In the words of Dr. Frankenstein, it's alive\!" \
    "rejoice, for the internet is risen"
end
