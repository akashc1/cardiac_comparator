import streamlit as st
import numpy as np
import random
from typing import Union, Path, Tuple, List

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

    np.random.shuffle(real_vids)
    np.random.shuffle(fake_vids)

    output_dir = st.text_input('Output folder', value=RESULTS_DIR)

    st.session_state.record = []

    quit_col1, quit_col2 = st.columns(2)
    quit_button_w_write = quit_col1.button('Quit & write results')
    quit_button = st.button('Quit')

    display_form = st.form('Comparator')
    form_col1, form_col2 = display_form.columns(2)

    while not (quit_button_w_write or quit_button) and real_vids and fake_vids:
        real_vid, fake_vid = real_vids[0], fake_vids[0]
        real_vids, fake_vids = real_vids[1:], fake_vids[1:]
        real_pos = random.choice((0, 1))
        col1_vid, col2_vid = (fake_vid, real_vid) if real_pos else (real_vid, fake_vid)
        form_col1.video(col1_vid)
        form_col2.video(col2_vid)

        selection = display_form.radio('Select which of the two echo\'s is real', ['left', 'right'])
        selection = bool(selection == 'right')
        is_real = real_pos == selection
        st.session_state.record.append(Selection(real_vid, fake_vid, is_real))
        st.write(f"Selection: {Selection(real_vid, fake_vid, is_real)}")

    st.write("Hit the quit + write? {quit_button_w_write}\tJust quit? {quit_button}")


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()
