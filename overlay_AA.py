import ffmpeg


def overlay_audio_on_video(video, sound, res_path, t0, t1):
    video = ffmpeg.input(video, ss=t0, t=t1 - t0)

    audio = ffmpeg.input(sound)

    ffmpeg.output(video, audio, res_path, vcodec="copy", acodec="mp3").run(overwrite_output=True)
