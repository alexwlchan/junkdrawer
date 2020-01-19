#!/usr/bin/env ruby

require "test/unit"

require_relative "./helpers"


class Node
  attr_accessor :child_nodes
  attr_accessor :metadata_entries

  def initialize(child_nodes: [], metadata_entries: [])
    @child_nodes = child_nodes
    @metadata_entries = metadata_entries
  end

  def ==(other)
    other.class == self.class && other.child_nodes == self.child_nodes && other.metadata_entries == self.metadata_entries
  end

  # How many values does this take up in the original license file?
  def size
    2 + child_nodes.map { |n| n.size }.sum + metadata_entries.size
  end

  def to_s
    "<Node child_nodes=#{child_nodes.inspect}, metadata_entries=#{metadata_entries.inspect}>"
  end

  def all_metadata_entries
    all = metadata_entries
    child_nodes.each { |n|
      all += n.all_metadata_entries
    }
    all
  end

  def value
    if child_nodes.size == 0
      metadata_entries.sum
    else
      # Remember to subtract 1 -- Ruby arrays are indexed from 0, not 1.
      metadata_entries
        .map { |m| child_nodes[m - 1] }
        .select { |maybe_child| !maybe_child.nil? }
        .map { |child| child.value }
        .sum
    end
  end
end


# Parse the first node in a list of numbers.  This method may not parse all
# the numbers, if the first node finishes before the end of the list.
def parse_first_node(numbers)
  child_node_count = numbers[0]
  metadata_count = numbers[1]

  # How far through the list are we?
  index = 2

  if child_node_count == 0
    Node.new(metadata_entries: numbers.slice(index, metadata_count))
  else
    child_nodes = []
    (1..child_node_count).each { |_|
      child_nodes << parse_first_node(numbers[index..-1])
      index += child_nodes[-1].size
    }
    Node.new(
      child_nodes: child_nodes,
      metadata_entries: numbers.slice(index, metadata_count)
    )
  end
end


class TestDay8 < Test::Unit::TestCase
  def test_examples
    node_B = Node.new(metadata_entries: [10, 11, 12])
    node_D = Node.new(metadata_entries: [99])
    node_C = Node.new(child_nodes: [node_D], metadata_entries: [2])
    node_A = Node.new(child_nodes: [node_B, node_C], metadata_entries: [1, 1, 2])

    assert_equal parse_first_node([0, 3, 10, 11, 12]), node_B
    assert_equal parse_first_node([1, 1, 0, 1, 99, 2]), node_C
    assert_equal parse_first_node([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]), node_A

    assert_equal node_B.value, 33
    assert_equal node_D.value, 99
    assert_equal node_C.value, 0
    assert_equal node_A.value, 66
  end
end


if __FILE__ == $0
  input = File.read("8.txt").split(" ").map { |s| s.to_i }
  root = parse_first_node(input)

  answer1 = root.all_metadata_entries.sum
  answer2 = root.value

  solution("8", "Memory Maneuver", answer1, answer2)
end
