## Setting up a Conda Environment

### Pre-requisites
- Make sure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/aasem-research-work/combinatorics-unified.git
    ```

2. **Navigate to the Project Directory**
    ```bash
    cd combinatorics-unified
    ```

3. **Create a New Conda Environment**
    - If your project includes a `requirements.txt` file, you can create a new environment from this file.
    ```bash
    conda create --name your-environment-name --file requirements.txt
    ```

    - If you have specific packages that are not included in the `requirements.txt`, you can also manually add them.
    ```bash
    conda install -n your-environment-name package-name
    ```

4. **Activate the Conda Environment**
    ```bash
    conda activate your-environment-name
    ```

5. **Install PyQt5**
    - If PyQt5 is not included in the `requirements.txt`, you can install it manually.
    ```bash
    conda install -c anaconda pyqt
    ```

6. **Deactivate the Environment**
    - When you're done, you can deactivate the environment.
    ```bash
    conda deactivate
    ```

### Usage
1. **Activate the Conda Environment**
    ```bash
    conda activate your-environment-name
    ```
2. **Run the Application**
    ```bash
    python main.py
    ```

### Notes
- Replace `your-environment-name` with the name you want to give to your conda environment.
- Replace `your-username` with your GitHub username.
- Replace `package-name` with any additional packages you need.
