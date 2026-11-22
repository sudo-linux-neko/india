# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Vaibhav Agarwal

import os
import time
import pandas as pd
from datetime import datetime, timedelta
from openchart import NSEData

# 1. Target Configuration
SYMBOL = "NIFTY 50"
SEGMENT = "IDX"  # Use 'IDX' for Indices, 'EQ' for Equities, 'FO' for Futures/Options
INTERVAL = "1m"   # 1-minute data bars

# Define total backtest range (10 years ago to today)
end_date = datetime.now()
final_start_date = end_date - timedelta(days=365 * 10)

# Initialize the client (This establishes the baseline session/cookies)
nse = NSEData()
all_chunks = []

current_end = end_date
chunk_days = 30  # Documentation standard safe window for 1-minute intervals

print(f"🚀 Starting 10-Year 1-Minute extraction for {SYMBOL}...")

# 2. Iterative Chunking Loop
while current_end > final_start_date:
    current_start = max(current_end - timedelta(days=chunk_days), final_start_date)
    
    print(f"📥 Fetching: {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}...")
    
    try:
        # Using the standard library approach that handles underlying headers and sessions
        df = nse.historical(
            symbol=SYMBOL,
            segment=SEGMENT,
            start=current_start,
            end=current_end,
            interval=INTERVAL
        )
        
        if df is not None and not df.empty:
            all_chunks.append(df)
            print(f"   ✅ Success: Retrieved {len(df)} rows.")
        else:
            print("   ⚠️ Empty block returned (Rate limited or window threshold exceeded).")
            
    except Exception as e:
        print(f"   ❌ Error occurred: {e}")
        
    # Crucial delay to avoid getting your IP banned by NSE's security system
    time.sleep(3) 
    
    # Move the window backward
    current_end = current_start

# 3. Compile and Export Results
if all_chunks:
    print("\n🔄 Compiling and deduplicating chunks...")
    final_df = pd.concat(all_chunks)
    
    # Sort chronologically and drop edge overlap rows
    final_df = final_df.sort_index().drop_duplicates()
    
    # Save directly to your active ~/india workspace
    filename = f"{SYMBOL.lower().replace(' ', '_')}_1min_10year.csv"
    final_df.to_csv(filename)
    print(f"🎉 Success! Total data collected: {len(final_df)} bars.")
    print(f"📁 File location: {os.path.abspath(filename)}")
else:
    print("\n❌ Severe Block: NSE servers rejected the header footprint.")
    print("💡 Back-up Plan: Run 'pip install requests' and let me know if it still fails.")
