# RedditToVideo

This Python script generates a video from top comments on a Reddit thread and overlays subtitles using MoviePy library.

## Dependencies

- `moviepy` (install with `pip install moviepy`)
- `requests`
- `pyttsx3`
- `nltk`

Make sure to have these Python libraries installed before running the script.

## Usage

1. Clone the repository or download the script files.
2. Ensure all dependencies are installed (`moviepy`, `requests`, `pyttsx3`, `nltk`).
3. Place a background video in the `background/` directory named `background_video.mp4`.
4. Change the `REDDIT_URL` variable in the script to the desired Reddit thread URL.
5. Change the `USERNAME` variable in the script to what text you want in the header image username spot.
6. Place an image in this directory named `icon.png` of what image you want in the header image profile picture spot.
7. Run the script using Python 3:

   ```bash
   python main.py

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### `Acknowledgements`

The `tiktokvoice.py` script is licensed under the MIT License and was authored by Mark Reznikov in 2024.