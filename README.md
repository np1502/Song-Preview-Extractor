# Song-Preview-Extractor

1.Dataset Link - https://drive.google.com/drive/folders/1iHcEPlTOpOY5Me6TBBZVz83DbhwQCYZi?usp=sharing

# Description

An AI based project aiming to extract teaser of a song based on vocals and accompainment , which can be used for making Instagram Reels , Tiktok and also for advertisment of the song.

Dataset was created from Instagram reels using Selenium-based script and used source separation tool "Spleeter" to separate the song file to its components.

Using Mel Spectogram , Wavenet AutoEncoder and MFCC converted the original file and splitted components into embeddings and finally converting these into 3 channels
of the image fed into the CNN network of size [1024,1024,3]

After performing similar preprocessing on y_data [128,128,3] and using RMSE loss for each channel respectively , we trained the model.
