# AI

### Environment Requirement

1. Ubuntu 18.04

2. Anaconda 

3. Nvidia driver. (Make sure able to run `nvidia-smi` in terminal.)


### Installation for development

1. conda create -n <env_name> python=3.7.9

2. conda activate <env_name>. Check `pip` installed. if not run `conda install pip`

3. git clone https://gitlab.com/vii3/real-time-face-rec/ai.git

4. cd ai and run `pip install -r requirements.txt`


### Download and Compile Model 

1. cd ./face-compare-matching-service/src/provider


2. Download from DVC via using `dvc pull -r s3`. If download success the terminal shown below

   

>  A       models/face_embedding data/                                                                                                         
>  A       models/face_detect/data/                                                                                                            
>  2 files added and 15 files fetched   


   If cannot download model. Please ensure you export the AWS environments (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION). for example using `export AWS_ACCESS_KEY_ID=Accesskey` or add `export AWS_ACCESS_KEY_ID=Accesskey` in `.bashrc`

3. Compile model. cd ./face-compare-matching-service/src/provider/models/face_detect

4. Run command `make`


### Run Service

1. Run main agent service using `python main.py`


### Branch Strategy

1. Branching strategy:
   - **production** - archived project. project which in production state.
   - **develop** - project in development status. should be runable. contains all of finished features. may different compared to release branch.
   - **staging** - project in staging state which is a state for testing.
   - **feature/{ feature-name in lowercase, dash separate }** - should contain meaningful feature name. should be independent as much as possible.
   - **refactor/{ context in lowercase, dash separate }** - same as feature branch. But no new features introduced in this branch.
   - **bugfix/{ bug-name or id in lowercase, dash separate }** - bugfix prioritized by planing.
   - **hotfix/{ bug-name or id lowercase, dash separate }** - on production bugfix. emergency bugfix.

2. Checkout new branch in context ex:
```bash
git checkout -b feature/new-feature
```





