# vì đề không cho cấu hình của L2 nên giả lập L2 không có set, way, address gì cả


class L2Cache:

    def __init__(self, mode=0):

        self.mode = mode

    def read(self, address):

        if self.mode == 1:
            print(f"Read from L2 {hex(address)}")

    def read_for_ownership(self, address):

        if self.mode == 1:
            print(
                f"Read for Ownership from L2 {hex(address)}"
            )

    def write_back(self, address):

        if self.mode == 1:
            print(f"Write to L2 {hex(address)}")

    def write_through(self):

        # Update L2 on the first write.
        # No additional output format is specified
        # for this operation in the project brief.
       
        pass
