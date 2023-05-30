import sys

if len(sys.argv) < 2:
    sys.exit(1)

spk_path = sys.argv[1]

# This seems to be in every SPK file right before the sequence names
start_sequence = bytearray([0x10, 0x03, 0x00, 0x16, 0x00, 0x00, 0x00, 0x01])

with open(spk_path, 'rb') as spk_file:
    spk_data = spk_file.read()
    start_index = spk_data.find(start_sequence)
    if start_index == -1:
        sys.exit(1)

    animation_data = spk_data[start_index + len(start_sequence):]

    # Skip the null bytes between the start and the first sequence
    non_null_index = next((i for i, byte in enumerate(
        animation_data) if byte != 0x00), None)

    if non_null_index is None:
        sys.exit(1)

    animation_data = animation_data[non_null_index:]
    animation_names = animation_data.split(b'\x00')

    for name in animation_names:
        try:
            decoded_name = name.decode('utf-8', errors='ignore')
            print(decoded_name)
        except UnicodeDecodeError:
            print("Unable to decode animation name.")

        # Base seems to always be the last sequence, I would assume this is the reference pose
        if decoded_name == "Base":
            break
