#!/usr/bin/env ruby

require "set"
require "test/unit"

require_relative "./helpers"


def calculate_frequency(changes)
  changes
    .map { |s| s.to_i }
    .inject(:+)
end


def find_first_duplicate_frequency(changes)
  current_freq = 0
  already_seen = Set.new([0])
  while true
    changes
      .map { |s| s.to_i }
      .each { |freq|
        current_freq += freq
        if already_seen.include? current_freq
          return current_freq
        else
          already_seen.add(current_freq)
        end
      }
  end
end


class TestDay1 < Test::Unit::TestCase
  def test_examples
    assert_equal calculate_frequency("+1, +1, +1".split(", ")), 3
    assert_equal calculate_frequency("+1, +1, -2".split(", ")), 0
    assert_equal calculate_frequency("-1, -2, -3".split(", ")), -6

    assert_equal find_first_duplicate_frequency("+1, -1".split(", ")), 0
    assert_equal find_first_duplicate_frequency("+3, +3, +4, -2, -4".split(", ")), 10
    assert_equal find_first_duplicate_frequency("-6, +3, +8, +5, -6".split(", ")), 5
    assert_equal find_first_duplicate_frequency("+7, +7, -2, -7, -4".split(", ")), 14
  end
end


if __FILE__ == $0
  input = File.read("1.txt").split("\n")
  answer1 = calculate_frequency(input)
  answer2 = find_first_duplicate_frequency(input)
  solution("1", "Chronal Calibration", answer1, answer2)
end
