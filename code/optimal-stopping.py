import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

# The secretary-problem ->
# Goal: Hire the best secretary
# Conditions: Seeing a candidate, you can only hire or continue searching. You cannot go back. Number of candidates are known. Candidate come in randomly.

def create_candidates(n: int) -> Tuple[np.ndarray, int]:
    rng = np.random.default_rng()
    candidates = rng.random(n)
    best_idx = np.argmax(candidates)
    return candidates, best_idx

def choose_secretary(candidates: np.ndarray, looking: float) -> Tuple[int, float]:
    # looking
    best_performance = 0.0
    hire_idx = 0
    n_looking = round(len(candidates) * looking)
    for cIdx in range(n_looking):
        perf = candidates[cIdx]
        if perf > best_performance:
            best_performance = perf

    # leaping
    for cIdx in range(n_looking, len(candidates)):
        perf = candidates[cIdx]

        # take the first one better than in looking phase
        if perf > best_performance:
            best_performance = perf
            hire_idx = cIdx
            break

    return hire_idx, best_performance

def do_experiment(nbr_experiments, nbr_candidates, looking) -> float:
    successes = 0.0
    for nIdx in range(nbr_experiments):
        candidates, best_idx = create_candidates(nbr_candidates)
        hire_idx, best_perf = choose_secretary(candidates, looking)
        if best_idx == hire_idx:
            successes += 1.0

    return successes / nbr_experiments




if __name__ == "__main__":
    n_candidates = 1000
    n_experiments = 10000

    success_rates = []
    lookings = []

    for looking in np.arange(0.0, 1.0, 0.02):
        success = do_experiment(n_experiments, n_candidates, looking)
        success_rates.append(success)
        lookings.append(looking)

    fig, ax = plt.subplots()
    ax.plot(lookings, success_rates)

    ax.set(xlabel='Looking', ylabel='Success',
           title='Secretary Problem')
    ax.grid()
    plt.show()



