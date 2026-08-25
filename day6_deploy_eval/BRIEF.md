# Day 6 — Deploy + Evaluation

**Why this is a brief:** deployment (Agent Runtime, Cloud Run, GKE) and the
eval framework both need a real GCP project and exact current commands. Look
them up from official docs. Don't guess at the syntax.

**Concept:**

- Two separate concerns: does the agent run somewhere other than your machine
  (deploy), and does it still work correctly after a change (eval).
- ADK's eval framework exists because "still works" is fuzzier to check for an
  LLM agent than for normal code. The same input can validly produce
  different, still-correct outputs.

**Build task:**

1. Deploy the smallest agent (`day1_single_agent`) to Cloud Run. Get a real
   URL you can hit.
2. Write 3-5 eval cases for `day1_single_agent` using ADK's eval framework, for
   example, "asks about Tokyo weather → should call get_forecast with
   city='Tokyo'." Run them.
3. Break something on purpose, for example, rename a tool without updating the
   instruction, and confirm the eval cases catch it. An eval suite that
   doesn't fail when you break what it's testing isn't testing anything. This
   step is the actual point of the exercise.

## Deploy sequence (`tools/deploy.py`)

```mermaid
sequenceDiagram
    actor Dev
    participant Script as tools/deploy.py
    participant GC as gcloud
    participant CLI as adk deploy cloud_run
    participant CB as Cloud Build
    participant AR as Artifact Registry
    participant CR as Cloud Run
    Dev ->> Script: python day6_deploy_eval/tools/deploy.py
    Script ->> GC: services enable run/cloudbuild/artifactregistry
    Script ->> GC: projects add-iam-policy-binding ... roles/run.builder
    Note over Script, GC: fixes the real gotcha this hit:<br/>Google no longer auto-grants this to the default compute SA
    Script ->> CLI: adk deploy cloud_run --project --region day1_single_agent
    CLI ->> CLI: generate Dockerfile, copy agent source
    CLI ->> GC: gcloud run deploy --source ...
    GC ->> CB: upload source, build container
    CB ->> AR: push built image
    CB -->> GC: build succeeded
    GC ->> CR: create revision, route 100% traffic
    Script ->> GC: run services describe --format=value(status.url)
    Script ->> CR: GET {url}/list-apps
    CR -->> Script: 200, [day1_single_agent]
    Script -->> Dev: "Live: {service_url}"
```

## Eval framework (mechanics, independent of whether the run finished)

```mermaid
sequenceDiagram
    actor Dev
    participant Test as test_eval.py
    participant Eval as AgentEvaluator
    participant Agent as day1_single_agent.root_agent
    participant Model as Gemini
    Dev ->> Test: pytest -m integration
    Test ->> Eval: evaluate(agent_module, eval_dataset_dir, num_runs=1)
    loop each case in weather_and_time.test.json
        Eval ->> Agent: send query, e.g. "What's the weather in Tokyo?"
        Agent ->> Model: LLM turn
        Model -->> Agent: tool_call get_forecast(city="Tokyo")
        Agent -->> Eval: actual tool trajectory
        Eval ->> Eval: compare actual vs expected_tool_use
    end
    Eval -->> Test: tool_trajectory_avg_score vs 1.0 threshold (test_config.json)
    Test -->> Dev: pass/fail
```
