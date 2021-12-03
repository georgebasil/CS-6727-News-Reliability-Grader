# News Reliability Grader


### Abstract

The internet has allowed misinformation to spread with little push-back enabling malicious actors to target subsets of people for cyber-attacks. Current defenses lack unbiased and immediate warnings to readers prior to reading and/or sharing news stories. In this report, a new solution is introduced which aims to deliver an unbiased and real-time news website reliability grade. The solution is achieved through a trained machine learning model on unbiased technical characteristics of recognized legitimate and misinformation sites with the machine learning model’s prediction made available immediately to readers through a Google Chrome extension in the form of a letter grade. This report will share the solution details and demonstrate its high success rate as an unbiased real-time news website reliability grader and as a necessary defense from cyber-attacks through misinformation.

### Design

<center><img src="/images/High-Level-Design-Diagram.png"></center>
<center>High Level Design Diagram</center>

### Installation

To use this project for self use, follow the installation steps below. 

###### System Requirements
 - Python version 3.7 or greater
 - Apache version 2.4 or greater
 - PHP version 5.6 or greater
 - Google Chrome version 88 or greater

###### API Keys
 - Sign up for an IPInfo API key here: https://ipinfo.io/
 - Sign up for a Klazify API key here: https://www.klazify.com/

###### Steps to use the machine learning model with pre-prepared training data
 1. Stand up a PHP-based web application locally or in the cloud
 2. Copy the Web-Server/classify.php file into your working web directory
 3. Copy the Web-Server/cgi-bin directory into the cgi-bin directory of your web server
 4. Update line 9 of Web-Server/classify.php replacing <PATH-TO-CGI-BIN-DIRECTORY> with your path
 5. Use the Web-Server/cgi-bin/requirements.txt file to install the necessary Python packages
 6. Update lines 51 and 81 of Web-Server/cgi-bin/train_model.py replacing <PATH-TO-WORKING-DIRECTORY> with your path
 7. Execute Web-Server/cgi-bin/train_model.py to train and save the model
 8. Update line 32 of Web-Server/cgi-bin/classify.py replacing <PATH-TO-WORKING-DIRECTORY> with your path
 9. Update line 15 of Web-Server/cgi-bin/classify.py replacing <YOUR-KLAZIFY-API-KEY> with your Klazify API key
 10. Update lines 284 and 285 of Web-Server/cgi-bin/fetch_data.py replacing <PATH-TO-WORKING-DIRECTORY> with your path
 11. Update line 207 of Web-Server/cgi-bin/fetch_data.py replacing <YOUR-IPINFO-API-KEY> with your IPInfo API key
 12. Update lines 51, 52, and 64 of Web-Server/cgi-bin/predict.py replacing <PATH-TO-WORKING-DIRECTORY> with your path
 13. Ensure your Apache web server is running
 14. The ML model is now ready to service API requests for predictions

###### Steps to use the Google Chrome extension
 1. Update line 23 of Google-Chrome-Extension/News-Reliability-Grader/js/background.js replacing <API-HOSTNAME-PATH-ENDPOINT-HERE> with your API endpoint created through the steps above
 2. Use Google Chrome to enter the extension management options and enable "Developer Mode" to install the extension (unpackaged)

###### Steps to produce a new training dataset
 1. Use the Training-Dataset/requirements.txt file to install the necessary Python packages
 2. Update lines 231, 276, and 277 of Training-Dataset/build_training_dataset.py replacing <PATH-TO-WORKING-DIRECTORY> with your path
 2. Update line 208 of Training-Dataset/build_training_dataset.py replacing <YOUR-IPINFO-API-KEY> with your IPInfo API key
 3. Execute Training-Dataset/build_training_dataset.py to generate a new training dataset CSV file using the existing sites.csv
 4. (optional) Replace sites.csv with a new file for creating a new training dataset. The format requirements are: DOMAIN,TRUE-SCORE (1/0)

### Disclaimer

This project was completed as part of the graduate course CS-6727 at the Georgia Institute of Technology. The project is free and available for future development. The project was NOT developed for deployment or any commercial use.
