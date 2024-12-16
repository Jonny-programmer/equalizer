import ffmpeg


def overlay_audio_on_video(video_file, audio_file, output_file, start_time, end_time):
    video = ffmpeg.input(video_file, ss=start_time, t=end_time - start_time)

    audio = ffmpeg.input(audio_file)

    ffmpeg.output(video, audio, output_file, vcodec="copy", acodec="aac").run(overwrite_output=True)


video_file = "/Users/eremin/Desktop/Films/eric_chien.mp4"
audio_file = ".data/music/JUST LIKE YOU - NF.mp3"
output_file = "Result.mp4"

start_time = 10
end_time = 20

overlay_audio_on_video(video_file, audio_file, output_file, start_time, end_time)
