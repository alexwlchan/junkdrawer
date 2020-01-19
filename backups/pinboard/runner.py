import concurrent.futures
import itertools
import subprocess


HOW_MANY_TASKS_AT_ONCE = 5


def process_concurrent(perform, tasks_to_do):
    """https://alexwlchan.net/2019/10/adventures-with-concurrent-futures/"""
    tasks_to_do = iter(tasks_to_do)

    with concurrent.futures.ThreadPoolExecutor() as executor:

        # Schedule the first N futures.  We don't want to schedule them all
        # at once, to avoid consuming excessive amounts of memory.
        futures = {
            executor.submit(perform, task)
            for task in itertools.islice(tasks_to_do, HOW_MANY_TASKS_AT_ONCE)
        }

        while futures:
            # Wait for the next future to complete.
            done, futures = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                yield fut.result()

            # Schedule the next set of futures.  We don't want more than N futures
            # in the pool at a time, to keep memory consumption down.
            for task in itertools.islice(tasks_to_do, len(done)):
                futures.add(executor.submit(perform, task))


def wget(*args):
    subprocess.call(["wget"] + list(args), stdout=subprocess.DEVNULL)
