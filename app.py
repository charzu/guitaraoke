import streamlit as st

from downloader import join_parts

PARTS = ['bass',
         'drums',
         'piano',
         'vocals',
         'other',
         ]


@st.cache
def download_and_split(url):
    from downloader import download_and_split
    return download_and_split(url)


def main():
    with st.form('Parameters:'):

        url = st.text_input('Paste YouTube link:')

        parts = []
        for part in PARTS:
            if st.checkbox(part, value=part != 'other'):
                parts.append(part)
        st.form_submit_button('Działaj!')

    if not url:
        st.error('Paste link to youTube video')
        return

    if not parts:
        st.error('Include at least one part')
        return

    sounds = download_and_split(url)

    result_buffer = join_parts(parts, sounds)
    filename = '_'.join(parts) + '.mp3'
    st.download_button('Download', result_buffer.read(), filename)


if __name__ == '__main__':
    main()
