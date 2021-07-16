# Downloads all burn data for specified window and/or year
# Make this run from command line where you can run for window/year combo

import pysftp
import re
import os


# connect to the umd fire server
def connect_to_umd_fire_server():
    sftp = pysftp.Connection(
        'fuoco.geog.umd.edu',
        username='fire',
        password='burnt',
        cnopts=cnopts
    )

    return sftp


# get a list of all the windows
def get_window_list():
    with sftp.cd('data/MODIS/C6/MCD64A1/TIFF'):
        return sftp.listdir()


# get a list of years for the given window
def get_year_list(window):
    with sftp.cd(f'data/MODIS/C6/MCD64A1/TIFF/{window}'):
        return sftp.listdir()


# make a set of folders to store annual data for the given window
def make_folders(window):
    print('Making folders...')
    for year in get_year_list(window):
        os.makedirs(f'data/{window}/{year}', exist_ok=True)  # TEST WITHOUT EXIST_OK


# check if file contains burn data (or is a qa layer)
def is_burndata(filename):
    match = re.search(
        pattern='burndate.tif',
        string=filename
    )

    return match


# download all monthly tiffs for specified window and year
# WOULD BE NICE TO HAVE OPTION TO OVERWRITE OLD DATA
# NEED TO SPECIFY LOCATION TO EXPORT DATA
def download_tiff(window, year):
    with sftp.cd(f'data/MODIS/C6/MCD64A1/TIFF/{window}/{year}'):
        files = sftp.listdir()

        while files:
            file = files.pop()

            # check if file exists
            file_exists = os.path.isfile(f'./data/{window}/{year}/{file}')

            if is_burndata(file) and file_exists == False:
                print(f'- Downloading {file}...')
                sftp.get(file, f'./data/{window}/{year}/{file}')


# this is not ideal and leaves open to man in the middle attack (should get host key instead)
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

sftp = pysftp.Connection('fuoco.geog.umd.edu', username='fire', password='burnt', cnopts=cnopts)

windows = ['Win03']  # get_window_list()

while windows:
    window = windows.pop()
    print(f'** WORKING ON {window} **')

    make_folders(window)

    for year in get_year_list(window)[:3]:
        download_tiff(window, year)

#################

# for year in get_year_list(window):
#     download_tiff(window, year)
# windows = get_window_list()
# for window in windows:
#     make_folders(window)
#     for year in get_year_list(window):
#         download_tiff

#######################################
# def tiff_data(sftp):
#     with sftp.cd():
#         sftp.chdir('data/MODIS/C6/MCD64A1/TIFF')
#         sftp.chdir(window)
#         sftp.chdir(year)
#         files = sftp.listdir()
#         while files:
#             file = files.pop()
#             if check_burndata(file):
#                 print(f'Downloading {file}...')
#                 sftp.get(file)
        # data.chdir(window)
        # data.chdir(year)
        # for filename in data.listdir():
        #     if check_burndata(filename):
        #         fire_queue = 

# with sftp.cd():
# sftp.get()




# with sftp as conn:
#     with conn.cd('/data/MODIS/C6/MCD64A1/TIFF'):
#         with conn.cd(window):
#             files = conn.chdir(year).listdir()
#             for f in files:
#                 if check_burndata(f):
#                     conn.get(f)


#         # get filenames for data files (ignore qa for now...)
#         [filename for filename in sftp.listdir() if re.search(pattern='burndate.tif', string=filename)]
        
#         # for filename in conn.listdir():
#         #     if re.search(pattern='burndate.tif'):

#         data = conn.listdir()
#         data






# sftp.close()

# with sftp as conn:
