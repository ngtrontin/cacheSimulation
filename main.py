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

    l2Cache = L2Cache(mode)
    iCache = Cache("I-Cache", NUM_SET, 2, l2Cache)
    dCache = Cache("D-Cache", NUM_SET, 4, l2Cache)
    info = AddressInfo()
    try:
        for event, address in ReadTrace(trace_file):
            if event == 0:      # đọc dữ liệu
                info.decode_address(address)
                dCache.read(info)
            elif event == 1:    # ghi dữ liệu
                info.decode_address(address)
                dCache.write(info)
            elif event == 2:    # lấy lệnh
                info.decode_address(address)
                iCache.read(info)
            elif event == 3:    # L2 evict: bỏ block khỏi cả hai L1
                info.decode_address(address)
                iCache.invalidate_block(info)
                dCache.invalidate_block(info)
            elif event == 8:    # reset toàn bộ trạng thái và thống kê
                iCache.reset()
                dCache.reset()
            elif event == 9:    # in nội dung cache
                iCache.print_cache_content()
                dCache.print_cache_content()
    except FileNotFoundError: 
        print(f"Can not file {trace_file}")
    except ValueError as e: 
        print(f"ERROR: {e}")

    iCache.print_statistics()
    dCache.print_statistics()

if __name__ == "__main__":
    main()