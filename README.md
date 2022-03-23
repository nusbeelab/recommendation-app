# recommendation-project

## Usage

### Run the experiment with Prolific

1. (If the oTree site has not been added to oTree HR) On oTree HR, add our oTree site. This requires specifying the site's url i.e.
   `https://nus-recommendation-project.herokuapp.com` and the config variable `OTREE_REST_KEY` as set on Heroku.

1. Create a session on our oTree site, specifying an appropriate number of participants.

1. On oTree HR, click the "Prolific" hyperlink associated with our oTree site. Here, add the session code that was created in the previous step.

1. Click the "Configure" hyperlink associated with the added session.

1. Enter the following URL (exactly) into Prolific as the URL of the study.

   ```
   https://otree-hr.herokuapp.com/redirect_prolific/404/?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
   ```

1. Identify the completion URL of the study as provided by Prolific. Return to the Prolific configuration page of the current session on oTree HR and update the completion URL.

### Export data

Data collected by the oTree app can be exported at https://nus-recommendation-project.herokuapp.com/export.

- For responses to binary choice questions, use the "custom export" option to export the data.
- For the rest, use the default export.

## Local development

### Prerequisites

- python3

### Setup in local machine

1. In terminal, navigate to the folder in which the repository will be located. Clone the repository here.

   ```
   git clone https://github.com/nusbeelab/recommendation-app.git
   ```

1. Change the current directory to the directory of the cloned repository.

   ```
   cd recommendation-app
   ```

1. Create a virtual environment named `venv_otree` to manage dependencies for the project.

   ```
   python3 -m venv venv_otree
   ```

1. Activate the virtual environment that has been created. Once the virtual environment is active, the prompt in the terminal will begin with `(venv_otree)`.

   On Windows,

   ```
   venv_otree\Scripts\activate.bat
   ```

   On Unix or MacOS,

   ```
   source venv_otree/bin/activate
   ```

1. Install dependencies for development.

   ```
   pip3 install -r requirements-dev.txt
   ```

1. To check that everything has been properly set up, start the development server.

   ```
   otree devserver
   ```

### Run tests

To run unit tests

```
python3 -m unittest [test_module|test_class|test_method]
```

To run automated bots

```
otree test [session_config_name]
```

## Deployment

1. From the root directory of the repo, run `otree zip` to create an `.otreezip` file.
1. Upload the `otreezip` file to oTree Hub at the project deployment page. If necessary, reset DB as well.
