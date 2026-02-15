import glob
import os
import requests
import argparse


downloads = {
    'GWTC-1': {
        'PE': 'https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.tar.gz',
        'RP': 'https://dcc.ligo.org/public/0156/P1800324/010/public_data_release.zip',
    },
    'GWTC-2': {
        'PE': 'https://dcc.ligo.org/public/0169/P2000223/007/all_posterior_samples.tar',
        'VT': 'https://dcc.ligo.org/public/0168/P2000217/003/O3aSensitivity.tar.gz',
    },
    'GWTC-2.1': {
        'PE': '5117702',
        'VT': '5117798',
    },
    'GWTC-3': {
        'PE': '5546662',
        'RP': '5650061',
        'VT': ['5546675', '5636815'],
    },
    'GWTC-4': {
        'PE': '16053484',
        'RP': '16911563',
        'VT': ['16740117', '16740128'],
    },
}


def download(catalog, dataset, extract = False, remove = False):
    catalog = str(catalog)
    dataset = str(dataset)

    if catalog not in downloads:
        raise KeyError(f'{catalog} not a recognized catalog')

    if dataset not in downloads[catalog]:
        raise KeyError(f'{dataset} not a recognized dataset for {catalog}')

    print('Downloading', catalog, dataset)

    path = '/'.join(__file__.split('/')[:-1])
    path += '/' + catalog + '/' + dataset

    files = glob.glob(f'{path}/*')

    links = downloads[catalog][dataset]
    if type(links) not in (list, tuple):
        links = [links]

    for link in links:
        if 'https' in link:
            os.system(f'wget {link} -nc -P {path}')
        else:
            url = 'https://zenodo.org/api/records'
            record = requests.get(f'{url}/{link}').json()['conceptrecid']
            record = requests.get(f'{url}/{record}').json()['id']
            os.system(f'zenodo_get {record} -o {path}')

    files = sorted(set(glob.glob(f'{path}/*')) - set(files))

    for file in files:
        print('Downloaded', file)

    if extract:
        for file in files:
            if file[-4:] == '.zip':
                os.system(f'unzip {file} -d {path}')
            elif file[-4:] == '.tar':
                os.system(f'tar -xvf {file} -C {path}')
            elif file[-7:] == '.tar.gz':
                os.system(f'tar -xzvf {file} -C {path}')
            elif file[-3:] == '.gz':
                os.system(f'gunzip -kf {file}')
            else:
                continue

            print('Extracted', file)

            if remove:
                os.system(f'rm {file}')
                print('Removed', file)

        if catalog == 'GWTC-1' and dataset == 'PE':
            os.system(f'mv {path}/GWTC-1_sample_release/* {path}')
            os.system(f'rm -r {path}/GWTC-1_sample_release')
        elif catalog == 'GWTC-2' and dataset == 'PE':
            os.system(f'mv {path}/all_posterior_samples/* {path}')
            os.system(f'rm -r {path}/all_posterior_samples')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs = '*')
    parser.add_argument('--extract', action = 'store_true')
    parser.add_argument('--remove', action = 'store_true')
    kwargs = parser.parse_args().__dict__
    args = kwargs.pop('args')

    if args == []:
        print('About to download all PE, RP, and VT data for all catalogs.')
        y = input('Are you sure you want to proceed? [y/n]')
        if y.lower() == 'y':
            for catalog in downloads:
                for dataset in downloads[catalog]:
                    download(catalog, dataset, **kwargs)

    elif len(args) == 2:
        catalog, dataset = args if 'GWTC' in args[0] else reversed(args)
        download(catalog, dataset, **kwargs)

    elif len(args) == 1:
        if 'GWTC' in args[0]:
            catalog = args[0]
            for dataset in downloads[catalog]:
                download(catalog, dataset, **kwargs)

        else:
            dataset = args[0]
            for catalog in downloads:
                if dataset in downloads[catalog]:
                    download(catalog, dataset, **kwargs)

    else:
        raise ValueError(
            f'Expected between 0 and 2 positional arguments, but got {args}',
        )


if __name__ == '__main__':
    main()
