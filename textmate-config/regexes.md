# Regexes used for find and replace

For fixing up Python test assertions:

    self.assertEquals?\(([a-zA-Z_.0-9\[\]\(\)'"]+),\s*([a-zA-Z_.0-9\[\]\(\)'"]+)\)
    assert $1 == $2
