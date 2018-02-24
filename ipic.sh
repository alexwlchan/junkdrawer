#!/usr/local/bin/fish
# This is hard-coded rather than using /usr/bin/env because Alfred (which
# is where this script is called from) doesn't seem to be able to find
# fish in /usr/bin/env.

set term "$argv"

pushd (mktemp -d)
  echo "<html>"                                                   >  index.html
  echo "<head>"                                                   >> index.html
  echo "<title>$term</title>"                                     >> index.html
  echo "<style>img {max-width:150px; max-height:150px;}</style>"  >> index.html
  echo "</head>"                                                  >> index.html
  echo "<body><h1>&ldquo;$term&rdquo; results</h1>"               >> index.html

  curl --get "https://itunes.apple.com/search" --data-urlencode "term=$term" > api.txt
  cat api.txt | jq '.results' | jq -c '.[]' | jq -r '.artworkUrl100' > results.txt
  cat results.txt | sort | uniq > uniq.txt

  while read line
    set url (echo $line | sed 's/100x100/600x600/g')
    echo "<a href=$url><img src=\"$url\"></a>"                    >> index.html
  end < uniq.txt

  echo "</body></html>"                                           >> index.html

  open -a Safari index.html
popd
