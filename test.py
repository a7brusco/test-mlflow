import os
import mlflow
import yaml

def change_artifact_uri(dirname: str, run: mlflow.entities.Run, new_path: str):
    mlruns_dir = os.path.join(r"//192.168.4.204/dna/test-mlflow", "")
    assert os.path.isdir(mlruns_dir)
    meta_run = os.path.join(mlruns_dir, run.info.experiment_id, run.info.run_id, "meta.yaml")
    with open(meta_run, "r+") as f:
        data = yaml.safe_load(f)
        data["artifact_uri"] = os.path.join(new_path, run.info.experiment_id, run.info.run_id)
        yaml.dump(data, f)


if __name__ == "__main__":
    mlflow.set_tracking_uri(r"//192.168.4.204/dna/test-mlflow")
    tracking_uri = mlflow.get_tracking_uri()
    print("Current tracking uri: {}".format(tracking_uri))

    with mlflow.start_run() as run:
        mlflow.log_param('my','param')
        mlflow.log_metric('score', 100)
        change_artifact_uri("test", mlflow.active_run(), r"//192.168.4.204/dna/test-mlflow-artifacts")
        mlflow.log_artifacts(os.path.join(os.path.dirname(__file__), "test", ""))

        artifact_uri = mlflow.get_artifact_uri()
        print("Current artifact uri: {}".format(artifact_uri))