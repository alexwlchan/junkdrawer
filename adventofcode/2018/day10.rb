#!/usr/bin/env ruby

require "set"
require "test/unit"

require_relative "./helpers"


INPUT_RE = /position=<(?<x>[\d\s\-]+), (?<y>[\d\s\-]+)> velocity=<(?<v_x>[\d\s\-]+), (?<v_y>[\d\s\-]+)>/


def parse_input(s)
  m = INPUT_RE.match(s)
  {
    "x" => m["x"].to_i,
    "y" => m["y"].to_i,
    "v_x" => m["v_x"].to_i,
    "v_y" => m["v_y"].to_i,
  }
end


def find_time_of_message(lights)
  t = 0
  y_heights = []

  while true
    y_coords = lights.map { |coord|
      coord["y"] + coord["v_y"] * t
    }

    # When the message is visible, the y-coordinates will be as tight as possible.
    # When it diverges, the y-coordinates will start to increase again.
    y_heights << y_coords.max - y_coords.min

    if y_heights.size < 3
      next
    else
      if y_heights[-1] > y_heights[-2] and y_heights[-2] < y_heights[-3]
        return t - 1
      end
    end

    t += 1
  end
end


def draw_message(lights, t: 0)
  message_coords = lights
    .map { |c| [c["x"] + c["v_x"] * t, c["y"] + c["v_y"] * t] }
    .to_set

  x_values = message_coords.map { |coord| coord[0] }
  y_values = message_coords.map { |coord| coord[1] }

  # Find the bounds of the box to draw.  The -1/+1 ensures an empty border
  # around the edge to make the image easier to see.
  x_min = x_values.min - 1
  x_max = x_values.max + 1

  y_min = y_values.min - 1
  y_max = y_values.max + 1

  (y_min..y_max).map { |y|
    (x_min..x_max).map { |x|
      if message_coords.include? [x, y]
        print "# "
      else
        print "· "
      end

      if x == x_max
        puts "\n"
      end
    }
  }
end


class TestDay9 < Test::Unit::TestCase
  def test_examples
    example = """position=< 9,  1> velocity=< 0,  2>
    position=< 7,  0> velocity=<-1,  0>
    position=< 3, -2> velocity=<-1,  1>
    position=< 6, 10> velocity=<-2, -1>
    position=< 2, -4> velocity=< 2,  2>
    position=<-6, 10> velocity=< 2, -2>
    position=< 1,  8> velocity=< 1, -1>
    position=< 1,  7> velocity=< 1,  0>
    position=<-3, 11> velocity=< 1, -2>
    position=< 7,  6> velocity=<-1, -1>
    position=<-2,  3> velocity=< 1,  0>
    position=<-4,  3> velocity=< 2,  0>
    position=<10, -3> velocity=<-1,  1>
    position=< 5, 11> velocity=< 1, -2>
    position=< 4,  7> velocity=< 0, -1>
    position=< 8, -2> velocity=< 0,  1>
    position=<15,  0> velocity=<-2,  0>
    position=< 1,  6> velocity=< 1,  0>
    position=< 8,  9> velocity=< 0, -1>
    position=< 3,  3> velocity=<-1,  1>
    position=< 0,  5> velocity=< 0, -1>
    position=<-2,  2> velocity=< 2,  0>
    position=< 5, -2> velocity=< 1,  2>
    position=< 1,  4> velocity=< 2,  1>
    position=<-2,  7> velocity=< 2, -2>
    position=< 3,  6> velocity=<-1, -1>
    position=< 5,  0> velocity=< 1,  0>
    position=<-6,  0> velocity=< 2,  0>
    position=< 5,  9> velocity=< 1, -2>
    position=<14,  7> velocity=<-2,  0>
    position=<-3,  6> velocity=< 2, -1>"""

    lights = example.split("\n").map { |s|
      parse_input(s)
    }

    assert_equal find_time_of_message(lights), 3
  end
end


if __FILE__ == $0
  inputs = File.read("10.txt").split("\n").map { |s| parse_input(s) }

  puts "--- Day 10: The Stars Align ---"

  t = find_time_of_message(inputs)

  draw_message(inputs, t: t)

  puts "You need to wait #{t} seconds"
end
