class CacheLine: 
    def __init__(self, tag=0, block_address=0, last_used=0, valid=False, dirty=False, has_been_written=False):
        self.tag = tag
        self.valid = valid
        self.dirty = dirty
        self.has_been_written = has_been_written
        self.block_address = block_address
        self.last_used = last_used
    def reset(self):
        self.tag = 0
        self.valid = False
        self.dirty = False
        self.has_been_written = False
        self.block_address = 0
        self.last_used = 0