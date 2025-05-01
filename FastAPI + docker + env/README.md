# How to Deploy GCP Cloud Run
1. Have FastAPI on port `8080` in docker image

2. Set Up GCP

    1.  Enable required services `gcloud services enable run.googleapis.com`
    
    2.  Authenticate with your GCP account `gcloud auth login`
    
    3. set the active project `gcloud config set project [PROJECT_ID]`

3. Push Docker Image to Artifact Registry

    1. Create an Artifact Registry repository:
    ```
    $ gcloud artifacts repositories create [AR-folder_name] \
        --repository-format=docker \
        --location=asia-southeast1
    ```
    
    **Noted:** you can check folder create in AR

4. Tag the Local Docker Image

    ```
    $ docker tag [DOCKER-IMAGE-NAME] us-central1-docker.pkg.dev/[PROJECT_ID]/[AR-folder_name]/[DOCKER-IMAGE-NAME]

    Ex.. $ docker tag test_api asia-southeast1-docker.pkg.dev/cpf-aiml-cv/kim-test-api-repo/test_api
    ```

5. Push the Image to Artifact Registry
    ```
    $ docker push asia-southeast1-docker.pkg.dev/[PROJECT_ID]/[AR-folder_name]/[DOCKER-IMAGE-NAME]

    Ex. $ docker push asia-southeast1-docker.pkg.dev/cpf-aiml-cv/kim-test-api-repo/test_api
    ```

    if can not push try below before.

    ```
    $ gcloud auth configure-docker [REGION]-docker.pkg.dev --quiet

    # REGION= asia-southeast1
    ```
    **Noted**: you can check image already pull on AR

6. Deploy the Image to Cloud Run
    ```
    $ gcloud run deploy [Cloud-run-name-service] \
        --image asia-southeast1-docker.pkg.dev[PROJECT_ID]/[AR-folder_name]/[DOCKER-IMAGE-NAME] \
        --platform managed \
        --region asia-southeast1 
    ```

## Noted
### Other Command when used Cloud Run
Test Cloud run
```
$ gcloud auth activate-service-account --key-file=<json-key>
$ curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" [CLOUDRUN ENDPOINT]
```

other command 
```
$ gcloud auth login
$ gcloud auth list
$ gcloud config set account <service-account@developer.gserviceaccount.com> | AD-email
$ gcloud auth print-identity-token
$ gcloud auth activate-service-account --key-file=<json-key>
```