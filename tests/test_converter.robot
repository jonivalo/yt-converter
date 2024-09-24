*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${SERVER_URL}    http://127.0.0.1:5000
${USERNAME}      testname
${PASSWORD}      testpassword
${VIDEO_URL}     https://www.youtube.com/watch?v=gzB3EDODx5I

*** Test Cases ***
Test User Registration, Login, and Video Conversion
    [Documentation]    Test the user registration, login, video conversion, and success page verification.

    # Register user
    Open Browser    ${SERVER_URL}/register    Chrome
    Maximize Browser Window
    Input Text      name=username    ${USERNAME}
    Input Text      name=password    ${PASSWORD}
    Click Button    xpath=//button[@type='submit']

    # Log in user
    Wait Until Element Is Visible    name=username
    Input Text      name=username    ${USERNAME}
    Input Text      name=password    ${PASSWORD}
    Click Button    xpath=//button[@type='submit']

    # Wait for redirect to converter page
    Wait Until Page Contains    Convert YouTube Video to MP3

    # Convert YouTube video to MP3
    Input Text      name=link    ${VIDEO_URL}
    Click Button    xpath=//button[@type='submit']

    # Wait for conversion to complete and redirect to success page
    Wait Until Page Contains    Your MP3 file is ready! 🎉

    # Wait for the download button to appear
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Download your MP3')]
    Click Link    xpath=//a[contains(text(), 'Download your MP3')]