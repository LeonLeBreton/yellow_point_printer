def print_matrix(dots):
    # Print the matrix of dots on standard output.
    print("           111111")
    print("  123456789012345")
    for y in range(7, -1, -1):
        line = ""
        for x in range(1, 16):
            if dots[(x,y)]:
                line += "o"
            else:
                line += " "
        print(y, line)

def column_value(col, dots):
    # Extract and decode the value of the indicated column.
    total = 0
    for y in range(6, -1, -1):
        total += dots[(col, y)] * 2**y
    return total

def main():
    dots = {}
    print("Please enter the dot pattern (0 for empty, 1 for filled):")
    
    for x in range(1, 16):
        for y in range(0, 8):
            while True:
                try:
                    value = input(f"Dot at position ({x}, {y}): ").strip()
                    if value == "":
                        raise ValueError("You must enter a value.")
                    dots[(x, y)] = int(value)
                    break
                except ValueError as e:
                    print(e)
    
    print("\nThis is the interpretation of the dot pattern:")
    print_matrix(dots)

    if not 1 in dots.values():
        print("\nThis pattern is empty and cannot be interpreted.")
        return

    print("\nIgnoring parity errors for odd rows and columns.")

    # Decode serial number
    serial_number = tuple(map(lambda col: column_value(col, dots), (13, 12, 11))) + tuple(map(lambda col: column_value(col, dots), (14, 13, 12, 11)))
    print("\nPrinter serial number:", "%02i%02i%02i [or %02i%02i%02i%02i]" % serial_number)

    # Decode date and time
    year = column_value(8, dots)
    if year < 70 or year > 99:
        year += 2000
    else:
        year += 1900

    month_names = ["(no month specified)", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    try:
        month = month_names[column_value(7, dots)]
    except IndexError:
        month = "(invalid month %i)" % column_value(8, dots)

    day = column_value(6, dots)
    if day == 0:
        day = "(no day specified)"
    elif day > 31:
        day = "(invalid day %i)" % day

    print("\nEvent date and time:")
    print("hh   :", column_value(5, dots))
    print("mm   :", column_value(2, dots))
    print("dd   :", day)
    print("MM   :", month)
    print("yyyy :", year)
    print("SSSSSSSS : Serial number", column_value(15, dots))

if __name__ == "__main__":
    main()
