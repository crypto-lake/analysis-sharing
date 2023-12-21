import gzip
from typing import List, Optional, Literal

import pandas as pd
import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm
import numba


from hftbacktest.data import merge_on_local_timestamp, correct, validate_data
from hftbacktest import DEPTH_CLEAR_EVENT, DEPTH_SNAPSHOT_EVENT, TRADE_EVENT, DEPTH_EVENT

# @numba.jit(nopython=False, cache=True)
def convert(
        input_dfs: List[pd.DataFrame],
        output_filename: Optional[str] = None,
        buffer_size: int = 100_000_000,
        ss_buffer_size: int = 5_000,
        base_latency: float = 0,
        method: Literal['separate', 'adjust'] = 'separate',
        # snapshot_mode: Literal['process', 'ignore_sod', 'ignore'] = 'process'
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
    TRADE = 0
    DEPTH = 1
    DEPTH_DELTAS = 2

    sets = []
    for df in input_dfs:
        file_type = None
        tmp = np.empty((buffer_size, 6), np.float64)
        row_num = 0
        is_snapshot = False
        ss_bid = None
        ss_ask = None
        rns = [0, 0]
        # is_sod_snapshot = True
        # print('Reading %s' % file)
        for idx, cols in tqdm(df.iterrows(), total=len(df)):
            if file_type is None:
                if 'trade_id' in cols:
                    file_type = TRADE
                elif 'bid_3_price' in cols:
                    file_type = DEPTH
                elif 'side_is_bid' in cols:
                    file_type = DEPTH_DELTAS
            elif file_type == TRADE:
                # Insert TRADE_EVENT
                tmp[row_num] = [
                    TRADE_EVENT,
                    cols['origin_time'].value,
                    cols['received_time'].value,
                    1 if cols['side'] == 'buy' else -1,
                    cols['price'],
                    cols['quantity']
                ]
                row_num += 1
            elif file_type == DEPTH:
                if True: # everything is snapshot
                # if cols[4] == 'true':
                    # if (snapshot_mode == 'ignore') or (snapshot_mode == 'ignore_sod' and is_sod_snapshot):
                    #     continue
                    # Prepare to insert DEPTH_SNAPSHOT_EVENT
                    if True: #not is_snapshot:
                        # is_snapshot = True
                        ss_bid = np.empty((50, 6), np.float64)
                        ss_ask = np.empty((50, 6), np.float64)
                        rns = [0, 0]
                    for side_idx, side, side_sign in ((0, ss_bid, 1), (1, ss_ask, -1)):
                        for level in range(0, 20):
                            price = cols.iloc[3 + level * 2 + side_idx * 40]
                            qty = cols.iloc[4 + level * 2 + side_idx * 40]
                            side[rns[side_idx]] = [
                                DEPTH_SNAPSHOT_EVENT,
                                cols['origin_time'].value,
                                cols['received_time'].value,
                                side_sign,
                                price,
                                qty,
                            ]
                            rns[side_idx] += 1
                if True:
                    # is_sod_snapshot = False
                    if True: #is_snapshot:
                        # End of the snapshot.
                        # is_snapshot = False

                        # Add DEPTH_CLEAR_EVENT before refreshing the market depth by the snapshot.

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
                        # Add DEPTH_SNAPSHOT_EVENT for the bid snapshot
                        tmp[row_num:row_num + len(ss_bid)] = ss_bid[:]
                        row_num += len(ss_bid)
                        ss_bid = None

                        ss_ask = ss_ask[:rns[1]]
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
                    # # Insert DEPTH_EVENT
                    # tmp[row_num] = [
                    #     DEPTH_EVENT,
                    #     int(cols[2]),
                    #     int(cols[3]),
                    #     1 if cols[5] == 'bid' else -1,
                    #     float(cols[6]),
                    #     float(cols[7])
                    # ]
                    # row_num += 1
            elif file_type == DEPTH_DELTAS:
                    if cols['origin_time'].value == 0:
                        # if (snapshot_mode == 'ignore') or (snapshot_mode == 'ignore_sod' and is_sod_snapshot):
                        #     continue
                        # Prepare to insert DEPTH_SNAPSHOT_EVENT
                        if not is_snapshot:
                            is_snapshot = True
                            ss_bid = np.empty((ss_buffer_size, 6), np.float64)
                            ss_ask = np.empty((ss_buffer_size, 6), np.float64)
                            rns = [0, 0]
                        if cols['side_is_bid'] == True:
                            ss_bid[rns[0]] = [
                                DEPTH_SNAPSHOT_EVENT,
                                cols['origin_time'].value,
                                cols['received_time'].value,
                                1,
                                cols['price'],
                                cols['size'],
                            ]
                            rns[0] += 1
                        else:
                            ss_ask[rns[1]] = [
                                DEPTH_SNAPSHOT_EVENT,
                                cols['origin_time'].value,
                                cols['received_time'].value,
                                -1,
                                cols['price'],
                                cols['size'],
                            ]
                            rns[1] += 1
                    else:
                        # is_sod_snapshot = False
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
                            cols['origin_time'].value,
                            cols['received_time'].value,
                            1 if cols['side_is_bid'] else -1,
                            cols['price'],
                            cols['size'],
                        ]
                        row_num += 1
        sets.append(tmp[:row_num])

    print('Merging')
    data = sets[0]
    del sets[0]
    while len(sets) > 0:
        data = merge_on_local_timestamp(data, sets[0])
        del sets[0]

    data = correct(data, base_latency=base_latency, method=method)

    # Validate again.
    num_corr = validate_data(data)
    if num_corr < 0:
        raise ValueError

    if output_filename is not None:
        print('Saving to %s' % output_filename)
        np.savez(output_filename, data=data)

    return data
