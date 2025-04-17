import timeit
from parking import tambah_kendaraan, keluar_parkir, list_kendaraan
from report import laporan_pendapatan

def performance_test():
    # Test setup
    test_cases = {
        "Tambah Kendaraan": lambda: tambah_kendaraan(),
        "List Kendaraan": lambda: list_kendaraan(),
        "Keluar Parkir": lambda: keluar_parkir(),
        "Laporan Pendapatan": lambda: laporan_pendapatan()
    }
    
    number_of_runs = 2
    results = {}
    
    print("Running performance tests...")
    print("-" * 50)
    
    for test_name, test_func in test_cases.items():
        try:
            # Measure execution time
            total_time = timeit.timeit(test_func, number=number_of_runs)
            avg_time = total_time / number_of_runs
            results[test_name] = avg_time
            
            print(f"{test_name}:")
            print(f"  Average execution time: {avg_time:.4f} seconds")
            print(f"  Total time for {number_of_runs} runs: {total_time:.4f} seconds")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error testing {test_name}: {str(e)}")
    
    # Summary
    print("\nPerformance Test Summary:")
    print("-" * 50)
    for operation, time in sorted(results.items(), key=lambda x: x[1]):
        print(f"{operation}: {time:.4f} seconds per operation")

if __name__ == "__main__":
    performance_test()