# recommendation-project

## Local development

### Prerequisites

- python3

### Setup in local machine

1. In terminal, navigate to the folder in which the repository will be located. Clone the repository here.

   ```
   git clone https://github.com/nusbeelab/recommendation-project.git
   ```

1. Change the current directory to the directory of the cloned repository.

   ```
   cd recommendation-project
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

1. Install oTree.

   ```
   pip3 install otree
   ```

1. To check that everything has been properly set up, start the development server.

   ```
   otree devserver
   ```

## Deployment
