NUM_SET = 16 * 1024 #Bytes
LINE_SIZE = 64      #Bytes

# class này dùng để chuyển tag, set, byte sang số bit cần thiết để biểu diễn nó
class AddressInfo:
    def __init__(self):
        self.tag_index = None
        self.set_index = None
        self.byte_index = None
        self.block_address = None

        self.set_bits = None
        self.byte_bits = None
    
    def decode_address(self, address, num_set = NUM_SET, line_size = LINE_SIZE):
        # # Cách 1 để tính tag, set, byte, block address
        block_bits = 32
        byte_bits = 6
        set_bits = 14
        tag_bits = block_bits - byte_bits - set_bits
        self.byte_index = block_bits & 63
        self.set_index = (block_bits >> 6) & 16383
        self.tag_index = 32 >> 14
0x00006
        # Cách 2 để tính tag, set, byte, block address
        # self.set_bits = (num_set-1).bit_length()
        # self.byte_bits = (line_size-1).bit_length()

        # # Trả về tag, set, byte được tính theo địa chỉ CPU đưa vào 
        # # vì trong 32bit của address có 12 bits tag, 14 bits set, 6 bit byte 

        # # có 6 bits để biểu diễn 64B (từ 0 -> 63) nên giá trị nhị phân của 63 là số lớn nhất của 6 bits là 111111
        # # khi AND (&) với 32 bits address thì sẽ lấy được 6 bits cuối của address 
        # # ví dụ 6 bits cúi address 101010 & 111111 = 101010 
        # self.byte_index = address & (line_size-1) 

        # # dịch address qua byte bits và tiếp tục lấy số lượng bit cho set_index
        # self.set_index = (address >> self.byte_bits) & (num_set-1)

        # # dịch qua byte bits và set bits -> còn lại là tag bits
        # self.tag_index = address >> (self.byte_bits+self.set_bits)

        # # tìm địa chỉ đầu tiên của block bằng cách lấy địa chỉ trừ cho offset(byte_index)
        # # Ví dụ 1 block có 64B -> address = 1 là CPU muốn truy cập vào ô nhớ có địa chỉ số 1 
        # # nên block address = 0 
        # # ~(line_size-1) để đưa 6 bits của line_size thành 0 để xóa 6 bits đó đi
        # self.block_address = address & ~(line_size-1)
