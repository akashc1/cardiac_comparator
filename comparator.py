import streamlit as st
import random
from typing import Union, Path, Tuple

from collections import namedtuple


Selection = namedtuple('Selection', ['real_vid', 'fake_vid', 'is_real'])

DATA_DIR = '/scratch/groups/willhies/cardiac_compare/2023_0209_dummy'
RESULTS_DIR = '/scratch/groups/willhies/cardiac_compare/outputs'


def get_video_paths(basedir: Union[Path, str], ext='.mp4') -> Tuple[list, list]:
    assert (real_dir := basedir / 'real').exists() and real_dir.is_dir()
    assert (fake_dir := basedir / 'fake').exists() and fake_dir.is_dir()

    real_vids = list(real_dir.glob(f'*{ext}'))
    fake_vids = list(fake_dir.glob(f'*{ext}'))

    return real_vids, fake_vids


def main():

    st.tile('Cardiac Comparator')
    st.markdown(
        'Evaluate our cardiac echo generative AI by selecting which echo from each pair'
        ' is the real one!'
    )

    basedir = st.text_input(
        'Base directory (containing both real + synthetic echo scans',
        value=DATA_DIR,
    )
    extension = st.selectbox('Video filetype', options=('.mp4', '.avi'))

    with st.spinner('Collecting real and synthetic examples...'):
        real_vids, fake_vids = get_video_paths(basedir, ext=extension)

    output_dir = st.text_input('Output folder', value=RESULTS_DIR)

    st.session_state.record = []

    while True:



if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()
