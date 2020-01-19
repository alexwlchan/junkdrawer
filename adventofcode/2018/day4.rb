#!/usr/bin/env ruby

require "test/unit"

require_relative "./helpers"


def tally_sleep_minutes(events)
  tally = Hash.new(nil)

  fell_asleep = nil

  events
    .each { |e|
      if e["event"] == "falls asleep"
        fell_asleep = e["minute"]
      elsif e["event"] == "wakes up"
        (fell_asleep...e["minute"]).each { |min|
          if !tally.key?(e["guard"])
            tally[e["guard"]] = Hash.new(0)
          end
          tally[e["guard"]][min] += 1
        }
      end
    }

  tally
end


def find_guard_who_spends_most_minutes_asleep(tally)
  minutes_asleep_by_guard = tally
    .map { |guard, sleep_minutes| [guard, sleep_minutes.values.sum] }

  minutes_asleep_by_guard.max_by { |guard, time_asleep| time_asleep }[0]
end


def find_guard_who_sleeps_most_on_same_minute(tally)
  tally
     .map { |guard, minutes| [guard, minutes.values.max] }
     .max_by { |guard, max_sleep_count| max_sleep_count }[0]
end


def find_most_frequent_sleep_minute(tally, guard)
  tally[guard].max_by { |min, count| count }[0]
end


def find_minute_most_often_asleep(tally, guard)
  tally[guard].max_by { |min, count| count }[0]
end


DATE_RE = /^\[(?<date>\d{4}\-\d{2}\-\d{2}) \d{2}:(?<minute>\d{2})\] (?<event>Guard #(?<guard>\d+) begins shift|falls asleep|wakes up)/


def parse_input(input)
  curr_guard = nil
  input
    .sort
    .select { |line| !line.strip.empty? }
    .map { |line| DATE_RE.match(line.strip) }
    .map { |m| m.named_captures }
    .each { |h|
      # Make sure that every event has an associated guard; use the last
      # guard we saw starting a shift.
      if h["guard"] != nil
        curr_guard = h["guard"]
      else
        h["guard"] = curr_guard
      end

      h["minute"] = h["minute"].to_i
    }
end


class TestDay4 < Test::Unit::TestCase
  def test_examples
    input = """
      [1518-11-01 00:00] Guard #10 begins shift
      [1518-11-01 00:05] falls asleep
      [1518-11-01 00:25] wakes up
      [1518-11-01 00:30] falls asleep
      [1518-11-01 00:55] wakes up
      [1518-11-01 23:58] Guard #99 begins shift
      [1518-11-02 00:40] falls asleep
      [1518-11-02 00:50] wakes up
      [1518-11-03 00:05] Guard #10 begins shift
      [1518-11-03 00:24] falls asleep
      [1518-11-03 00:29] wakes up
      [1518-11-04 00:02] Guard #99 begins shift
      [1518-11-04 00:36] falls asleep
      [1518-11-04 00:46] wakes up
      [1518-11-05 00:03] Guard #99 begins shift
      [1518-11-05 00:45] falls asleep
      [1518-11-05 00:55] wakes up
    """.split("\n")

    events = parse_input(input)
    tally = tally_sleep_minutes(events)

    assert_equal find_guard_who_spends_most_minutes_asleep(tally), "10"
    assert_equal find_minute_most_often_asleep(tally, "10"), 24

    assert_equal find_guard_who_sleeps_most_on_same_minute(tally), "99"
    assert_equal find_most_frequent_sleep_minute(tally, "99"), 45
  end
end


if __FILE__ == $0
  input = File.read("4.txt").split("\n")

  events = parse_input(input)
  tally = tally_sleep_minutes(events)

  most_asleep_guard = find_guard_who_spends_most_minutes_asleep(tally)
  minutes_asleep = find_minute_most_often_asleep(tally, most_asleep_guard)
  answer1 = most_asleep_guard.to_i * minutes_asleep

  guard_sleeps_most_on_same_minute = find_guard_who_sleeps_most_on_same_minute(tally)
  most_sleep_minute = find_most_frequent_sleep_minute(tally, guard_sleeps_most_on_same_minute)
  answer2 = guard_sleeps_most_on_same_minute.to_i * most_sleep_minute

  solution("4", "Repose Record", answer1, answer2)
end
