from src.jsdc_loader import jsdc_dump, jsdc_load # Focus on jsdc_dumps
from dataclasses import dataclass, field
from typing import List
import cProfile
import pstats
import io # Required for pstats output string
import time
from random import randint

@dataclass
class Test:
    name: str
    age: int

@dataclass
class Test_list:
    tests: List[Test]

print("Preparing test data (1 million items)...")
test_list_obj = Test_list(tests=[])
for i in range(100000): # Using 100000 as per user feedback
    test = Test(name="test", age=i)
    # if i >= 10000:
    #     # Randomly add mismatch type
    #     if randint(0, 1) == 0:
    #         test.age = "10"
    #     else:
    #         test.name = 10
    test_list_obj.tests.append(test)
print("Test data prepared.")

PROFILE_FILE = "dumps.prof"

# Profile jsdc_dumps
print(f"Profiling jsdc_dump and jsdc_load and saving to {PROFILE_FILE}...")
profiler = cProfile.Profile()
profiler.enable()
iterations = 4
start_time = time.time()

try:
    for i in range(iterations):
        datas = jsdc_dump(test_list_obj, output_path="test.json") # Default indent, no other kwargs
    print("Dumps complete.")
    print(f"Average Time taken: {(time.time() - start_time) / iterations} seconds")
    time.sleep(5)
    start_time = time.time()
    for i in range(iterations):
        gg = jsdc_load("test.json", Test_list)
    print("Loads complete.")
    print(f"Average Time taken: {(time.time() - start_time) / iterations} seconds")
except Exception as e:
    print(f"Error during profiling: {e}")
finally:
    profiler.disable()
    profiler.dump_stats(PROFILE_FILE)
end_time = time.time()
print(f"Profiling complete. Stats saved to {PROFILE_FILE}")
print(f"Time taken: {(end_time - start_time)/iterations} seconds")

# Optionally, print stats to stdout as well for quick view
s = io.StringIO()
ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
ps.print_stats(30) # Print top 30 cumulative time consumers
print(s.getvalue())
