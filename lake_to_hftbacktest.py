from typing import List, Optional, Literal
import time

import pandas as pd
import numpy as np
from numpy.typing import NDArray
from numba_progress import ProgressBar
from numba import njit

from hftbacktest.data import merge_on_local_timestamp, correct, validate_data
from hftbacktest import DEPTH_CLEAR_EVENT, DEPTH_SNAPSHOT_EVENT, TRADE_EVENT, DEPTH_EVENT

@njit(cache=True)
def convert_trade(vals, buffer_size, progress_hook):
    tmp = np.empty((buffer_size, 6), np.float64)
    row_num = 0
    for idx in range(len(vals)):
        progress_hook.update()
        cols = vals[idx]
        # Insert TRADE_EVENT
        tmp[row_num] = [
            TRADE_EVENT,
            cols[4],
            cols[5],
            1 if cols[0] == 'buy' else -1,
            cols[2],
            cols[1],
        ]
        row_num += 1
    return tmp[:row_num]

@njit(cache=True)
def convert_books(vals, buffer_size, progress_hook):
    tmp = np.empty((buffer_size, 6), np.float64)
    row_num = 0
    ss_bid = None
    ss_ask = None
    rns = [0, 0]
    for idx in range(len(vals)):
        progress_hook.update()
        cols = vals[idx]
        ss_bid = np.empty((50, 6), np.float64)
        ss_ask = np.empty((50, 6), np.float64)
        rns = [0, 0]
        for side_idx, side, side_sign in ((0, ss_bid, 1), (1, ss_ask, -1)):
            for level in range(0, 20):
                price = cols.iloc[3 + level * 2 + side_idx * 40]
                qty = cols.iloc[4 + level * 2 + side_idx * 40]
                side[rns[side_idx]] = [
                    DEPTH_SNAPSHOT_EVENT,
                    cols[0],
                    cols[1],
                    side_sign,
                    price,
                    qty,
                ]
                rns[side_idx] += 1

        ss_bid = ss_bid[:rns[0]]
        # Clear the bid market depth within the snapshot bid range.
        tmp[row_num] = [
            DEPTH_CLEAR_EVENT,
            ss_bid[0, 1],
            ss_bid[0, 2],
            1,
            ss_bid[-1, 4],
            0
        ]
        row_num += 1

        tmp[row_num:row_num + len(ss_bid)] = ss_bid[:]
        row_num += len(ss_bid)
        ss_bid = None

        ss_ask = ss_ask[:rns[1]]

        tmp[row_num] = [
            DEPTH_CLEAR_EVENT,
            ss_ask[0, 1],
            ss_ask[0, 2],
            -1,
            ss_ask[-1, 4],
            0
        ]
        row_num += 1

        tmp[row_num:row_num + len(ss_ask)] = ss_ask[:]
        row_num += len(ss_ask)
        ss_ask = None

    return tmp[:row_num]

