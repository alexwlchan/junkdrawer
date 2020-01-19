#!/usr/bin/env ruby

require "test/unit"

require_relative "./helpers"


def manhattan_distance(a, b)
  (a[0] - b[0]).abs + (a[1] - b[1]).abs
end


def find_largest_finite_area(coords)
  # Anything outside the bounding box is part of an infinite area, and so
  # we can restrict our attendion to this box.
  min_x = coords.map { |c| c[0] }.min
  max_x = coords.map { |c| c[0] }.max

  min_y = coords.map { |c| c[1] }.min
  max_y = coords.map { |c| c[1] }.max

  closest_coords = Hash.new()

  # First we walk the entire board, and at each point we compute the Manhattan
  # distance between it and the named coordinates.
  #
  # We store the IDs in a hash so we can tell them apart.
  #
  (min_x..max_x).each { |x|
    (min_y..max_y).each { |y|
      current_coord = [x, y]

      distances_to_named_coords = coords.each_with_index
        .map { |coord, index| [index, manhattan_distance(current_coord, coord)] }
        .to_h

      closest_named, distance = distances_to_named_coords.min_by { |k, v| v }

      # If this is a uniquely close point, we count it -- if it's equidistant
      # to two or more named coordinates, we don't.
      if distances_to_named_coords.values.count(distance) == 1
        closest_coords[current_coord] = closest_named
      else
        closest_coords[current_coord] = nil
      end
    }
  }

  # Now we find which of the named coordinates has the most "closest" points.
  counter = Hash.new(0)
  closest_coords.map { |_, label| counter[label] += 1 }

  # 'nil' is used for all the points that are equidistant to one of more
  # named coordinates, but we don't care about those.
  if counter.key? nil
    counter.delete(nil)
  end

  # If any coordinate is on the edge of the board, it must be part of an
  # infinite area, so we discard it.
  (min_x..max_x).each { |x|
    [min_y, max_y].map { |y|

      # If we've already eliminated all but one area, that must be the only
      # finite area.  (Assuming the puzzle is soluble!)
      if counter.size == 1
        break
      end

      if counter.key? closest_coords[[x, y]]
        counter.delete(closest_coords[[x, y]])
      end
    }
  }

  (min_y..max_y).each { |y|
    [min_x, max_x].map { |x|
      if counter.size == 1
        break
      end

      if counter.key? closest_coords[[x, y]]
        counter.delete(closest_coords[[x, y]])
      end
    }
  }

  counter.values.max
end


def count_coords_in_safe_region(coords, safe_distance)
  # Anything outside the bounding box is part of an infinite area, and so
  # we can restrict our attendion to this box.
  min_x = coords.map { |c| c[0] }.min
  max_x = coords.map { |c| c[0] }.max

  min_y = coords.map { |c| c[1] }.min
  max_y = coords.map { |c| c[1] }.max

  safe_count = 0

  # First we walk the entire board, and at each point we compute the Manhattan
  # distance between it and the named coordinates.
  #
  # We store the IDs in a hash so we can tell them apart.
  #
  (min_x..max_x).each { |x|
    (min_y..max_y).each { |y|
      current_coord = [x, y]

      distances_to_named_coords = coords.each_with_index
        .map { |coord, index| [index, manhattan_distance(current_coord, coord)] }
        .to_h

      if distances_to_named_coords.values.sum < safe_distance
        safe_count += 1
      end
    }
  }

  safe_count
end


class TestDay6 < Test::Unit::TestCase
  def test_examples
    assert_equal find_largest_finite_area([
      [1, 1],
      [1, 6],
      [8, 3],
      [3, 4],
      [5, 5],
      [8, 9],
      ]), 17

    assert_equal count_coords_in_safe_region([
      [1, 1],
      [1, 6],
      [8, 3],
      [3, 4],
      [5, 5],
      [8, 9],
      ], 32), 16
  end

  def test_ignores_infinite_areas
    # On this grid, only the area "c" counts, because it's the only finite
    # area.
    #
    #     aaaAaaa..bbB
    #     daaaaa.cc.bb
    #     ddaaa.cccc.b
    #     ddd..cccCcc.
    #     ddddd.cccc.e
    #     dddddd.cc.ee
    #     ddDdddd..eeE
    #
    assert_equal find_largest_finite_area([
      [1, 1],   # A
      [9, 1],   # B
      [6, 4],   # C
      [1, 7],   # D
      [9, 7]    # E
    ]), 18
  end
end


if __FILE__ == $0
  input = File.read("6.txt").split("\n")
    .map { |line| line.split(",").map { |s| s.to_i } }

  answer1 = find_largest_finite_area(input)
  answer2 = count_coords_in_safe_region(input, 10000)

  solution("6", "Chronal Coordinates", answer1, answer2)
end
