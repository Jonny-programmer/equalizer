import ffmpeg

def overlay_audio_on_video(video, sound, res_path, t0, t1):
    video = ffmpeg.input(video, ss=t0, t=t1 - t0)

    audio = ffmpeg.input(sound)

    ffmpeg.output(video, audio, res_path, vcodec="copy", acodec="mp3").run(overwrite_output=True)


video_file = "/Users/eremin/Desktop/Films/eric_chien.mp4"
audio_file = ".data/music/JUST LIKE YOU - NF.mp3"
output_file = "Result.mp4"

start_time = 10
end_time = 20

overlay_audio_on_video(video_file, audio_file, output_file, start_time, end_time)
