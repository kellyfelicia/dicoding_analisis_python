# Kelly Dashboard Collection
## Setup environmetn Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

##Setup environment shell/terminal
mkdir proyek_akhir
cd proyek_akhir
pipenv install
pipenv shell
pip install -r requirements.txt

##Run streamlit app\
streamlit run dashboard_ecommerce.py

