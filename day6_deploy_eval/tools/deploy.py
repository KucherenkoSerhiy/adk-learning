"""Deploys day1_single_agent to Cloud Run.

Run directly: python day6_deploy_eval/tools/deploy.py
Idempotent: safe to re-run (API enablement and IAM binding are no-ops if
already in place; redeploying just creates a new revision).

Requires: gcloud CLI installed, `gcloud auth login` already done.
"""
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from constants import AGENT_DIR, PROJECT, REGION, SERVICE_NAME

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_gcloud() -> tuple[str, dict]:
    """Full gcloud executable path, plus an environment with its directory on PATH.

    subprocess.run() without shell=True does not apply PATHEXT resolution to a
    bare "gcloud" — Windows' gcloud is a .cmd file, so the call needs the fully
    resolved path. The PATH fixup on top is still needed separately: `adk deploy
    cloud_run` shells out to `gcloud` by bare name internally, so the subprocess
    it spawns needs PATH to be right too.
    """
    env = os.environ.copy()
    gcloud = shutil.which("gcloud", path=env["PATH"])
    if gcloud is None:
        windows_sdk_bin = (
            Path(os.environ.get("LOCALAPPDATA", ""))
            / "Google" / "Cloud SDK" / "google-cloud-sdk" / "bin"
        )
        gcloud = str(windows_sdk_bin / "gcloud.cmd")
        if not Path(gcloud).exists():
            sys.exit("gcloud not found on PATH or at the default Windows Cloud SDK location.")
        env["PATH"] = f"{windows_sdk_bin}{os.pathsep}{env['PATH']}"
    return gcloud, env


def _adk_executable() -> str:
    """The adk console script next to the running interpreter, PATH-independent."""
    suffix = ".exe" if os.name == "nt" else ""
    return str(Path(sys.executable).parent / f"adk{suffix}")


def main():
    gcloud, env = _resolve_gcloud()

    print("Enabling required APIs (Cloud Run, Cloud Build, Artifact Registry)...")
    subprocess.run(
        [
            gcloud, "services", "enable",
            "run.googleapis.com", "cloudbuild.googleapis.com", "artifactregistry.googleapis.com",
            f"--project={PROJECT}",
        ],
        env=env, check=True,
    )

    print("Granting roles/run.builder to the default Compute Engine service account...")
    project_number = subprocess.run(
        [gcloud, "projects", "describe", PROJECT, "--format=value(projectNumber)"],
        env=env, check=True, capture_output=True, text=True,
    ).stdout.strip()
    compute_sa = f"{project_number}-compute@developer.gserviceaccount.com"
    subprocess.run(
        [
            gcloud, "projects", "add-iam-policy-binding", PROJECT,
            f"--member=serviceAccount:{compute_sa}",
            "--role=roles/run.builder",
            "--condition=None",
        ],
        env=env, check=True, capture_output=True,
    )

    print(f"Deploying {AGENT_DIR} to Cloud Run service '{SERVICE_NAME}'...")
    subprocess.run(
        [
            _adk_executable(), "deploy", "cloud_run",
            f"--project={PROJECT}",
            f"--region={REGION}",
            f"--service_name={SERVICE_NAME}",
            f"--app_name={AGENT_DIR}",
            str(REPO_ROOT / AGENT_DIR),
            "--", "--allow-unauthenticated", "--quiet",
        ],
        env=env, check=True,
    )

    service_url = subprocess.run(
        [
            gcloud, "run", "services", "describe", SERVICE_NAME,
            f"--region={REGION}", f"--project={PROJECT}",
            "--format=value(status.url)",
        ],
        env=env, check=True, capture_output=True, text=True,
    ).stdout.strip()

    print(f"Verifying {service_url}/list-apps ...")
    with urllib.request.urlopen(f"{service_url}/list-apps", timeout=30) as resp:
        body = resp.read().decode()
    if AGENT_DIR not in body:
        sys.exit(f"Deployed, but {AGENT_DIR} not found in /list-apps response: {body}")

    print(f"Live: {service_url}")


if __name__ == "__main__":
    main()
