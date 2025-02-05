#!/usr/bin/env python3
#
# fix_io_cor_gds.py ---
#
# Special-purpose script that does the work of what ought to be a simple
# binary diff and patch.  Except that no such thing exists as a standard
# offering on most Linux systems, so instead of adding another OS
# package requirement, I'm just writing a binary search-and-replace in
# python.
#
# The purpose of the patch is to add the isolated substrate layer
# (GDS layer 23:5) to the ESD_CLAMP_COR cell, which is the only way to
# get the cell to be LVS-correct at that level of hierarchy.  The layer
# is simply copied down from further up in the hierarchy.  There is no
# mask change to the corner cell itself, but the change allows the corner
# cell to be read back from GDS, extract, and pass LVS.

import sys

if len(sys.argv) != 2:
    print('Usage:  fix_io_cor_gds.py <filename>')
    sys.exit(1)
else:
    file_name = sys.argv[1]

# orig_data is the STRNAME record for ESD_CLAMP_COR.  Insert the isosub layer
# data after this record.
orig_data = b'\x00\x12\x06\x06\x45\x53\x44\x5f\x43\x4c\x41\x4d\x50\x5f\x43\x4f\x52\x00'

append_data = b'\x00\x04\x08\x00\x00\x06\x0d\x02\x00\x17\x00\x06\x0e\x02\x00\x05\x00\x3c\x10\x03\xff\xff\xff\x2e\x00\x03\x48\x2d\xff\xff\xff\x2e\x00\x04\x5b\xd2\x00\x04\x47\xf5\x00\x04\x5b\xd2\x00\x04\x47\xf5\x00\x04\x42\x14\x00\x04\x5a\x65\x00\x04\x42\x14\x00\x04\x5a\x65\x00\x03\x48\x2d\xff\xff\xff\x2e\x00\x03\x48\x2d\x00\x04\x11\x00'

# This is not efficient, but only needs to be done once.

with open(file_name, 'rb') as ifile:
    data = ifile.read()
    data = data.replace(orig_data, orig_data + append_data)

# Write back into the same file
with open(file_name, 'wb') as ofile:
    ofile.write(data)

print("Done!")
