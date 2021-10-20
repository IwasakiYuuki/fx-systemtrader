## Argo Workflow
Argo WorkflowはKubernetesのワークフロー管理ツールで，デフォルトでは設定しずらいジョブの並列化や依存関係などをマニフェストから簡単に指定できる．
本システムではGKE上で機械学習などのパイプラインを実装するためにArgo Workflowを使用する．

## ディレクトリ構造
```
.
├── sample-iris                        # サンプル：Irisの分類
│   ├── train_model
│   │   ├── Dockerfile
│   │   └── main.py
│   ├── upload_result
│   │   ├── Dockerfile
│   │   └── main.py
│   └── workflow.yaml
└── tutorial                           # 公式チュートリアル（helloworldとartifactのinput，output）
    ├── artifact_workflow.yaml
    ├── gpu_test.yaml                  # GPUノードが使用できるかのテスト用
    ├── helloworld_workflow.yaml
    ├── serviceaccounts
    │   └── argo-tutorial-sa.yaml
    └── workload-identity-test.yaml    # Workload Identityが機能してるかチャック用
```
各ワークフローはサブディレクトリごとに分けている．
基本的にはその中のworkflow.yamlにワークフローの設定が書かれており，実行する各ステップのプログラムなどはDockerイメージしてGCRにアップロードする．
実行する際にはargo CLIを使って```argo submit workflow.yaml```とする方法と，```kubectl apply -f workflow.yaml```で行う方法がある．

## TODO
- ルートにMakefileを作成して，Cloud Buildでワークフローのアップロードなどをするときに１コマンドで出来るようにする．
- いずれスケジューラなどを設定して一定の間隔で実行などをするため，workflow.yaml以外のマニフェストもMakefileで追加できるようにする．
- サブディレクトリにもそれぞれMakefileを作成して，ルートから伝搬させられるようにする．
