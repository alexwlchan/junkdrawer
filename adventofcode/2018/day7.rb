#!/usr/bin/env ruby

require "set"
require "test/unit"

require_relative "./helpers"


REQUIREMENT_RE = /Step (?<blocker>[A-Z]) must be finished before step (?<step>[A-Z]) can begin\./


def parse_input(input)
  dependencies = Hash.new()

  input
    .strip
    .split("\n")
    .map { |line| REQUIREMENT_RE.match(line) }
    .each { |match|
      step = match["step"]
      blocker = match["blocker"]

      if dependencies.key? step
        dependencies[step].add(blocker)
      else
        dependencies[step] = Set[blocker]
      end

      if !dependencies.key? blocker
        dependencies[blocker] = Set.new
      end
    }

  dependencies
end


def find_correct_order(dependencies)
  remaining = Hash.new
  dependencies.each { |k, v| remaining[k] = v.clone }
  procedure = ""

  while remaining.size > 0
    # Find all the steps which are "available" -- that is, nothing in the
    # remaining tree depends on them.
    available_steps = remaining
      .select { |step, blockers| blockers.size == 0 }
      .map { |step, blockers| step }
      .sort

    # Now we take the first available step, add it to the procedure, and
    # remove it from any remaining steps that contain it.
    next_step = available_steps[0]
    procedure += next_step

    remaining.delete(next_step)

    remaining
      .each { |step, blockers| blockers.delete? next_step }
  end

  procedure
end


def length_of_step(c, base_task_time)
  c.ord - ("A".ord - (base_task_time + 1))
end


def find_parallel_runtime(dependencies, elf_count: 0, base_task_time: 0)
  remaining = Hash.new
  dependencies.each { |k, v| remaining[k] = v.clone }
  elves = (1..elf_count)
    .map { |i| {"id" => i, "current_step" => nil, "remaining" => nil} }

  t = 0

  # We continue while there are still steps to start, or there are elves
  # who are doing some current work.
  while remaining.size > 0 || elves.select { |e| !e["current_step"].nil? }.size > 0

    # Go through and decrement a second from each task the elves are
    # currently working on.  If one of them ahas finished a task, we
    # can unassign them and mark that task as unblocked.
    elves
      .select { |e| !e["current_step"].nil? }
      .each { |e|
        e["remaining"] -= 1
        if e["remaining"] == 0
          remaining.each { |step, blockers| blockers.delete? e["current_step"] }
          e["current_step"] = nil
          e["remaining"] = nil
        end
      }

    # Work through the elves that don't have anything to do right now,
    # and assign them a task.
    while (
      elves.select { |e| e["current_step"].nil? }.size > 0 &&
      remaining.select { |step, blockers| blockers.size == 0 }.size > 0)
        elf = elves
          .select { |e| e["current_step"].nil? }
          .first
        step = remaining
          .select { |step, blockers| blockers.size == 0 }
          .map { |step, blockers| step }
          .sort
          .first

        # We add one to the time remaining to account for the time taken
        # on this step.
        elf["current_step"] = step
        elf["remaining"] = length_of_step(step, base_task_time)

        # And now we remove the task from "remaining" so nobody else
        # can claim it.
        remaining.delete(step)
    end

    t += 1
  end

  # The final step will be entirely idle, so we skip one.
  t - 1
end



class TestDay7 < Test::Unit::TestCase
  def test_examples
    dependencies = parse_input("""
      Step C must be finished before step A can begin.
      Step C must be finished before step F can begin.
      Step A must be finished before step B can begin.
      Step A must be finished before step D can begin.
      Step B must be finished before step E can begin.
      Step D must be finished before step E can begin.
      Step F must be finished before step E can begin.
    """)

    assert_equal find_correct_order(dependencies), "CABDFE"

    assert_equal length_of_step("A", 60), 61
    assert_equal length_of_step("Z", 60), 86

    assert_equal find_parallel_runtime(dependencies, elf_count: 2), 15
  end
end


if __FILE__ == $0
  input = File.read("7.txt")
  dependencies = parse_input(input)

  answer1 = find_correct_order(dependencies)
  answer2 = find_parallel_runtime(dependencies, elf_count: 4, base_task_time: 60)

  solution("7", "The Sum of Its Parts", answer1, answer2)
end
