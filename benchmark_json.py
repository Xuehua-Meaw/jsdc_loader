import time
import datetime
import uuid
import os
from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# Attempt to import orjson, skip orjson parts if not available
try:
    import orjson
    HAS_ORJSON = True
except ImportError:
    HAS_ORJSON = False

# Need to import from the local jsdc_loader src directory
# This assumes the benchmark script is run from the repository root
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from jsdc_loader.dumper import jsdc_dumps
from jsdc_loader.loader import jsdc_loads

# --- Dataclass definitions (similar to test_performance) ---
@dataclass
class BenchmarkSimpleItem:
    id: int
    name: str
    value: float
    created_at: datetime.datetime
    item_uuid: uuid.UUID
    price: Decimal
    tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class BenchmarkPerformanceConfig:
    items: List[BenchmarkSimpleItem]
    config_name: str
    version: int
    is_active: bool
    notes: Optional[str] = None

def generate_test_data(num_items: int, num_configs: int) -> List[BenchmarkPerformanceConfig]:
    """Generates a list of BenchmarkPerformanceConfig instances."""
    all_configs = []
    for c_idx in range(num_configs):
        items_list = []
        for i in range(num_items):
            items_list.append(
                BenchmarkSimpleItem(
                    id=i,
                    name=f"Item {i}-{uuid.uuid4().hex[:4]}",
                    value=float(i) * 1.23,
                    created_at=datetime.datetime.now(datetime.timezone.utc),
                    item_uuid=uuid.uuid4(),
                    price=Decimal(str(i * 0.5)) + Decimal("0.01"),
                    tags=[f"tag{j}" for j in range(5)],
                    metadata={f"m_key_{j}": f"m_val_{j}_{uuid.uuid4().hex[:2]}" for j in range(3)},
                )
            )
        all_configs.append(
            BenchmarkPerformanceConfig(
                items=items_list,
                config_name=f"Config {c_idx}-{uuid.uuid4().hex[:6]}",
                version=c_idx + 1,
                is_active=bool(c_idx % 2),
                notes="This is a benchmark note." if i % 5 == 0 else None
            )
        )
    return all_configs

