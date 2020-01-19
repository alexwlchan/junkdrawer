#!/usr/bin/env ruby

require "test/unit"

require_relative "./helpers"


def calculate_letter_frequency(s)
  tally = Hash.new(0)
  s.each_char { |c| tally[c] += 1 }
  tally
end


def calculate_checksum(strings)
  frequencies = strings
    .map { |s| calculate_letter_frequency(s) }
    .map { |t| t.values }

  double_letters = frequencies.select { |f| f.include? 2 }.size
  triple_letters = frequencies.select { |f| f.include? 3 }.size

  double_letters * triple_letters
end


def find_differing_strings(strings)
  # First check all the strings are the same length
  s_length = strings[0].length
  strings.each { |s| raise "Inconsistent lengths" unless s.length == s_length }

  # Now we iterate through each index.  To find similar strings, we replace the
  # nth character with ?, and stuff them in a counter.  If any string appears twice
  # in the counter, we know we've found the correct string.
  (0..s_length).map { |index|
    counter = Hash.new(0)
    strings
      .map { |s|
        t = s.dup
        t[index] = "?"
        t
      }
      .map { |s| counter[s] += 1}
    if counter.values.max == 2
      counter.map { |k, v|
        if v >= 2
          return k.sub("?", "")
        end
      }
    end
  }
end


class TestDay2 < Test::Unit::TestCase
  def test_examples
    assert_equal calculate_checksum([
      "abcdef",
      "bababc",
      "abbcde",
      "abcccd",
      "aabcdd",
      "abcdee",
      "ababab"
    ]), 12

    assert_equal find_differing_strings([
      "abcde",
      "fghij",
      "klmno",
      "pqrst",
      "fguij",
      "axcye",
      "wvxyz",
    ]), "fgij"
  end
end


if __FILE__ == $0
  input = File.read("2.txt").split("\n")
  answer1 = calculate_checksum(input)
  answer2 = find_differing_strings(input)
  solution("2", "Inventory Management System", answer1, answer2)
end
