# Project KV
A simple e-commerce style website for a graphic designing company.

## Tech Stack: 
* Flask Framework for Python
* Python
* HTML
* SCSS
* Bootstrap style library
* Fontawesome icons library
* JavaScript
* Node Package Manager (npm)

## Visual Studio Code Plugins: 
* Live Sass Compiler - **Required** *For SCSS Preprocessing*
* Material Icon Theme - *Optional*
* Flask Snippets - *Optional*

## Steps: Clone and Set up in Local system.

### Cloning the repository.
* Install git bash.
* Run Command   ```git clone https://github.com/kreativision/ProjectKV.git``` in a directory of your choice.

### Setting up python environment.
* Make sure **python 3.8.6** or higher is installed.
* Run Command   ```virtualenv venv``` inside the directory where the repository is cloned.
  * A new directory called **venv** will be created.
* Run Command   ```venv/Scripts/activate.ps1``` to activate the cirtual environment.
* Run Command   ```pip install -r requirements.txt``` to install all the required dependencies for the current app state.

### Setting up bootstrap and fontawesome.

* Make sure **Node.js version 10** or higher is installed.

##### Bootstrap
* Run Command   ```npm install bootstrap --save``` in the virtual environment terminal.
  * A new directory called **node_modules** will be created.
  * There should be a **bootstrap** folder inside.
  
##### Fontawesome
* Run Command   ```npm install @fortawesome/fontawesome-free --save``` in the virtual environment terminal.
  * A new directory called **@fortawesome** will be created inside the *node_modules* folder.
* Create a folder **fontawesome** inside *app/static* direcotry.
* Copy folders **scss, sprites, svgs** from *node_modules/@fortawesome/fontawesome-free* and paste into *app/static/fontawesome*.

##### Verify setup: 
* Run the **Live Sass Compiler**. If no error occurs, everything is just fine.

## Running the project: 
Make sure that virtual environment is activated.  
Run Command ```python app/app.py```.  
If all went well, the output should read  
```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 232-721-636
 * Running on http://0.0.0.0:6174/ (Press CTRL+C to quit)
```  
Open your browser to ```http://localhost:6174``` to view the app.


## Important Notes:

### Installing new Flask dependencies.
After installing any new Flask specific dependency, run command ```pip freeze > requirements.txt``` inside the virtualenv terminal to update the *requirements.txt* file. 

### Viewing the app in your local network.
* On an andministrator terminal, run command ```ipconfig```
* Look for something similar to ```IPv4 Address. . . . . . . . . . . : 192.168.XX.XXX```
  * This is the IP of your machine.
* On a device connected to your local network, access the URL ```http://192.168.XX.XXX:6174``` to view your app.
