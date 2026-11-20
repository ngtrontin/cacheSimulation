# Mỗi cache có 16kB sets = 16*1024 = 16384 bits, mỗi sets có 2 or 4 ways (EX: 2ways chứa 2 cache line) 
# 1 cache line có size là 64B 
# I-Cache = 16384 * 2 = 32768 lines
# D-Cache = 16384 * 4 = 65536 lines
# Every L1 cache has form: LRU / D / V / TAG / SET / BYTE (offset-xác định byte bên trong cache line)
#                                     12 bits / 14 bits / 6 bits

# DEFINITION: WRITE-BACK, WRITE-THROUGH, WRITE-ALLOCATE
# I-CACHE, D-CACHE, INCLUSIVE CACHE ( dữ liệu được lưu trong L1 chắc chắn sẽ được lưu trong L2 )
from cache_line import CacheLine 
from cache_status import CacheStatus
from l2_cache import L2Cache

class Cache:
    def __init__(self, name, num_set, num_way, L2Cache,line_size = 64):
        self.name = name
        self.num_set = num_set
        self.num_way = num_way
        self.line_size = line_size
        self.sets = [
            #list comprehensive : sẽ tạo ra set có dạng 
            [CacheLine() for way in range(num_way)] for set in range(num_set)
        ]

        # dùng cho LRU
        self.access_counter = 0

        self.l2 = L2Cache

        self.status = CacheStatus()


    def lookup(self, address_info):

        if not (0 <= address_info.set_index < self.num_set): 
            raise ValueError("Invalid set index")

        # find set by using address_info
        cache_set = self.sets[address_info.set_index]

        # enumerate trả về index và giá trị của từng phần tử
        for way_index, line in enumerate(cache_set):
            if line.valid and (line.tag == address_info.tag_index):
                return way_index, line

        return None, None

    # LRU
    def update_lru(self, cache_line):
        self.access_counter += 1
        cache_line.last_used = self.access_counter

    def select_victim(self, set_index):
        cache_set = self.sets[set_index]
        for way_index, line in enumerate(cache_set):
            if not line.valid:
                return way_index
        victim_way = 0
        for way_index, line in enumerate(cache_set):
            if(line.last_used < cache_set[victim_way].last_used):
                victim_way = way_index

        return victim_way
        
    def read(self, address_info):
        self.status.reads += 1
        way, line = self.lookup(address_info)

        # nếu không phải none thì hit 
        if line is not None:
            self.status.hits += 1
            #update last_used cho line đó
            self.update_lru(line)
            return True
        else:
        # cache miss
            self.status.misses += 1
            victim_way = self.select_victim(address_info.set_index)
            victim_line = self.sets[address_info.set_index][victim_way]
            if(victim_line.valid and victim_line.dirty):
                self.l2.write_back(victim_line.block_address)
            self.l2.read(address_info.block_address)
            #update line mới mà Cpu cần đọc từ L2 vào cache
            victim_line.tag = address_info.tag_index
            victim_line.valid = True
            victim_line.dirty = False
            victim_line.has_been_written = False
            victim_line.block_address = address_info.block_address
            self.update_lru(victim_line)

            return False
    
    # Write Allocate: Khi ghi vào địa chỉ chưa có trong Cache, đưa Cache Line tương ứng vào Cache trước rồi mới thực hiện ghi.
    # Write-Through: Ghi thay đổi xuống L2 ngay lập tức.
    # Write-Back: Giữ thay đổi trong L1; đánh dấu Dirty. Khi Line bị thay thế thì mới ghi dữ liệu xuống L2.
    
    def write(self, address_info):
        self.status.writes += 1
        way_index, line = self.lookup(address_info)
        if (line is not None):
            # write hit
            self.status.hits += 1
        else:
            # write miss
            self.status.misses += 1
            way_index = self.select_victim(address_info.set_index)
            line = self.sets[address_info.set_index][way_index]

            if(line.valid and line.dirty):
                # ghi địa chỉ của line cũ trong L1 cần bị thay thế
                self.l2.write_back(line.block_address)
 
            self.l2.read_for_ownership(address_info.block_address)

            line.tag = address_info.tag_index
            line.valid = True
            line.has_been_written = False
            line.dirty = False
            line.block_address = address_info.block_address


        if not (line.has_been_written):
            # Write through
            self.l2.write_through()
            line.has_been_written = True
            line.dirty = False
        else:
            # write back
            line.dirty = True

        self.update_lru(line)
        return way_index

    def invalidate_block(self, address_info):
        cache_set = self.sets[address_info.set_index]
        for way, line in enumerate(cache_set):
            if line.valid and line.tag == address_info.tag_index:
                line.valid = False
                line.dirty = False
                line.last_used = 0
                line.has_been_written = 0
                line.block_address = 0

    # event 9
    def print_cache_content(self):
    #    """In các line valid của cache: set, way, tag, dirty, LRU.
    #   LRU là thứ hạng trong set: 0 = cũ nhất (victim), n-1 = mới nhất."""
        print(f"--- {self.name} contents ---")
        count = 0
        for set_index, cache_set in enumerate(self.sets):
            valid_lines = [(w, l) for w, l in enumerate(cache_set) if l.valid]
            if not valid_lines:
                continue
            # sắp theo last_used tăng dần rồi đánh số 0,1,2,...
            by_age = sorted(valid_lines, key=lambda wl: wl[1].last_used)
            rank = {w: r for r, (w, _) in enumerate(by_age)}
            for way, line in valid_lines:
                print(
                    f"Set {set_index:#06x} Way {way} "
                    f"Tag {line.tag:#05x} "
                    f"Dirty {int(line.dirty)} LRU {rank[way]}"
                )
                count += 1
        if count == 0:
            print("(no valid lines)")

    def print_statistics(self):
        s = self.status
        print(f"--- {self.name} statistics ---")
        print(f"Cache reads  : {s.reads}")
        print(f"Cache writes : {s.writes}")
        print(f"Cache hits   : {s.hits}")
        print(f"Cache misses : {s.misses}")
        print(f"Hit ratio    : {s.hit_ratio():.4f}")

    def reset(self):
        # cache_set là 1 set có dạng [way0][way1] -> for thứ 2 là truy cập vào line được chứa trong mỗi way
        for cache_set in self.sets:
            for cache_line in cache_set:
                cache_line.reset()

        self.access_counter = 0
        self.status.reset()
