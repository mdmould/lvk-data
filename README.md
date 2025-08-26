# lvk-data

This is a repo I use to download and store public data released by the LIGO-Virgo-KAGRA (LVK) collaboration. In particular, from the [GWTC releases](https://gwosc.org/eventapi/html/GWTC/) I usually only need parameter-estimation (PE) samples, search injections to estimate sensitive volume-time (VT), and rates and population (RP) analysis results. The data for these can be found on [GWOSC](https://gwosc.org) via [Zenodo](https://zenodo.org/communities/ligo-virgo-kagra/records).

## Installation

Clone the repo.

```
git clone git@github.com:mdmould/lvk-data.git
```

This contains a predefined structure for data directories and a single Python script to download data. Each catalog `GWTC-*` has a folder, within which `PE`, `RP`, and `VT` each have a folder.

## Usage

Simply execute the Python download script.

```
python download.py (*args) (--extract) (--remove)
```

Between 0 and 2 (inclusive) positional arguments are accepted.

- If none are given, the script will download all available `PE`, `RP`, and `VT` data for all `GWTC` releases. E.g., `python download.py`.

- If one is given, it will download all data matching that argument. E.g.: `python download.py GWTC-1` will download all `PE`, `RP`, and `VT` data for `GWTC-1`; `python download.py PE` will download `PE` for all `GWTC` releases.

- If two are given, they correspond to a single catalog and a single dataset type. E.g., `python download.py GWTC-3 VT` will download the `VT` files from the `GWTC-3` data release.

Flags:
- `--extract`: Extract archive files that are downloaded.
- `--remove`: Delete archive files after extracting.
