# Chand

Chand is an ML project designed to turn raw data into usable software. It collects data from a car marketplace website, trains machine learning models on the data, and presents the predictions to users through a web interface. Chand specifically targets Persian users.

## Project Overview
Chand aims to simplify the process of browsing and analyzing car listings by leveraging machine learning techniques. By scraping data from a car marketplace, the project enables users to obtain insights and predictions regarding car brands, models, years, mileage, and prices.

## Features
- Data collection from a car marketplace website.
- Training machine learning models on the collected data.
- Web interface for users to interact with the trained models and receive predictions.

## Technologies Used
- Scikit learn
- TensorFlow
- Flask
- MySQL
- Selenium
- Jupyter Notebook

## Installation
To install and set up Chand on your local machine, follow these steps:

1. Clone the repository:
git clone https://github.com/TheMightyEmad/chand-ml-model-deployment.git

2. Navigate to the project directory:
cd chand

3. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate

4. Install the required dependencies:
pip install -r requirements.txt

## Usage
To run Chand and interact with the web interface, follow these steps:

1. Set up the MySQL database:
- Start your MySQL server.
- Run the following queries to create the necessary database and tables:
  ```sql
  CREATE DATABASE main_database COLLATE utf8mb4_0900_ai_ci;
  CREATE TABLE `scrape` (
    `id` int NOT NULL AUTO_INCREMENT,
    `brand` varchar(50),
    `model` varchar(50),
    `prod_year` int,
    `mileage` int,
    `trim` varchar(50),
    `location` varchar(100),
    `price` bigint,
    PRIMARY KEY (`id`)
  );
  CREATE TABLE `dict_value` (
    `model` varchar(255),
    `encoded` decimal(65,10),
    `year` varchar(25),
    `id` int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`)
  );
  ```

2. Configure the SQL connection:
- In the `scraper.py` file, enter the appropriate information for your SQL connection.

3. Scrape the data:
- Adjust the address and regex for your target car marketplace website in `scraper.py`.
- Run `scraper.py` to collect data from the website and populate the MySQL database.

4. Train the models:
- Open and run the Jupyter Notebook file `model_training.ipynb`.
- Experiment with hyperparameters and explore different models.

5. Generate model files:
- Place the `location_dict.joblib` and ML models (with a `.joblib` format) in the `website/models` folder.

6. Run the web interface:
- Execute the following command in the terminal:
  ```
  cd website
  python app.py
  ```
- Access the web interface in your browser at `http://localhost:5000`.

## Folder Structure
The main folders and files in the repository are structured as follows:

- `website/`: Contains the Flask application files and website-related components.
- `models/`: Stores ML models and related files.

## License
This project is licensed under the MIT License.
