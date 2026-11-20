def ReadTrace(filename):
    with open(filename, "r") as file:
        for line_num, line in enumerate(file,start=1):
            line = line.strip()
            if not line: 
                continue
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Invalid trace at line {line_num}")
            events = int(parts[0])
            address = int(parts[1],16)

            if(events not in [0,1,2,3,8,9]):
                raise ValueError(f"Unknown event {events}")

            yield events, address
    