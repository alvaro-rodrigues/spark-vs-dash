import timeit
import psutil
import gc
import os


import dask
import dask.dataframe as dd
from dask.distributed import Client, progress, LocalCluster

import dask_ml.cluster

exec(open("./utils/utils.py").read())

def self_join(data_size, file_type):

    gc.collect()
    with LocalCluster(processes=True, memory_limit='14GB') as cluster:
        with Client(cluster) as client:
            t_start = timeit.default_timer()

            dtype={'Aantal wielen': 'float64',
                'Europese uitvoeringcategorie toevoeging': 'object',
                'Europese voertuigcategorie toevoeging': 'object',
                'Massa ledig voertuig': 'float64',
                'Subcategorie Nederland': 'object',
                'Type gasinstallatie': 'object',
                'Rupsonderstelconfiguratiecode': 'object',
                'Datum tenaamstelling': 'float64',
                'Datum eerste toelating': 'float64',
                'Type': 'object',
                'Variant': 'object',
                'Uitvoering': 'object',
                'Code toelichting tellerstandoordeel': 'object',
                'Vervaldatum APK DT': 'object',
                'Vervaldatum tachograaf DT': 'object',
                'Zuinigheidsclassificatie': 'object',
                'Typegoedkeuringsnummer': 'object',
                'Wielbasis': 'float64'}


            if file_type == "csv":
                df = dd.read_csv(f'./data/data_{data_size}.csv', dtype=dtype)
            elif file_type == "parquet":
                df = dd.read_parquet(f'./data/parquet/data_{data_size}.parquet', engine="fastparquet")
            else:
                raise ValueError(f"File type {file_type} not supported")

            ans = df.merge(df, on='Kenteken', suffixes=['_1', '_2'])
            if file_type == "csv":
                ans.to_csv(f"./dask_output/{file_type}/self_join/{data_size}", index=False)
            elif file_type == "parquet":
                ans.to_parquet(f"./dask_output/{file_type}/self_join/{data_size}", engine="fastparquet", overwrite=True)
            else:
                raise ValueError(f"File type {file_type} not supported")

            t = timeit.default_timer() - t_start
            m = memory_usage()
            write_log('self_join', 'dask', data_size, file_type, t, m)

            del df
            del ans
            del dtype
    