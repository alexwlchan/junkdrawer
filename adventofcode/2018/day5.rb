#!/usr/bin/env ruby

require "test/unit"

require_relative "./helpers"


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def build_polymer_regexp
  # Construct a mega-regex of the form
  #
  #    (aA|Aa|bB|Bb...)
  #
  regex_components = []
  ALPHABET.each_char { |c|
    regex_components << "#{c}#{c.upcase}"
    regex_components << "#{c.upcase}#{c}"
  }

  Regexp.new "(#{regex_components.join("|")})"
end


POLYMER_REGEXP = build_polymer_regexp


def react_polymer(p)
  curr_size = p.size

  # Now iterate repeatedly until the polymer `p` is no longer changing size --
  # then we know we're done.
  #
  # This could be inefficient if the polymer is nested in a nasty way, e.g.
  #
  #     abcdefgGFEDCBA
  #
  # Oh well, I'll live with it.
  while true
    p = p.gsub(POLYMER_REGEXP, "")
    if p.size == curr_size
      return p
    else
      curr_size = p.size
    end
  end
end


def find_smallest_polymer_size_with_missing_unit(p)
  # Start by reducing the polymer as much as possible -- removing extra units
  # won't affect this reduction, but gives us a smaller starting point
  # when we do remove units.
  reduced_p = react_polymer(p)

  ALPHABET
    .each_char
    .map { |c|
      modified_p = reduced_p.gsub(c, "").gsub(c.upcase, "")
      react_polymer(modified_p).size
    }
    .min
end


class TestDay5 < Test::Unit::TestCase
  def test_examples
    assert_equal react_polymer("aA"), ""
    assert_equal react_polymer("abBA"), ""
    assert_equal react_polymer("abAB"), "abAB"
    assert_equal react_polymer("aabAAB"), "aabAAB"

    assert_equal find_smallest_polymer_size_with_missing_unit("dabAcCaCBAcCcaDA"), 4
  end
end


if __FILE__ == $0
  input = File.read("5.txt").strip

  answer1 = react_polymer(input).size
  answer2 = find_smallest_polymer_size_with_missing_unit(input)

  solution("5", "Alchemical Reduction", answer1, answer2)
end