@njit(cache=True)
def convert_book_diffs(vals, buffer_size, ss_buffer_size, progress_hook):
    tmp = np.empty((buffer_size, 6), np.float64)
    row_num = 0
    is_snapshot = False
    ss_bid: np.ndarray = None
    ss_ask: np.ndarray = None
    rns = [0, 0]
    for idx in range(len(vals)):
        progress_hook.update()
        cols = vals[idx]
        if cols[0] == 0:
            # Prepare to insert DEPTH_SNAPSHOT_EVENT
            if not is_snapshot:
                is_snapshot = True
                ss_bid = np.empty((ss_buffer_size, 6), np.float64)
                ss_ask = np.empty((ss_buffer_size, 6), np.float64)
                rns = [0, 0]
            if cols[3] == 1: # side is bid
                ss_bid[rns[0]] = [
                    DEPTH_SNAPSHOT_EVENT,
                    cols[0],
                    cols[1],
                    1,
                    cols[4],
                    cols[5],
                ]
                rns[0] += 1
            else:
                ss_ask[rns[1]] = [
                    DEPTH_SNAPSHOT_EVENT,
                    cols[0],
                    cols[1],
                    -1,
                    cols[4],
                    cols[5],
                ]
                rns[1] += 1
        else:
            if is_snapshot:
                # End of the snapshot.
                is_snapshot = False

                # Add DEPTH_CLEAR_EVENT before refreshing the market depth by the snapshot.
                ss_bid = ss_bid[:rns[0]]
                if len(ss_bid) > 0:
                    # Clear the bid market depth within the snapshot bid range.
                    tmp[row_num] = [
                        DEPTH_CLEAR_EVENT,
                        ss_bid[0, 1],
                        ss_bid[0, 2],
                        1,
                        ss_bid[-1, 4],
                        0
                    ]
                    row_num += 1
                    # Add DEPTH_SNAPSHOT_EVENT for the bid snapshot
                    tmp[row_num:row_num + len(ss_bid)] = ss_bid[:]
                    row_num += len(ss_bid)
                ss_bid = None

                ss_ask = ss_ask[:rns[1]]
                if len(ss_ask) > 0:
                    # Clear the ask market depth within the snapshot ask range.
                    tmp[row_num] = [
                        DEPTH_CLEAR_EVENT,
                        ss_ask[0, 1],
                        ss_ask[0, 2],
                        -1,
                        ss_ask[-1, 4],
                        0
                    ]
                    row_num += 1
                    # Add DEPTH_SNAPSHOT_EVENT for the ask snapshot
                    tmp[row_num:row_num + len(ss_ask)] = ss_ask[:]
                    row_num += len(ss_ask)
                ss_ask = None
            # Insert DEPTH_EVENT
            tmp[row_num] = [
                DEPTH_EVENT,
                cols[0],
                cols[1],
                1 if cols[3] == 1 else -1,
                cols[4],
                cols[5],
            ]
            row_num += 1
    return tmp[:row_num]

def convert(
        input_dfs: List[pd.DataFrame],
        output_filename: Optional[str] = None,
        buffer_size: int = 100_000_000,
        ss_buffer_size: int = 5_000,
        base_latency: float = 0,
        method: Literal['separate', 'adjust', 'keep'] = 'adjust',
) -> NDArray:
    r"""
    Converts Crypto Lake data files into a format compatible with HftBacktest.

    Args:
        input_dfs: Input dataframes from lake
        output_filename: If provided, the converted data will be saved to the specified filename in ``npz`` format.
        buffer_size: Sets a preallocated row size for the buffer.
        base_latency: The value to be added to the feed latency.
                      See :func:`.correct_local_timestamp`.
        method: The method to correct reversed exchange timestamp events. See :func:`..validation.correct`.

    Returns:
        Converted data compatible with HftBacktest.
    """
    sets = []
    for df in input_dfs:
        df['origin_time'] = df['origin_time'].astype(int)
        df['received_time'] = df['received_time'].astype(int)
        with ProgressBar(total=len(df)) as numba_progress:
            if 'trade_id' in df.columns:
                if df['side'].dtype != int:
                    df['side'] = df['side'].map({'buy': 1, 'sell': -1}).astype(int)
                sets.append(convert_trade(df.values, buffer_size, numba_progress))
            elif 'bid_3_price' in df.columns:
                sets.append(convert_books(df.values, buffer_size, numba_progress))
            elif 'side_is_bid' in df.columns:
                df['side_is_bid'] = df['side_is_bid'].astype('int8')
                sets.append(convert_book_diffs(df.values, buffer_size, ss_buffer_size, numba_progress))

    print('Merging', time.time())
    data = sets[0]
    del sets[0]
    while len(sets) > 0:
        data = merge_on_local_timestamp(data, sets[0])
        del sets[0]

    print('Correcting', time.time())
    data = correct(data, base_latency=base_latency, method=method)

    # print('Val2', time.time())
    # # Validate again.
    # num_corr = validate_data(data)
    # if num_corr > 0:
    #     raise ValueError

    print(time.time())
    if output_filename is not None:
        print('Saving to %s' % output_filename)
        np.savez(output_filename, data=data)
    print(time.time())

    return data
