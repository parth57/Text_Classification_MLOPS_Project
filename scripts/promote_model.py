# promote model
import os, httpx, certifi
import mlflow

def promote_model():
    # Set up DagsHub credentials for MLflow tracking
    os.environ["SSL_CERT_FILE"] = certifi.where()
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ["MLFLOW_TRACKING_INSECURE_TLS"] = "true"  # disable SSL verify

    os.environ["MLFLOW_TRACKING_REQUESTS_VERIFY"] = "false"

    orig_init = httpx.Client.__init__
    def patched_init(self, *args, **kwargs):
        kwargs["verify"] = False
        return orig_init(self, *args, **kwargs)

    httpx.Client.__init__ = patched_init
    dagshub_token = os.getenv("CAPSTONE_TEST")
    dagshub_token = os.getenv("CAPSTONE_TEST")
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "parth57"
    repo_name = "Text_Classification_MLOPS_Project"

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.MlflowClient()

    model_name = "sentiment_model"
    # Get the latest version in staging
    latest_version_staging = client.get_latest_versions(model_name, stages=["Staging"])[0].version

    # Archive the current production model
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived"
        )

    # Promote the new model to production
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage="Production"
    )
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promote_model()
