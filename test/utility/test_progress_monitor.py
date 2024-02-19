import multiprocessing as mp

import pytest

from hsc.utility import ProgressMonitor


@pytest.fixture(scope="module")
def monitor():
    return ProgressMonitor()


def test_print_progress(monitor):
    monitor.print_progress_bar(1, 1, "test prefix", "test suffix")


def test_pool_progress(monitor):
    def mock_payload(args):
        i, queue = args
        queue.put(i)

    n_threads = 4
    # setup multi-processing
    n_threads_actual = min([n_threads, mp.cpu_count()])
    pool = mp.Pool(processes=n_threads_actual)
    manager = mp.Manager()
    queue = manager.Queue()

    args = [(i, queue) for i in range(100)]
    result = pool.map_async(mock_payload, args)

    # monitoring loop
    ProgressMonitor.monitor_pool(
        result,
        queue,
        100,
        prefix="Test: ",
        suffix=f"Running on {n_threads_actual} threads.",
    )