# --- Default handler for orjson (if needed, mainly for Decimal) ---
def orjson_default_handler(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    # orjson handles datetime and UUID natively.
    # If we were using a library that didn't, we'd add:
    # elif isinstance(obj, datetime.datetime):
    #     return obj.isoformat()
    # elif isinstance(obj, uuid.UUID):
    #     return str(obj)
    # elif isinstance(obj, Enum): # orjson handles Enum natively by value
    #     return obj.value
    raise TypeError(f"Type {type(obj)} not serializable for orjson custom handler")

# --- Benchmark parameters ---
NUM_CONFIGS = 10  # Number of PerformanceConfig instances
NUM_ITEMS_PER_CONFIG = 200  # Number of SimpleItem instances per PerformanceConfig
NUM_RUNS = 10  # Number of times to run each serialization/deserialization for averaging

def run_benchmark():
    print("Generating benchmark data...")
    # Generate one large list of configs, typical for many real-world scenarios
    # rather than one monolithic object.
    data_to_test = generate_test_data(NUM_ITEMS_PER_CONFIG, NUM_CONFIGS)
    print(f"Data generated: {NUM_CONFIGS} config objects, each with {NUM_ITEMS_PER_CONFIG} items.")
    print(f"Each operation will be run {NUM_RUNS} times.")

    jsdc_dump_times = []
    jsdc_load_times = []
    orjson_dump_times = []
    orjson_load_times = []

    # --- jsdc_loader (standard json) ---
    print("\nBenchmarking jsdc_loader (standard json)...")
    serialized_jsdc = ""
    for _ in range(NUM_RUNS):
        start_time = time.perf_counter()
        serialized_jsdc = jsdc_dumps(data_to_test, indent=None) # Compact JSON
        end_time = time.perf_counter()
        jsdc_dump_times.append(end_time - start_time)

    # Verify output type for jsdc_dumps
    if not isinstance(serialized_jsdc, str):
        print(f"Warning: jsdc_dumps output type is {type(serialized_jsdc)}, expected str.")

    # Ensure serialized_jsdc is not empty before loading
    if not serialized_jsdc:
        print("Error: jsdc_dumps produced empty output. Skipping jsdc_loads.")
    else:
        for _ in range(NUM_RUNS):
            start_time = time.perf_counter()
            loaded_data_jsdc = jsdc_loads(serialized_jsdc, List[BenchmarkPerformanceConfig])
            end_time = time.perf_counter()
            jsdc_load_times.append(end_time - start_time)
            if not loaded_data_jsdc or len(loaded_data_jsdc) != NUM_CONFIGS: # Basic check
                 print("Warning: jsdc_loads output seems incorrect.")


    avg_jsdc_dump = sum(jsdc_dump_times) / NUM_RUNS if jsdc_dump_times else 0
    avg_jsdc_load = sum(jsdc_load_times) / NUM_RUNS if jsdc_load_times else 0
    print(f"  jsdc_dumps average: {avg_jsdc_dump:.6f} seconds")
    if avg_jsdc_load > 0 :
        print(f"  jsdc_loads average: {avg_jsdc_load:.6f} seconds")
    else:
        print(f"  jsdc_loads: Not run due to previous error or empty output.")


    # --- orjson ---
    if HAS_ORJSON:
        print("\nBenchmarking orjson...")
        serialized_orjson_bytes = b""
        # orjson options:
        # OPT_PASSTHROUGH_DATACLASS - if we want our default handler to process dataclasses
        # For this benchmark, we want orjson's native dataclass speed.
        # The default handler is mainly for Decimal.
        orjson_options = None
        # If orjson's native dataclass serialization doesn't use our JSDCJSONEncoder logic
        # (e.g. for Enum name vs value, or custom Decimal format if it differed),
        # we might need OPT_PASSTHROUGH_DATACLASS and a more complex default.
        # For now, assuming native dataclass is fine and default handles Decimal.

        for _ in range(NUM_RUNS):
            start_time = time.perf_counter()
            # orjson serializes dataclasses natively.
            # We only need the default handler for types orjson doesn't know (like Decimal).
            serialized_orjson_bytes = orjson.dumps(data_to_test, default=orjson_default_handler, option=orjson_options)
            end_time = time.perf_counter()
            orjson_dump_times.append(end_time - start_time)

        # Verify output type for orjson.dumps
        if not isinstance(serialized_orjson_bytes, bytes):
            print(f"Warning: orjson.dumps output type is {type(serialized_orjson_bytes)}, expected bytes.")

        # For fair comparison with jsdc_loads (which expects str), we might decode.
        # However, orjson.loads can take bytes directly.
        # If we were to use orjson to replace standard json in jsdc_dumps,
        # jsdc_dumps would either return bytes, or do this decode step.
        # For now, we pass bytes to orjson.loads.

        # Ensure serialized_orjson_bytes is not empty before loading
        if not serialized_orjson_bytes:
            print("Error: orjson.dumps produced empty output. Skipping orjson.loads.")
        else:
            for _ in range(NUM_RUNS):
                start_time = time.perf_counter()
                # orjson.loads does not use the `default` hook. It doesn't convert to custom types like Decimal.
                # It will load Decimals as strings if our default handler turned them to strings.
                # This is a limitation if direct type recovery is needed without a full deserializer like jsdc_loads.
                # For this benchmark, we are comparing raw JSON processing speed.
                # The output of orjson.loads will be standard Python dicts/lists/str etc.
                loaded_data_orjson = orjson.loads(serialized_orjson_bytes)
                end_time = time.perf_counter()
                orjson_load_times.append(end_time - start_time)
                # A full comparison would require converting this raw dict data back to dataclasses.
                # jsdc_loads does this full conversion. This benchmark for orjson.loads is more about raw parsing.
                if not loaded_data_orjson or len(loaded_data_orjson) != NUM_CONFIGS: # Basic check
                    print("Warning: orjson.loads output seems incorrect.")

        avg_orjson_dump = sum(orjson_dump_times) / NUM_RUNS if orjson_dump_times else 0
        avg_orjson_load = sum(orjson_load_times) / NUM_RUNS if orjson_load_times else 0
        print(f"  orjson.dumps average: {avg_orjson_dump:.6f} seconds")
        if avg_orjson_load > 0:
            print(f"  orjson.loads average (raw parse): {avg_orjson_load:.6f} seconds")
        else:
            print(f"  orjson.loads: Not run due to previous error or empty output.")

        if avg_jsdc_dump > 0 and avg_orjson_dump > 0:
            print(f"\n  Comparison (dumps): orjson is approx. {avg_jsdc_dump/avg_orjson_dump:.2f}x faster")
        if avg_jsdc_load > 0 and avg_orjson_load > 0:
            # Note: This loads comparison is jsdc_loads (full dataclass conversion) vs orjson.loads (raw dict/list parsing)
            # A fairer 'loads' comparison would be jsdc_loads vs (orjson.loads + manual conversion to dataclasses)
            # or using orjson within jsdc_loads's parsing step.
            print(f"  Comparison (loads): jsdc_loads vs orjson.loads (raw): jsdc_loads is {avg_jsdc_load:.6f}s, orjson.loads is {avg_orjson_load:.6f}s")
            print(f"    Note: orjson.loads here is raw parsing, jsdc_loads includes full object conversion.")
    else:
        print("\nSkipping orjson benchmarks (orjson not installed).")

if __name__ == "__main__":
    # Install orjson if you want to test it: pip install orjson
    run_benchmark()
