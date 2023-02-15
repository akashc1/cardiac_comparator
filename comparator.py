from collections import namedtuple
import csv
from datetime import datetime
from pathlib import Path
import random
from typing import List, Tuple, Union
from uuid import uuid4

import numpy as np
import streamlit as st

Selection = namedtuple(
    'Selection',
    [
        'real_vid', 'fake_vid', 'real_selection', 'real_pos', 'selected_real',
    ],
)

DATA_DIR = '/scratch/groups/willhies/cardiac_compare/2023_0209_dummy'
RESULTS_DIR = '/scratch/groups/willhies/cardiac_compare/outputs'


def get_video_paths(basedir: Union[Path, str], ext='.mp4') -> Tuple[list, list]:
    basedir = Path(basedir)
    assert (real_dir := basedir / 'real').exists() and real_dir.is_dir(), str(real_dir)
    assert (fake_dir := basedir / 'synthetic').exists() and fake_dir.is_dir(), str(fake_dir)

    real_vids = [str(p) for p in real_dir.glob(f'*{ext}')]
    fake_vids = [str(p) for p in fake_dir.glob(f'*{ext}')]

    return real_vids, fake_vids


def init_state():
    state = st.session_state

    if 'record' not in state:
        state['record'] = []

    if 'videos' in state:
        return

    videos = {}
    with st.spinner('Collecting real and synthetic examples...'):
        videos['real'], videos['fake'] = get_video_paths(
            state['video_basedir'], state['vid_filetype'],
        )

    np.random.shuffle(videos['real'])
    np.random.shuffle(videos['fake'])

    st.session_state['videos'] = videos


def submit_one():
    state = st.session_state

    assert 'record' in state
    real_selection = int(state['real_select'].lower() == 'right')
    selected_real = real_selection == state['real_pos']
    new_selection = Selection(
        state['real_vid'],
        state['fake_vid'],
        real_selection,
        state['real_pos'],
        selected_real,
    )

    state.record.append(new_selection)


def iter_videos():
    state = st.session_state
    video_state = state['videos']

    real_vid, fake_vid = video_state['real'][0], video_state['fake'][0]
    video_state['real'] = video_state['real'][1:]
    video_state['fake'] = video_state['fake'][1:]
    real_pos = random.choice((0, 1))

    state['real_vid'], state['fake_vid'], state['real_pos'] = real_vid, fake_vid, real_pos

    return real_vid, fake_vid, real_pos


def have_more_videos():
    video_state = st.session_state.videos
    return bool(video_state['real']) and bool(video_state['fake'])


def write_outputs():
    state = st.session_state

    output_dir, trial_id = state['output_dir'], state['trial_id']
    out_file = Path(output_dir) / f'{trial_id}.csv'
    with open(out_file, 'w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=Selection._fields, delimiter=',')
        st.write(Selection._fields)
        writer.writeheader()
        for s in state.record:
            st.write(s._asdict())
            writer.writerow(s._asdict())

    st.write(f"Wrote session results to {str(out_file)}")


def main():

    st.title('Cardiac Comparator')
    st.markdown(
        'Evaluate our cardiac echo generative AI by selecting which echo from each pair'
        ' is the real one!'
    )

    basedir = st.text_input(
        'Base directory (containing both real + synthetic echo scans)',
        value=DATA_DIR,
        key='video_basedir',
    )
    extension = st.selectbox('Video filetype', options=('.mp4', '.avi'), key='vid_filetype')
    output_dir = st.text_input('Output folder', value=RESULTS_DIR, key='output_dir')
    default_id = (
        datetime.now().strftime('%Y%m%d_%H%M%S_') + str(uuid4()).replace('-', '')
        if 'trial_id' not in st.session_state else st.session_state['trial_id']
    )
    trial_identifier = st.text_input('Trial ID', value=default_id, key='trial_id')

    init_state()

    if have_more_videos():
        real_vid, fake_vid, real_pos = iter_videos()
        col1_vid, col2_vid = (fake_vid, real_vid) if real_pos else (real_vid, fake_vid)

        with st.form(f'Comparator {col1_vid} vs. {col2_vid}'):
            form_col1, form_col2 = st.columns(2)

            form_col1.video(str(col1_vid))
            form_col2.video(str(col2_vid))
            selection = st.radio(
                'Please select the real echo',
                ['Left', 'Right'],
                key='real_select',
            )
            st.form_submit_button("Submit", on_click=submit_one)
    else:
        st.write(f"Completed all videos!")

    quit_col1, quit_col2 = st.columns(2)
    quit_button_w_write = quit_col1.button('Quit & write results')
    quit_button = quit_col2.button('Quit')

    if quit_button_w_write:
        st.write("Writing results and quitting!")
        write_outputs()
        return

    if quit_button:
        st.write("Quitting without writing results!")
        return

if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()
