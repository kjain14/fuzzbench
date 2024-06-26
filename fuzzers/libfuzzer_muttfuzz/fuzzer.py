# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Integration code for AFLSmart fuzzer."""

import glob
import os
import shutil

from fuzzers.aflplusplus_muttfuzz import fuzzutil
from fuzzers.libfuzzer import fuzzer as libfuzzer_fuzzer


def build():
    """Build benchmark."""
    libfuzzer_fuzzer.build()


def restore_out(input_corpus, output_corpus, crashes_storage):
    """Restores output dir and copies crashes after mutant is done running"""
    # os.system(f"rm -rf {input_corpus}/*")
    # os.system(f"cp {output_corpus}/crashes/* {crashes_storage}/")
    # os.system(f"cp {output_corpus}/crashes/* {input_corpus}/")
    # os.system(f"cp {output_corpus}/corpus/* {input_corpus}/")
    # os.system(f"rm -rf {output_corpus}/*")
    pass


def fuzz(input_corpus, output_corpus, target_binary):
    """Run afl-fuzz on target."""
    print(f"{input_corpus} {output_corpus} {target_binary}")

    crashes_storage = "/storage"
    os.makedirs(crashes_storage, exist_ok=True)

    libfuzzer_fuzzer_fn = lambda: libfuzzer_fuzzer.fuzz(
        input_corpus, output_corpus, target_binary)

    budget = 86_400
    fraction_mutant = 0.5
    time_per_mutant = 300
    initial_budget = 1_800
    post_mutant_fn = lambda: restore_out(input_corpus, output_corpus,
                                         crashes_storage)
    fuzzutil.fuzz_with_mutants_via_function(
        libfuzzer_fuzzer_fn,
        target_binary,
        budget,
        time_per_mutant,
        fraction_mutant,
        initial_fn=libfuzzer_fuzzer_fn,
        initial_budget=initial_budget,
        post_initial_fn=post_mutant_fn,
        post_mutant_fn=post_mutant_fn,
    )
