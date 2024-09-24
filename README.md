# YouTube Converter

Built using Flask and SQLAlchemy

## Features

- **User Authentication**: Register and log in to use the conversion features.
- **Video Conversion**: Download and convert YouTube videos to MP3 format.

# Testing YouTube Converter

Built using Robot Framework and SeleniumLibrary

## Features

- **User Registration**: Test the ability to register a new user with a unique username and password.
- **User Login**: Verify that registered users can log in to the application.
- **Video Conversion**: Test the conversion of a YouTube video link to MP3 format.
- **Success Verification**: Ensure that the success page displays the appropriate messages and download links.

## Limitations

- **Video Length**: The current implementation is not optimized for converting long videos (approximately over five minutes). Tests may fail if the conversion time exceeds expected limits.