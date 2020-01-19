#!/usr/bin/env ruby

require "test/unit"

require_relative "./helpers"


INPUT_RE = /(?<players>\d+) players; last marble is worth (?<last_marble>\d+) points/


def parse_input(s)
  m = INPUT_RE.match(s)
  {
    "players" => m["players"].to_i,
    "last_marble" => m["last_marble"].to_i
  }
end


class Node
  attr_accessor :value, :clockwise, :counter_clockwise
  def initialize(value, clockwise: nil, counter_clockwise: nil)
    @value = value
    @clockwise = clockwise
    @counter_clockwise = counter_clockwise
  end

  def ==(other)
    self.value == other.value
  end

  def to_s
    "Node(#{@value}, clockwise = #{@clockwise.value}, counter_clockwise = #{@counter_clockwise.value})"
  end
end


class MarbleCircle
  attr_accessor :current
  def initialize
    @current = Node.new(0)
    @current.clockwise = @current
    @current.counter_clockwise = @current
  end

  def play_marble(value)
    if value % 23 == 0
      # We step back 7 marbles counter-clockwise, then remove it from the circle.
      (1..7).map { |_|
        @current = @current.counter_clockwise
      }

      # We now have a setup like follows
      #
      #     A -> c-wise                                                 cc-wise <- B
      #                    cc-wise <- (about to be removed) -> c-wise
      #
      about_to_be_removed = @current
      marble_A = @current.counter_clockwise
      marble_B = @current.clockwise

      marble_A.clockwise = marble_B
      marble_B.counter_clockwise = marble_A

      @current = @current.clockwise
      [value, about_to_be_removed.value]
    else
      # The node places the new marble at a point between 1 and 2 marbles clockwise
      # of the current marble -- so advance one point clockwise first.
      @current = @current.clockwise

      # The existing set up is as follows:
      #
      #     @current -> c-wise                                             cc-wise <- A
      #                        cc-wise <- (about to be inserted) -> c-wise
      marble_A = @current.clockwise
      new_marble = Node.new(
        value,
        clockwise: marble_A,
        counter_clockwise: @current
      )

      @current.clockwise = new_marble
      marble_A.counter_clockwise = new_marble

      @current = new_marble

      nil
    end
  end

  def to_s
    values = []
    looking_at = @current
    while true
      looking_at = looking_at.clockwise
      values << looking_at.value
      if looking_at == @current
        break
      end
    end

    while values[0] != 0
      values << values.delete_at(0)
    end

    rv = ""
    values.map { |v|
      if v == @current.value
        rv += "(#{v})"
      else
        rv += " #{v} "
      end
    }
    rv
  end
end


def play_game(players: 1, last_marble: 1)
  circle = MarbleCircle.new

  scores = (0...players).map { |p| [p, Array.new] }.to_h

  (1..last_marble).each { |m|
    score = circle.play_marble(m)
    if !score.nil?
      scores[m % players] += score
    end
  }

  scores.map { |player, values| [player, values.sum] }.to_h
end


def get_high_score(input_data)
  scores = play_game(
    players: input_data["players"],
    last_marble: input_data["last_marble"]
  )
  scores.values.max
end


class TestDay9 < Test::Unit::TestCase
  def test_examples
    assert_equal get_high_score(parse_input("9 players; last marble is worth 25 points")), 32
    assert_equal get_high_score(parse_input("10 players; last marble is worth 1618 points")), 8317
    assert_equal get_high_score(parse_input("13 players; last marble is worth 7999 points")), 146373
    assert_equal get_high_score(parse_input("17 players; last marble is worth 1104 points")), 2764
    assert_equal get_high_score(parse_input("21 players; last marble is worth 6111 points")), 54718
    assert_equal get_high_score(parse_input("30 players; last marble is worth 5807 points")), 37305
  end
end


if __FILE__ == $0
  input = parse_input(File.read("9.txt"))

  answer1 = get_high_score(input)

  input["last_marble"] *= 100
  answer2 = get_high_score(input)

  solution("9", "Marble Mania", answer1, answer2)
end
