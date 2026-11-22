# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Vaibhav Agarwal

from openchart import NSEData

nse = NSEData()

# Search indices
indices = nse.search('NIFTY', 'IDX')
print(indices)
