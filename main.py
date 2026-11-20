# import sys

# from address_info import AddressInfo, NUM_SET
# from cache import Cache
# from l2_cache import L2Cache
# from read_trace import read_trace

# # Cách chạy: python main.py <mode> <trace_file>
# #   mode 0: chỉ in thống kê + kết quả của lệnh 9
# #   mode 1: như mode 0 và in thêm các message giao tiếp với L2
# DEFAULT_TRACE = "traces.txt"


# def print_cache_content(cache):
#     """In các line valid của cache: set, way, tag, dirty, LRU.
#     LRU là thứ hạng trong set: 0 = cũ nhất (victim), n-1 = mới nhất."""
#     print(f"--- {cache.name} contents ---")
#     count = 0
#     for set_index, cache_set in enumerate(cache.sets):
#         valid_lines = [(w, l) for w, l in enumerate(cache_set) if l.valid]
#         if not valid_lines:
#             continue
#         # sắp theo last_used tăng dần rồi đánh số 0,1,2,...
#         by_age = sorted(valid_lines, key=lambda wl: wl[1].last_used)
#         rank = {w: r for r, (w, _) in enumerate(by_age)}
#         for way, line in valid_lines:
#             print(
#                 f"Set {set_index:#06x} Way {way} "
#                 f"Tag {line.tag:#05x} "
#                 f"Dirty {int(line.dirty)} LRU {rank[way]}"
#             )
#             count += 1
#     if count == 0:
#         print("(no valid lines)")


# def print_statistics(cache):
#     s = cache.status
#     print(f"--- {cache.name} statistics ---")
#     print(f"Cache reads  : {s.reads}")
#     print(f"Cache writes : {s.writes}")
#     print(f"Cache hits   : {s.hits}")
#     print(f"Cache misses : {s.misses}")
#     print(f"Hit ratio    : {s.hit_ratio():.4f}")


# def main():
#     if len(sys.argv) < 2 or sys.argv[1] not in ("0", "1"):
#         print("Usage: python main.py <mode 0|1> [trace_file]")
#         sys.exit(1)

#     mode = int(sys.argv[1])
#     filename = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TRACE

#     # Một L2 dùng chung cho cả hai cache
#     l2 = L2Cache(mode)
#     icache = Cache("L1 Instruction Cache", NUM_SET, 2)
#     dcache = Cache("L1 Data Cache", NUM_SET, 4)
#     icache.l2 = l2
#     dcache.l2 = l2

#     info = AddressInfo()

#     try:
#         for event, address in read_trace(filename):
#             if event in (8, 9) and address is None:
#                 address = 0

#             if event == 0:      # đọc dữ liệu
#                 info.decode_address(address)
#                 dcache.read(info)
#             elif event == 1:    # ghi dữ liệu
#                 info.decode_address(address)
#                 dcache.write(info)
#             elif event == 2:    # lấy lệnh
#                 info.decode_address(address)
#                 icache.read(info)
#             elif event == 3:    # L2 evict: bỏ block khỏi cả hai L1
#                 info.decode_address(address)
#                 icache.invalidate_block(info)
#                 dcache.invalidate_block(info)
#             elif event == 8:    # reset toàn bộ trạng thái và thống kê
#                 icache.reset()
#                 dcache.reset()
#             elif event == 9:    # in nội dung cache
#                 print_cache_content(icache)
#                 print_cache_content(dcache)
#     except FileNotFoundError:
#         print(f"Cannot open trace file: {filename}")
#         sys.exit(1)
#     except ValueError as e:
#         print(f"Trace error: {e}")
#         sys.exit(1)

#     # Thống kê khi chạy hết trace
#     print_statistics(icache)
#     print_statistics(dcache)


# if __name__ == "__main__":
#     main()







import argparse
from cache import Cache
from l2_cache import L2Cache
from address_info import AddressInfo, NUM_SET
from read_trace import ReadTrace

def main():
    # Đọc mode và tên file traces từ terminal 
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=int)
    parser.add_argument("trace_file", type=str)
    agrs = parser.parse_args()
    mode = agrs.mode
    trace_file = agrs.trace_file

    l2Cache = L2Cache()
    iCache = Cache("I-Cache", NUM_SET, 2, l2Cache)
    dCache = Cache("D-Cache", NUM_SET, 4, l2Cache)
    info = AddressInfo()

    try:
        for event, address in ReadTrace(trace_file):
            print("helo")
    except FileNotFoundError: 
        print(f"Can not file {trace_file}")
    except ValueError as e: 
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()