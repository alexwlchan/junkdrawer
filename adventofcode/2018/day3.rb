#!/usr/bin/env ruby

require "set"
require "test/unit"

require_relative "./helpers"


def find_single_claim_area(left_offset, top_offset, width, height)
  coords = Set.new([])
  (1..width).map { |w|
    (1..height).map { |h|
      coords.add([left_offset + w, top_offset + h])
    }
  }
  raise "Incorrect size" unless coords.size == width * height
  coords
end


def tally_areas(all_claims)
  used_areas = Hash.new(0)
  all_claims.map { |claim|
    claimed_area = find_single_claim_area(
      claim["left_offset"],
      claim["top_offset"],
      claim["width"],
      claim["height"]
    )

    claimed_area.map { |coord|
      used_areas[coord] += 1
    }
  }
  used_areas
end


def count_overlapping_claims(all_claims)
  tally_areas(all_claims).values.select { |v| v > 1 }.size
end


def find_non_overlapping_claim(all_claims)
  used_areas = tally_areas(all_claims)

  all_claims.each { |claim|
    claimed_area = find_single_claim_area(
      claim["left_offset"],
      claim["top_offset"],
      claim["width"],
      claim["height"]
    )

    has_overlap = false
    claimed_area.map { |c|
      if used_areas[c] > 1
        has_overlap = true
        break
      end
    }

    if !has_overlap
      return claim["claim_id"]
    end
  }
end


class TestDay3 < Test::Unit::TestCase
  def test_examples
    assert_equal find_single_claim_area(3, 2, 5, 4), Set.new([
      [4, 3], [5, 3], [6, 3], [7, 3], [8, 3],
      [4, 4], [5, 4], [6, 4], [7, 4], [8, 4],
      [4, 5], [5, 5], [6, 5], [7, 5], [8, 5],
      [4, 6], [5, 6], [6, 6], [7, 6], [8, 6],
    ])

    assert_equal find_single_claim_area(3, 1, 4, 4), Set.new([
      [4, 2], [5, 2], [6, 2], [7, 2],
      [4, 3], [5, 3], [6, 3], [7, 3],
      [4, 4], [5, 4], [6, 4], [7, 4],
      [4, 5], [5, 5], [6, 5], [7, 5],
    ])

    test_claims = [
      {"claim_id" => "1", "left_offset" => 1, "top_offset" => 3, "width" => 4, "height" => 4},
      {"claim_id" => "2", "left_offset" => 3, "top_offset" => 1, "width" => 4, "height" => 4},
      {"claim_id" => "3", "left_offset" => 5, "top_offset" => 5, "width" => 2, "height" => 2},
    ]

    assert_equal count_overlapping_claims(test_claims), 4

    assert_equal find_non_overlapping_claim(test_claims), "3"
  end
end


CLAIM_RE = /^\#(?<claim_id>\d+) @ (?<left_offset>\d+),(?<top_offset>\d+): (?<width>\d+)x(?<height>\d+)$/


if __FILE__ == $0
  input = File.read("3.txt").split("\n")

  claims = input
    .map { |line| CLAIM_RE.match(line) }
    .map { |m| m.named_captures }
    .each { |data|
      ["left_offset", "top_offset", "width", "height"].each { |key|
        data[key] = data[key].to_i
      }
    }

  answer1 = count_overlapping_claims(claims)
  answer2 = find_non_overlapping_claim(claims)
  solution("3", "No Matter How You Slice It", answer1, answer2)
end
