# MIT License
#
# Copyright (c) 2022 Quandela
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# As a special exception, the copyright holders of exqalibur library give you
# permission to combine exqalibur with code included in the standard release of
# Perceval under the MIT license (or modified versions of such code). You may
# copy and distribute such a combined system following the terms of the MIT
# license for both exqalibur and Perceval. This exception for the usage of
# exqalibur is limited to the python bindings used by Perceval.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .statevector import BSDistribution, BSCount, BSSamples

import math
import numpy as np
import random


def _deduce_count(count: int, **kwargs) -> int:
    if count is not None:
        return count
    max_shots = kwargs.get("max_shots", None)
    max_samples = kwargs.get("max_samples", None)
    if max_shots is not None and max_samples is not None:
        return min(max_samples, max_shots)  # Not accurate in terms of shot limit
    count = max_shots or max_samples
    if count is None:
        raise RuntimeError("kwargs does not contain sample count information")
    return count


# Conversion functions (samples <=> probs <=> sample_count)
def samples_to_sample_count(sample_list: BSSamples) -> BSCount:
    results = BSCount()
    for s in sample_list:
        if s not in results:
            results[s] = sample_list.count(s)
    return results


def samples_to_probs(sample_list: BSSamples) -> BSDistribution:
    return sample_count_to_probs(samples_to_sample_count(sample_list))


def probs_to_sample_count(probs: BSDistribution, count: int = None, **kwargs) -> BSCount:
    count = _deduce_count(count, **kwargs)
    perturbed_dist = {state: max(prob + np.random.normal(scale=(prob * (1 - prob) / count) ** .5), 0)
                      for state, prob in probs.items()}
    prob_sum = sum(prob for prob in perturbed_dist.values())
    if prob_sum == 0:
        return samples_to_sample_count(probs_to_samples(probs, count))
    fac = 1 / prob_sum
    perturbed_dist = {key: fac * prob for key, prob in perturbed_dist.items()}  # Renormalisation
    results = BSCount()
    for state in perturbed_dist:
        results.add(state, round(perturbed_dist[state] * count))
    # Artificially deal with the rounding errors
    diff = round(count - sum(list(results.values())))
    if diff > 0:
        results[random.choice(list(results.keys()))] += diff
    elif diff < 0:
        while diff < 0:
            k = random.choice(list(results.keys()))
            current_diff = max(-results[k], diff)
            diff -= current_diff
            results[k] += current_diff
    return results


def probs_to_samples(probs: BSDistribution, count: int = None, **kwargs) -> BSSamples:
    count = _deduce_count(count, **kwargs)
    return probs.sample(count)


def sample_count_to_probs(sample_count: BSCount) -> BSDistribution:
    bsd = BSDistribution()
    for state, count in sample_count.items():
        if count == 0:
            continue
        if count < 0:
            raise RuntimeError(f"A sample count must be positive (got {count})")
        bsd[state] = count
    bsd.normalize()
    return bsd


def sample_count_to_samples(sample_count: BSCount, count: int = None, **kwargs) -> BSSamples:
    try:
        count = _deduce_count(count, **kwargs)
    except RuntimeError:
        count = sum([v for v in sample_count.values()])
    return sample_count_to_probs(sample_count).sample(count)
