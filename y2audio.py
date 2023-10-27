import os
import requests
from pytube import YouTube
# from transformers import pipeline, set_seed

## Setup Text Generation Pipeline
# generator = pipeline('text-generation', model='gpt2')

## Setup Random State for reducing randomness & enhance reproducibility
# set_seed(42) 

def download_audio_from_youtube(video_link):
  destination = 'audio/'

  try:
    video = YouTube(video_link)
    audio = video.streams.filter(only_audio=True).first()
    audio.download(output_path=destination)

    default_filename = audio.default_filename
    filename = video.title
    new_filename = f"{filename}.wav"
    os.rename(os.path.join(destination, default_filename),
              os.path.join(destination, new_filename))

    return os.path.join(destination, new_filename)

  except Exception as e:
    print("Error:", str(e))
    return None


def delete_audio_file(file_path):
  try:
    if os.path.exists(file_path):
      os.remove(file_path)
      print("Audio file deleted successfully.")
    else:
      print("Audio file does not exist.")

  except Exception as e:
    print("Error occurred while deleting the audio file:", str(e))


# Add function that gets youtube_link and returns dictionary: 'title', 'description'
def get_data_from_youtube(video_url):
  yt = YouTube(video_url)

  title = yt.title
  author = yt.author
  channel_url = yt.channel_url
  publish_date = yt.publish_date
  # gen_data = generator(title, max_length=50, num_return_sequences=1)
  # content = gen_data[0]['generated_text']
  try:
    response = requests.get('https://api.chucknorris.io/jokes/random')
    content = response.json()["value"]
  except Exception as e:
    print("Error: ", e)
    content = "Some Text!"
  return {
    'title': title,
    'author': author,
    'channel_url': channel_url,
    'publish_date': publish_date,
    'content': content
  }


def main():
  pass


if __name__ == '__main__':
  main()
